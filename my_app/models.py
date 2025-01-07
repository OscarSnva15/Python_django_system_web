from django.db import models

# Create your models here.
# los modelos sireven para crear tablas provienentes de una base de datos 
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    public = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField()
