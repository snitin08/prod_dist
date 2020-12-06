from faker import Faker
from .models import *

from random import randint
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return str(randint(range_start, range_end))

fake = Faker(['en-IN'])
Faker.seed(0)
def createCompany(no_of_companies=5):

    for i in range(no_of_companies):
        data = {
            "email":fake.email(),
            "password":fake.password(),
            "company":fake.company(),
            "mobile":random_with_N_digits(10),
            "address": fake.address(),
            "state":fake['en_IN'].state(),
            "city":fake.city(),
            "pincode":fake['en_IN'].zipcode(),
        }
        
        print(data)

        company = Company.objects.create_company(
            email=data["email"],
            company_name=data["company"],
            mobile=data["mobile"],
            address=data["address"],
            state=data["state"],
            city=data['city'],
            pincode=data["pincode"],
            password=data["password"],
        )

def createDistributor(no_of_distributors=5):
    for i in range(no_of_distributors):
        data = {
            "email":fake.email(),
            "password":fake.password(),
            "first_name":fake.first_name(),
            "last_name":fake.last_name(),
            "mobile":random_with_N_digits(10),
            "address": fake.address(),
            "state":fake['en_IN'].state(),
            "city":fake.city(),
            "pincode":fake['en_IN'].zipcode(),
        }

        distributor = Distributor.objects.create_distributor(        
            email=data["email"],            
            mobile=data["mobile"],
            address=data["address"],
            state=data["state"],
            city=data['city'],
            pincode=data["pincode"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["password"],
        )
        
        print(data)

def createRetailer(no_of_retailers=5):
    for i in range(no_of_retailers):
        data = {
            "email":fake.email(),
            "password":fake.password(),
            "first_name":fake.first_name(),
            "last_name":fake.last_name(),
            "mobile":random_with_N_digits(10),
            "address": fake.address(),
            "state":fake['en_IN'].state(),
            "city":fake.city(),
            "pincode":fake['en_IN'].zipcode(),
        }

        distributor = Retailer.objects.create_retailer(        
            email=data["email"],            
            mobile=data["mobile"],
            address=data["address"],
            state=data["state"],
            city=data['city'],
            pincode=data["pincode"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["password"],
        )
        
        print(data)
