def panier_count(request):
    panier = request.session.get('panier', {})
    count = sum(panier.values())
    return {'panier_count': count}