from django.db import models

# Create your models here.
class categoryDB(models.Model):
    Category_Name=models.CharField(max_length=100,null=True,blank=True)
    Description=models.CharField(max_length=100,null=True,blank=True)
    cat_profile=models.ImageField(upload_to="category",null=True,blank=True)
class productDB(models.Model):
    Category_name=models.CharField(max_length=100,null=True,blank=True)
    Product_name=models.CharField(max_length=100,null=True,blank=True)
    Description=models.CharField(max_length=100,null=True,blank=True)
    Price=models.IntegerField(null=True,blank=True)
    Product_image=models.ImageField(upload_to="Product",null=True,blank=True)
class serviceDB(models.Model):
    service_Name=models.CharField(max_length=100,null=True,blank=True)
    Description=models.CharField(max_length=100,null=True,blank=True)
    ser_profile=models.ImageField(upload_to="category",null=True,blank=True)