


from django.forms import ValidationError
from django.http import JsonResponse
from pyautogui import Point
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Func
from geopy.distance import geodesic
from math import radians, sin, cos, sqrt, atan2
from django.http import JsonResponse

class Sqrt(Func):
    function = 'SQRT'

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of Earth in kilometers (change this if you want miles)
    radius = 6371.0

    # Calculate the distance
    distance = radius * c

    return distance

@api_view(['GET'])
def get_closest_users_for_game(request, game_name, my_latitude, my_longitude):
    try:
        # Convert coordinates to floats
        my_latitude, my_longitude = float(my_latitude), float(my_longitude)

        # Get the user's location as a Point object
        my_location = Point(my_longitude, my_latitude)

        # Get all users who play the specified game
        users = CustomUser.objects.filter(list_games__nom=game_name)

        # Calculate distances and create a list of users with distances
        users_with_distances = [
            {"user": user, "distance": geodesic((my_latitude, my_longitude), (user.location.latitude, user.location.longitude)).kilometers}
            for user in users
        ]

        # Sort users by distance
        sorted_users = sorted(users_with_distances, key=lambda x: x["distance"])

        # Serialize user data
        serializer = UsersSerializer([entry["user"] for entry in sorted_users], many=True)

        return JsonResponse(serializer.data, safe=False)

    except (ValueError, TypeError, ValidationError):
        return JsonResponse({"error": "Invalid coordinates provided."}, status=400)


# ----------------------------------------User CRUD--------------------------------------------


@api_view(['GET'])
def allUsers(request):
    users = CustomUser.objects.all()
    serialisation = UsersSerializer(users, many=True)
    return Response(serialisation.data)


@api_view(['GET'])
def getUser(request, id):
    user = CustomUser.objects.get(id=id)
    serializer = UsersSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def addUsers(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Update list_users field in each related Game
        for game in user.list_games.all():
            game.users.add(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def updateUser(request, id):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UsersSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteUser(request, id):
    try:
        user = CustomUser.objects.get(id=id)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    for game in user.list_games.all():
        game.users.remove(user)
    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ----------------------------------------Location CRUD--------------------------------------------

@api_view(['GET'])
def allLocations(request):
    locations = Location.objects.all()
    serialisation = LocationSerializer(locations, many=True)
    return Response(serialisation.data)


@api_view(['GET'])
def getLocation(request, id):
    location = Location.objects.get(id=id)
    serializer = LocationSerializer(location)
    return Response(serializer.data)


@api_view(['POST'])
def addLocation(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateLocation(request, id):
    try:
        location = Location.objects.get(id=id)
    except Location.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = LocationSerializer(location, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteLocation(request, id):
    try:
        location = Location.objects.get(id=id)
    except Location.DoesNotExist:
        return Response({"error": "Location not found"}, status=status.HTTP_404_NOT_FOUND)

    location.delete()
    return Response({"message": "location deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ----------------------------------------Game CRUD--------------------------------------------


@api_view(['GET'])
def allGames(request):
    games = Game.objects.all()
    serialisation = GameSerializer(games, many=True)
    return Response(serialisation.data)


@api_view(['GET'])
def getGame(request, id):
    game = Game.objects.get(id=id)
    serializer = GameSerializer(game)
    return Response(serializer.data)


@api_view(['POST'])
def addGame(request):
    serializer = GameSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateGame(request, id):
    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        return Response({"error": "game not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = GameSerializer(game, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteGame(request, id):
    try:
        game = Game.objects.get(id=id)
    except Game.DoesNotExist:
        return Response({"error": "game not found"}, status=status.HTTP_404_NOT_FOUND)
    game.users.clear()

    game.delete()
    return Response({"message": "game deleted successfully"}, status=status.HTTP_204_NO_CONTENT)








# ----------------------------------------Message CRUD--------------------------------------------


@api_view(['GET'])
def allMessages(request):
    messages = Message.objects.all()
    serialisation = MessageSerializer(messages, many=True)
    return Response(serialisation.data)


@api_view(['GET'])
def getMessage(request, id):
    message = Message.objects.get(id=id)
    serializer = MessageSerializer(message)
    return Response(serializer.data)


@api_view(['POST'])
def addMessage(request):
    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateMessage(request, id):
    try:
        message = Message.objects.get(id=id)
    except Message.DoesNotExist:
        return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = MessageSerializer(message, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteMessage(request, id):
    try:
        message = Message.objects.get(id=id)
    except Message.DoesNotExist:
        return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

    message.delete()
    return Response({"message": "Message deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# ----------------------------------------Produit CRUD--------------------------------------------*

@api_view(['GET'])
def allProduits(request):
    produits = Produit.objects.all()
    serialisation = ProduitSerializer(produits, many=True)
    return Response(serialisation.data)


@api_view(['GET'])
def getProduit(request, id):
    produit = Produit.objects.get(id=id)
    serializer = ProduitSerializer(produit)
    return Response(serializer.data)


@api_view(['POST'])
def addProduit(request):
    serializer = ProduitSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateProduit(request, id):
    try:
        produit = Produit.objects.get(id=id)
    except Produit.DoesNotExist:
        return Response({"error": "produit not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProduitSerializer(produit, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteProduit(request, id):
    try:
        produit = Produit.objects.get(id=id)
    except Produit.DoesNotExist:
        return Response({"error": "produit not found"}, status=status.HTTP_404_NOT_FOUND)

    produit.delete()
    return Response({"message": "produit deleted successfully"}, status=status.HTTP_204_NO_CONTENT)




# ----------------------------------------Categorie CRUD--------------------------------------------*
@api_view(['GET'])
def allCategories(request):
    categories = Categorie.objects.all()
    serialisation = CategorieSerializer(categories, many=True)
    return Response(serialisation.data)


@api_view(['GET'])
def getCategorie(request, id):
    categorie = Categorie.objects.get(id=id)
    serializer = CategorieSerializer(categorie)
    return Response(serializer.data)


@api_view(['POST'])
def addCategorie(request):
    serializer = CategorieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateCategorie(request, id):
    try:
        categorie = Categorie.objects.get(id=id)
    except Categorie.DoesNotExist:
        return Response({"error": "categorie not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CategorieSerializer(categorie, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteCategorie(request, id):
    try:
        categorie = Categorie.objects.get(id=id)
    except Categorie.DoesNotExist:
        return Response({"error": "categorie not found"}, status=status.HTTP_404_NOT_FOUND)

    categorie.delete()
    return Response({"message": "categorie deleted successfully"}, status=status.HTTP_204_NO_CONTENT)





# ----------------------------------------Commande CRUD--------------------------------------------*
@api_view(['GET'])
def allCommandes(request):
    commandes = Commande.objects.all()
    serialisation = CommandeSerializer(commandes, many=True)
    return Response(serialisation.data)


@api_view(['GET'])
def getCommande(request, id):
    commande = Commande.objects.get(id=id)
    serializer = CommandeSerializer(commande)
    return Response(serializer.data)


@api_view(['POST'])
def addCommande(request):
    serializer = CommandeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def updateCommande(request, id):
    try:
        commande = Commande.objects.get(id=id)
    except Commande.DoesNotExist:
        return Response({"error": "commande not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommandeSerializer(commande, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def deleteCommande(request, id):
    try:
        commande = Commande.objects.get(id=id)
    except Commande.DoesNotExist:
        return Response({"error": "commande not found"}, status=status.HTTP_404_NOT_FOUND)

    commande.delete()
    return Response({"message": "commande deleted successfully"}, status=status.HTTP_204_NO_CONTENT)





