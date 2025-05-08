from django.shortcuts import redirect
from django.contrib import messages

def login_required_message(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Veuillez vous connecter pour accéder au panier')
            return redirect('login')
        return function(request, *args, **kwargs)
    return wrap