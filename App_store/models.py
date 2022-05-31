from tabnanny import verbose
from turtle import title
from django.db import models

# Create your models here.

class Category (models.Model):
    title = models.CharField(max_length=250,unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    class Meta:
        verbose_name_plural = "Categories"

class Product (models.Model):
    mainimage = models.ImageField(upload_to = "Products")
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=264, unique=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    preview_text = models.TextField(max_length=250, verbose_name="preview_text")
    details_text = models.TextField(max_length=250,verbose_name="description")
    price = models.FloatField()
    old_price = models.FloatField(default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    class Meta:
        ordering =['-created']
