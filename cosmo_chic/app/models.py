from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    category = models.TextField()

class product(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    pid = models.TextField(unique=True)
    name = models.TextField()
    dis = models.TextField()
    img = models.FileField()

class Details(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    price = models.IntegerField()
    offer_price = models.IntegerField()
    stock = models.IntegerField()
    weight = models.TextField()

class Otp(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp=models.TextField()
    
class Cart(models.Model):
    details=models.ForeignKey(Details,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()

class Buy(models.Model):
    details=models.ForeignKey(Details,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    t_price=models.IntegerField()
    date=models.DateField(auto_now_add=True)

