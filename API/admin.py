from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Location)
admin.site.register(Game)
admin.site.register(CustomUser)
admin.site.register(Message)
admin.site.register(Produit)
admin.site.register(Categorie)
admin.site.register(Commande)

