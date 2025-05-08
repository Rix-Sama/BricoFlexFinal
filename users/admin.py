from django.contrib import admin
from .models import Admin, Client

class AdminAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'telephone', 'date_inscription', 'date_connexion', 'is_active')
    search_fields = ('email', 'username', 'telephone')
    list_filter = ('is_active', 'date_inscription')
    readonly_fields = ('date_inscription', 'date_connexion')

admin.site.register(Admin, AdminAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'telephone', 'ville', 'pays', 'date_inscription', 'is_active')
    search_fields = ('email', 'username', 'telephone', 'ville')
    list_filter = ('is_active', 'ville', 'pays', 'date_inscription')
    readonly_fields = ('date_inscription', 'date_connexion')

admin.site.register(Client, ClientAdmin)
from .models import Admin, Client
