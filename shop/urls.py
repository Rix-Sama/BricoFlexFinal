from django.urls import path
from .views import index, detail, checkout, confirmation, profil, ajouter_au_panier, retirer_du_panier, afficher_panier
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, decrementer_quantite, incrementer_quantite  # Add incrementer_quantite import

urlpatterns = [
    path('', index, name='home'),
    path('<int:myid>/', detail, name='detail'),
    path('checkout/', checkout, name='checkout'),
    path('confirmation/', confirmation, name='confirmation'),
    path('profil/', profil, name='profil'),
    path('ajouter-au-panier/<int:produit_id>/', ajouter_au_panier, name='ajouter_au_panier'),
    path('retirer-du-panier/<int:produit_id>/', retirer_du_panier, name='retirer_du_panier'),
    path('panier/', afficher_panier, name='afficher_panier'),
    path('create-paypal-order/', views.create_paypal_order, name='create_paypal_order'),
    path('paypal-success/', views.paypal_success, name='paypal_success'),
    path('login/', login_view, name='login'),
    path('decrementer-quantite/<int:produit_id>/', decrementer_quantite, name='decrementer_quantite'),
    path('incrementer-quantite/<int:produit_id>/', incrementer_quantite, name='incrementer_quantite'),
   
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)