from django.db import models

# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_added']
    def __str__(self):
        return self.name

class product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop/images',null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)     
    
    class Meta:
        ordering = ['-date_added']
    def __str__(self):
        return self.title 
    

class Commande(models.Model):
    items=  models.CharField(max_length=200)
    total = models.FloatField(max_length=200)
    nom = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    pays = models.CharField(max_length=600)
    zipcode = models.CharField(max_length=300)
    date_commande = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_commande']    


    def __str__(self):
        return self.nom     