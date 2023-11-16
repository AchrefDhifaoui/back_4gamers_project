from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import date




class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return 'location'


class Game(models.Model):
    nom = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Games_pics/', null=True, blank=True)
    users = models.ManyToManyField('CustomUser', blank=True )

    def __str__(self):
        return self.nom
    
    


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,  default=False)
    pays = models.CharField(max_length=20)
    photo_profil = models.ImageField(
        upload_to='profile_pics/', null=True, blank=True)
    password = models.CharField(max_length=20, unique=True)
    location = models.OneToOneField(
        Location, on_delete=models.SET_NULL, null=True, blank=True)
    list_games = models.ManyToManyField(
        'Game', blank=True)
    first_name = models.CharField(max_length=30, default=False)
    last_name = models.CharField(max_length=30, default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    



class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        CustomUser, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender



class Categorie(models.Model):
    name = models.CharField(max_length=50)
    image =  models.ImageField(
        upload_to='categorie_pics/', null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class Produit(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    category = models.ForeignKey('Categorie', on_delete=models.PROTECT)
    picture = models.ImageField(upload_to="produit_pics/", null=True, blank=True)
    
    def __str__(self):
        return self.name

class Commande(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(Produit)
    date = models.DateField(default=date.today)