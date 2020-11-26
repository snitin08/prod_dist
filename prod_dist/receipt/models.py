from djongo import models
from django import forms

class Product(models.Model):
    _id = models.ObjectIdField()
    product_name = models.CharField(max_length=50)
    product_price = models.FloatField()

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'product_name', 'product_price'
        )

class Receipt(models.Model):
    name = models.CharField(max_length=100)
    # products = models.ArrayField(
    #     model_container=Product,
    #     model_form_class=ProductForm,        
    # )

# Create your models here.

