from django.db import models

# Create your models here.
from mongoengine import *

class Products(EmbeddedDocument):
    prod_id = IntField(required=True, primary_key = True)
    prod_name = StringField(max_length=200)
    price = DecimalField(min_value=0, max_value=1000000.00, precision=2, rounding='ROUND_HALF_UP')
    quantity = IntField(required=True)



class Receipt(Document):
    receipt_id = IntField(required=True, primary_key = True)
    from_name =  StringField(max_length=200)
    to_name = StringField(max_length=200)
    from_address = StringField(max_length=200)
    to_address = StringField(max_length=200)
    products = ListField(EmbeddedDocumentField(Products))
    sub_total = DecimalField(min_value=0, max_value=1000000.00, precision=2, rounding='ROUND_HALF_UP')
    taxes = DecimalField(min_value=0, max_value=100.00, precision=2, rounding='ROUND_HALF_UP')
    discount = DecimalField(min_value=0, max_value=100.00, precision=2, rounding='ROUND_HALF_UP')
    total = DecimalField(min_value=0, max_value=1000000.00, precision=2, rounding='ROUND_HALF_UP')

p1 = Products(prod_id = 1, prod_name = 'shamshampoo', price = 449.45, quantity = 5)
r1 = Receipt(receipt_id = 123, from_name = 'abc', to_name = 'def', from_address = '123adf', to_address = '2edfb', products = [p1], sub_total = 5000.00, taxes = 0.00, discount =  0.00, total = 5000.00)
r1.save()