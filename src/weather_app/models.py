from django.db import models

# Create your models here.

class City(models.Model):
    """
    city model to store the city details
    """
    city_name = models.CharField(max_length=100, unique=True)
