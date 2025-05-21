from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserAuthenticationForm
from .models import Commande 
def login_view(request):
    if request.method == "POST":
        form = UserAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # ou la page que tu veux
    else:
        form = UserAuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import requests
from django.conf import settings
from .models import product, Commande
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest

def index(request):
    item_name = request.GET.get('item-name')
    if item_name:
        product_object = product.objects.filter(title__icontains=item_name)
    else:
        product_object = product.objects.all()
    
    paginator = Paginator(product_object, 4)  # Paginer les résultats, 4 produits par page
    page = request.GET.get('page')
    product_object = paginator.get_page(page)
    
    return render(request, 'shop/index.html', {'product_object': product_object})

def detail(request, myid):
    product_object = product.objects.get(id=myid)
    return render(request, 'shop/detail.html', {'product': product_object})

@login_required(login_url='/login/')
def checkout(request):
    panier = request.session.get('panier', {})
    produits = product.objects.filter(id__in=panier.keys())
    panier_details = []
    total = 0
    for produit in produits:
        quantite = panier[str(produit.id)]
        total_ligne = produit.price * quantite
        panier_details.append({
            'produit': produit,
            'quantite': quantite,
            'total_ligne': total_ligne,
        })
        total += total_ligne
    if request.method == "POST":
        items = request.POST.get('items')
        total = request.POST.get('total')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        address = request.POST.get('address')
        ville = request.POST.get('ville')
        pays = request.POST.get('pays')
        zipcode = request.POST.get('zipcode')
        
        # Validation des données
        if not items or not total:
            return render(request, 'shop/checkout.html', {'error': 'Le panier est vide', 'panier': panier_details, 'total': total})
        
        try:
            total = float(total)
        except ValueError:
            return render(request, 'shop/checkout.html', {'error': 'Total invalide', 'panier': panier_details, 'total': total})
        
        if not all([nom, email, address, ville, pays, zipcode]):
            return render(request, 'shop/checkout.html', {'error': 'Tous les champs sont obligatoires', 'panier': panier_details, 'total': total})
        
        try:
            com = Commande(items=items, total=total, nom=nom, email=email, 
                         address=address, ville=ville, pays=pays, zipcode=zipcode)
            com.save()
            # Incrémenter le nombre de commandes de l'utilisateur connecté
            if request.user.is_authenticated:
                request.user.nombre_commandes += 1
                request.user.save()
            return redirect('confirmation')
        except Exception as e:
            return render(request, 'shop/checkout.html', {'error': str(e), 'panier': panier_details, 'total': total})

    return render(request, 'shop/checkout.html', {'panier': panier_details, 'total': total})

def confirmation(request):
    info = Commande.objects.all()[:1]
    for item in info:
        nom = item.nom
    return render(request, 'shop/confirmation.html', {'name': nom})


@login_required
def profil(request):
    return render(request, 'shop/profil.html', {'user': request.user})


@require_POST
def ajouter_au_panier(request, produit_id):
    panier = request.session.get('panier', {})
    panier[str(produit_id)] = panier.get(str(produit_id), 0) + 1
    request.session['panier'] = panier
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Retourne le nombre d'articles dans le panier
        panier_count = sum(panier.values())
        return JsonResponse({'success': True, 'panier_count': panier_count})
    return redirect('afficher_panier')

def decrementer_quantite(request, produit_id):
    panier = request.session.get('panier', {})
    if str(produit_id) in panier:
        if panier[str(produit_id)] > 1:
            panier[str(produit_id)] -= 1
        else:
            del panier[str(produit_id)]
        request.session['panier'] = panier
    return redirect('afficher_panier')

def incrementer_quantite(request, produit_id):
    panier = request.session.get('panier', {})
    if str(produit_id) in panier:
        panier[str(produit_id)] += 1
        request.session['panier'] = panier
    return redirect('afficher_panier')

def retirer_du_panier(request, produit_id):
    panier = request.session.get('panier', {})
    if str(produit_id) in panier:
        del panier[str(produit_id)]
        request.session['panier'] = panier
    return redirect('afficher_panier')

def afficher_panier(request):
    panier = request.session.get('panier', {})
    produits = product.objects.filter(id__in=panier.keys())
    panier_details = []
    total = 0
    for produit in produits:
        quantite = panier[str(produit.id)]
        total_ligne = produit.price * quantite
        panier_details.append({
            'produit': produit,
            'quantite': quantite,
            'total_ligne': total_ligne
        })
        total += total_ligne
    return render(request, 'shop/panier.html', {'panier': panier_details, 'total': total})


def get_paypal_access_token():
    url = f"{settings.PAYPAL_API_BASE}/v1/oauth2/token"
    response = requests.post(
        url,
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET),
        data={'grant_type': 'client_credentials'},
    )
    return response.json()['access_token']

@login_required(login_url='/login/')
def create_paypal_order(request):
    if request.method == "POST":
        total = request.POST.get('total')
        if not total:
            return HttpResponseBadRequest("Total manquant")
        access_token = get_paypal_access_token()
        url = f"{settings.PAYPAL_API_BASE}/v2/checkout/orders"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        data = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "amount": {
                    "currency_code": "EUR",
                    "value": str(total)
                }
            }],
            "application_context": {
                "return_url": request.build_absolute_uri('/paypal-success/'),
                "cancel_url": request.build_absolute_uri('/checkout/')
            }
        }
        response = requests.post(url, headers=headers, json=data)
        order = response.json()
        for link in order['links']:
            if link['rel'] == 'approve':
                return JsonResponse({'approval_url': link['href']})
        return HttpResponseBadRequest("Erreur PayPal")
    return HttpResponseBadRequest("Méthode non autorisée")

@login_required(login_url='/login/')
def paypal_success(request):
    order_id = request.GET.get('token')
    if not order_id:
        return HttpResponseBadRequest("Token manquant")
    access_token = get_paypal_access_token()
    url = f"{settings.PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.post(url, headers=headers)
    if response.status_code == 201:
        # Ici, tu peux enregistrer la commande dans ta base de données
        panier = request.session.get('panier', {})
        produits = product.objects.filter(id__in=panier.keys())
        total = 0
        items = []
        for produit in produits:
            quantite = panier[str(produit.id)]
            total_ligne = produit.price * quantite
            items.append(f"{produit.title} x{quantite}")
            total += total_ligne
        items_str = ", ".join(items)
        # Récupère les infos utilisateur si besoin
        nom = request.user.username if request.user.is_authenticated else "Invité"
        email = request.user.email if request.user.is_authenticated else ""
        # Adresse fictive ou à adapter selon ton modèle
        address = ""
        ville = ""
        pays = ""
        zipcode = ""
        com = Commande(
            items=items_str,
            total=total,
            nom=nom,
            email=email,
            address=address,
            ville=ville,
            pays=pays,
            zipcode=zipcode
        )
        com.save()
        # Incrémente le nombre de commandes de l'utilisateur connecté
        if request.user.is_authenticated:
            if hasattr(request.user, 'profile'):
                request.user.profile.nombre_commandes += 1
                request.user.profile.save()
            request.user.save()
        # Vide le panier après commande
        request.session['panier'] = {}
        return redirect('confirmation')
    return HttpResponseBadRequest("Paiement non validé")

from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    item_name = request.GET.get('item-name')
    if item_name:
        product_object = product.objects.filter(
            title__icontains=item_name
        )
    else:
        product_object = product.objects.all()
    
    paginator = Paginator(product_object, 4)  # Paginer les résultats, 4 produits par page
    page = request.GET.get('page')
    product_object = paginator.get_page(page)
    
    return render(request, 'shop/index.html', {'product_object': product_object})

