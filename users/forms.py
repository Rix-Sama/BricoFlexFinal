from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Admin, Client

class AdminCreationForm(UserCreationForm):
    class Meta:
        model = Admin
        fields = ('email', 'username', 'telephone')  # adapte selon ton modèle

class ClientCreationForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ('email', 'username', 'telephone', 'adresse', 'ville', 'pays', 'code_postal')