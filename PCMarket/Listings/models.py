from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager

class CurrentListing(models.Model):
    part_type = models.CharField(max_length=10) 
    model_name = models.CharField(max_length=100)
    price = models.CharField(max_length=6)
    attrs = models.JSONField(default=dict)

class SoldListing(models.Model):
    part_type = models.CharField(max_length=10) 
    model_name = models.CharField(max_length=100)
    price = models.CharField(max_length=6)
    attrs = models.JSONField(default=dict)
    
class FollowedListing(models.Model):
    part_type = models.CharField(max_length=10) 
    model_name = models.CharField(max_length=100)
    price = models.CharField(max_length=6)
    attrs = models.JSONField(default=dict)

class User(AbstractBaseUser):
    email = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    current_listings = models.ManyToManyField(CurrentListing)
    sold_listings = models.ManyToManyField(SoldListing, related_name="sold_listings", db_column="sold_listings")
    purchases = models.ManyToManyField(SoldListing, related_name="purchases", db_column="purchases")
    followings = models.ManyToManyField(FollowedListing)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []