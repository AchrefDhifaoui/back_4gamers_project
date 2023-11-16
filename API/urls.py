
from django.urls import path
from . import views

urlpatterns = [
    # ----------------------------------------User CRUD Link--------------------------------------------
    path('users/', views.allUsers),
    path('user/<int:id>/', views.getUser),
    path('addUsers/', views.addUsers),
    path('updateUser/<int:id>/', views.updateUser),
    path('deleteUser/<int:id>/', views.deleteUser),
    path('closestUsers/<str:game_name>/<str:my_latitude>/<str:my_longitude>/',
         views.get_closest_users_for_game),

    # ----------------------------------------Location CRUD Link--------------------------------------------
    path('locations/', views.allLocations),
    path('location/<int:id>/', views.getLocation),
    path('addLocations/', views.addLocation),
    path('updateLocation/<int:id>/', views.updateLocation),
    path('deleteLocation/<int:id>/', views.deleteLocation),




    # ----------------------------------------Game CRUD Link--------------------------------------------
    path('games/', views.allGames),
    path('game/<int:id>/', views.getGame),
    path('addGame/', views.addGame),
    path('updateGame/<int:id>/', views.updateGame),
    path('deleteGame/<int:id>/', views.deleteGame),

    # ----------------------------------------Message CRUD Link--------------------------------------------
    path('messages/', views.allMessages),
    path('message/<int:id>/', views.getMessage),
    path('addMessage/', views.addMessage),
    path('updateMessage/<int:id>/', views.updateMessage),
    path('deleteMessage/<int:id>/', views.deleteMessage),


    # ----------------------------------------Produit CRUD Link--------------------------------------------
    path('produits/', views.allProduits),
    path('produit/<int:id>/', views.getProduit),
    path('addProduit/', views.addProduit),
    path('updateProduit/<int:id>/', views.updateProduit),
    path('deleteProduit/<int:id>/', views.deleteProduit),




    # ----------------------------------------Categorie CRUD Link--------------------------------------------
    path('categories/', views.allCategories),
    path('categorie/<int:id>/', views.getCategorie),
    path('addCategorie/', views.addCategorie),
    path('updateCategorie/<int:id>/', views.updateCategorie),
    path('deleteCategorie/<int:id>/', views.deleteCategorie),





    # ----------------------------------------Commande CRUD Link--------------------------------------------
    path('commandes/', views.allCommandes),
    path('commande/<int:id>/', views.getCommande),
    path('addCommande/', views.addCommande),
    path('updateCommande/<int:id>/', views.updateCommande),
    path('deleteCommande/<int:id>/', views.deleteCommande),





]
