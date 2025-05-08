from django.contrib import admin
from .models import category, product , Commande




# Register your models here.
admin.site.site_header= 'E-commerce'
admin.site.site_title= 'Gestion BricoFlax'
admin.site.index_title= 'Manager'



class adminCategory(admin.ModelAdmin):
    list_display = ('name', 'date_added')

class adminProduct(admin.ModelAdmin):
    list_display = ('title', 'price', 'description', 'category', 'date_added')
    search_fields = ('title',)
    list_editable= ('price',)


class adminCommande(admin.ModelAdmin):
    list_display=('items', 'nom', 'email', 'address', 'ville', 'pays','total', 'zipcode', 'date_commande')


admin.site.register(category, adminCategory)
admin.site.register(product, adminProduct)
admin.site.register(Commande, adminCommande)

