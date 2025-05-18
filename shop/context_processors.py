from .models import category

def panier_count(request):
    panier = request.session.get('panier', {})
    count = sum(panier.values())
    return {'panier_count': count}

def categories_list(request):
    return {'categories': category.objects.all()}