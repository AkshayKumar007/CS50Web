from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pizza(models.Model):
    pizza_type = models.CharField(primary_key=True, max_length=128)
    size = models.IntegerField()

class Topping(models.Model):
    top_name = models.CharField(primary_key=True, max_length=128)

class Subs(models.Model):
    class Meta:
        unique_together = (('sub_name', 'size', 'price'),)
    sub_name = models.CharField(primary_key=True, max_length=128)
    size = models.IntegerField()
    price = models.IntegerField()

class Pasta(models.Model):
    pasta_name = models.CharField(primary_key=True, max_length=128)
    price = models.IntegerField()

class Salads(models.Model):
    salad_name = models.CharField(primary_key=True, max_length=128)
    price = models.IntegerField()

class DinnerPlaters(models.Model):
    class Meta:
        unique_together = (('dinner_name', 'size', 'price'),)
    dinner_name = models.CharField(primary_key=True, max_length=128)
    size = models.IntegerField()
    price = models.IntegerField()

