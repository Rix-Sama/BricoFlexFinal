from .forms import UserCreationFormCustom
from django.contrib import messages
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationFormCustom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Votre compte a été créé ! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserCreationFormCustom()
    return render(request, 'shop/register.html', {'form': form})