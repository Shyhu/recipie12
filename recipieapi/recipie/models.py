from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Recipe(models.Model):
    title=models.CharField(max_length=255)
    cuisine=models.CharField(max_length=100)
    meal_type=models.CharField(max_length=100)
    ingredients=models.TextField()

    def __str__(self):
        return self.title

class Review(models.Model):
    recipe=models.ForeignKey(Recipe,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review=models.TextField()
    ratings=models.IntegerField()
    def __str__(self):
        return self.review