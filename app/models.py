from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name=models.CharField(max_length=200)
    image=models.FileField(upload_to='products/images')
    def __str__(self):
        return self.name
    
class Catcategory(models.Model):   
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    categoryname=models.CharField(max_length=200)
    def __str__(self):
        return self.categoryname

# Create your models here.
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    catcategory=models.ForeignKey(Catcategory,on_delete=models.CASCADE)

    name=models.CharField(max_length=200)
    rate=models.IntegerField()
    image=models.FileField(upload_to='products/images')
    image2=models.FileField(upload_to='products/images')
    description=models.TextField()
    fabric=models.TextField(default=1)
    origin=models.TextField(default=1)
    fittype=models.TextField(default=1)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    rate=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total=models.DecimalField(max_digits=10, decimal_places=2, default=0)
class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.TextField()