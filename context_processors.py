def panier_count(request):
    panier = request.session.get('panier', {})
    return {'panier_count': sum(panier.values())}