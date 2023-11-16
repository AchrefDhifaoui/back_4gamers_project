from rest_framework import serializers
from .models import *



class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['latitude', 'longitude']
        
        
        
class UsersSerializer(serializers.ModelSerializer):
    list_games = serializers.PrimaryKeyRelatedField(
        queryset=Game.objects.all(), many=True, required=False)
    location = LocationSerializer()

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'pays',
                  'password', 'location', 'list_games')
        
    def create(self, validated_data):
        location_data = validated_data.pop('location', None)
        user = super().create(validated_data)

        # If there is location data, create or update the location for the user
        if location_data:
            location_serializer = LocationSerializer(data=location_data)
            if location_serializer.is_valid():
                location = location_serializer.save()
                user.location = location
                user.save()
            else:
                raise serializers.ValidationError(location_serializer.errors)

        return user
    def update(self, instance, validated_data):
        location_data = validated_data.pop('location', None)

        # Update user fields
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.pays = validated_data.get('pays', instance.pays)
        instance.password = validated_data.get('password', instance.password)

        # If there is location data, create or update the location for the user
        if location_data:
            location_serializer = LocationSerializer(instance.location, data=location_data)
            if location_serializer.is_valid():
                location = location_serializer.save()
                instance.location = location
            else:
                raise serializers.ValidationError(location_serializer.errors)

        instance.save()
        return instance





class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = '__all__'


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'


class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'
