from .forms import ClientCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = ClientCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_client = True
            user.save()
            messages.success(request, 'Votre compte client a été créé ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = ClientCreationForm()
    return render(request, 'shop/register.html', {'form': form})