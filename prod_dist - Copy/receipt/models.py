from django.db import models
# Create your models here.
from mongoengine import *
import datetime


class Products(EmbeddedDocument):    
    prod_name = StringField(max_length=200)
    price = DecimalField(min_value=0, max_value=1000000.00, precision=2, rounding='ROUND_HALF_UP')
    tax = DecimalField(min_value=0, max_value=1000000.00, precision=2, rounding='ROUND_HALF_UP', null=True, blank=True)
    discount = DecimalField(min_value=0, max_value=1000000.00, precision=2, rounding='ROUND_HALF_UP', null=True, blank=True)
    quantity = IntField(required=True)
    defective = IntField(default=0)



class Receipt(Document):
    #receipt_id = IntField(required=True, primary_key = True)
    from_id = IntField()
    to_id = IntField()
    from_type = StringField(max_length=50)
    to_type = StringField(max_length=50)
    from_name =  StringField(max_length=200)
    to_name = StringField(max_length=200)
    from_address = StringField(max_length=500)
    to_address = StringField(max_length=500)
    products = ListField(EmbeddedDocumentField(Products))
    sub_total = DecimalField(min_value=0, max_value=1000000.00, precision=2, rounding='ROUND_HALF_UP')
    taxes = DecimalField(min_value=0, max_value=100.00, precision=2, rounding='ROUND_HALF_UP')
    discount = DecimalField(min_value=0, max_value=100.00, precision=2, rounding='ROUND_HALF_UP')
    total = DecimalField(min_value=0, max_value=1000000.00, precision=2, rounding='ROUND_HALF_UP')
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    year = IntField(default=datetime.datetime.utcnow().year)
    month = IntField(default=datetime.datetime.utcnow().month)
    day = IntField(default=datetime.datetime.utcnow().day)
    requested = BooleanField(default=False)
    defective = BooleanField(default=False)
    status = StringField(max_length=50,default="pending")
    comments = StringField(max_length=500,default="")
    

# p1 = Products(prod_id = 1, prod_name = 'shamshampoo', price = 449.45, quantity = 5)
# r1 = Receipt( from_name = 'abc', to_name = 'def', from_address = '123adf', to_address = '2edfb', products = [p1], sub_total = 5000.00, taxes = 0.00, discount =  0.00, total = 5000.00)
# r1.save()
