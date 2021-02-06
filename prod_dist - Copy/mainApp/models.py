from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.
from django.db.models.query import QuerySet
from django.contrib.auth.backends import ModelBackend #BaseBackend

# Create your models here.
class CustomBackend(ModelBackend):
    def authenticate(self,request,username=None, password=None,usertype="None"):
        lookup_model=None
        if usertype=='retailer':
            lookup_model = Retailer
        elif usertype=='company':
            lookup_model = Company
        elif usertype=='distributor':
            lookup_model=Distributor
        
        try:
            o = lookup_model.objects.get(email=username)
            if o.check_password(raw_password=password)==True:
                return o
            else:
                return None 
        except lookup_model.DoesNotExist:            
            return None
        
        
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None




class City(models.Model):
    city = models.CharField(max_length=20,primary_key=True)
    state = models.CharField(max_length=20)

class Pincode(models.Model):
    pincode = models.CharField(max_length=20,primary_key=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE)

    class Meta:
        unique_together = unique_together = (('pincode', 'city'),)


class Address(models.Model):
    address = models.CharField(max_length=50,primary_key=True)
    pincode = models.ForeignKey(Pincode,on_delete=models.CASCADE)

class RetailerQuerySet(models.query.QuerySet):
    def get_queryset(self):
        return super().get_queryset().select_related('address__pincode').all()

    def update(self,first_name,last_name,mobile,
                        address,state,city,pincode,gst_number):
        obj = Retailer.objects.get(id=self[0].id)
        a = obj.address
        p = a.pincode
        c = p.city

        c.city = city
        c.state = state
        c.save()
        c = City.objects.get(city=city)


        p.pincode = pincode
        p.city = c
        p.save()

        p = Pincode.objects.get(pincode=pincode,city=c)
        a.address = address
        a.pincode = p
        a.save()
        
        a = Address.objects.get(address=address)
        obj.first_name = first_name
        obj.last_name = last_name
        obj.gst_number = gst_number
        obj.mobile = mobile
        obj.address=a

        obj.save()


class Retailer1Manager(BaseUserManager):
    def create_retailer(self,email,mobile,
                        address,state,city,pincode,first_name,
                        last_name=None,password=None,gst_number=''):
        if not email:
            raise ValueError('Users must have an email address')

        
        c,_ = City.objects.get_or_create(city=city,state=state)
        p,_ = Pincode.objects.get_or_create(pincode=pincode,city=c)
        a,_ = Address.objects.get_or_create(address=address,pincode=p)
        

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,            
            gst_number=gst_number,
            address=a
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def update(self, *args, **kwargs):
        # Some Business Logic

        # Call super to continue the flow -- from below line we are unable to invoke super
        print(args,kwargs)
        super().update(*args, **kwargs) 

    
    def get_queryset(self):
        # this is to use your custom queryset methods
        return RetailerQuerySet(self.model, using=self._db)

class Retailer(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    mobile = models.CharField(max_length=15)
    gst_number = models.CharField(max_length=50,unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    address = models.OneToOneField('Address',on_delete=models.CASCADE)
    objects = Retailer1Manager()

class DistributorQuerySet(models.query.QuerySet):
    def get_queryset(self):
        return super().get_queryset().select_related('address__pincode').all()

    def update(self,first_name,last_name,mobile,
                        address,state,city,pincode,gst_number):
        obj = Distributor.objects.get(id=self[0].id)
        a = obj.address
        p = a.pincode
        c = p.city

        c.city = city
        c.state = state
        c.save()
        c = City.objects.get(city=city)


        p.pincode = pincode
        p.city = c
        p.save()

        p = Pincode.objects.get(pincode=pincode,city=c)
        a.address = address
        a.pincode = p
        a.save()
        
        a = Address.objects.get(address=address)
        obj.first_name = first_name
        obj.last_name = last_name
        obj.gst_number = gst_number
        obj.mobile = mobile
        obj.address=a

        obj.save()


class Distributor1Manager(BaseUserManager):
    def create_distributor(self,email,mobile,
                        address,state,city,pincode,first_name,
                        last_name=None,password=None,gst_number=''):
        if not email:
            raise ValueError('Users must have an email address')

        c,_ = City.objects.get_or_create(city=city,state=state)
        p,_ = Pincode.objects.get_or_create(pincode=pincode,city=c)
        a,_ = Address.objects.get_or_create(address=address,pincode=p)

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,            
            gst_number=gst_number,
            address=a
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def update(self, *args, **kwargs):
        # Some Business Logic

        # Call super to continue the flow -- from below line we are unable to invoke super
        print(args,kwargs)
        super().update(*args, **kwargs) 
    
    def get_queryset(self):
        # this is to use your custom queryset methods
        return DistributorQuerySet(self.model, using=self._db)

class Distributor(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50,null=True,blank=True)
    mobile = models.CharField(max_length=15)
    gst_number = models.CharField(max_length=50,unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    address = models.OneToOneField('Address',on_delete=models.CASCADE)
    distributor_retailers = models.ManyToManyField(Retailer,db_table='distributes')
    objects = Distributor1Manager()

class CompanyQuerySet(models.query.QuerySet):
    def get_queryset(self):
        return super().get_queryset().select_related('address__pincode').all()

    def update(self,company_name,mobile,
                        address,state,city,pincode,gst_number):
        obj = Company.objects.get(company_name=company_name)
        a = obj.address
        p = a.pincode
        c = p.city

        c.city = city
        c.state = state
        c.save()
        c = City.objects.get(city=city)


        p.pincode = pincode
        p.city = c
        p.save()

        p = Pincode.objects.get(pincode=pincode,city=c)
        a.address = address
        a.pincode = p
        a.save()
        
        a = Address.objects.get(address=address)
        obj.company_name = company_name
        obj.gst_number = gst_number
        obj.mobile = mobile
        obj.address=a

        obj.save()



class Company1Manager(BaseUserManager):
    def create_company(self,email,company_name,mobile,
                        address,state,city,pincode,password,gst_number):
        if not email:
            raise ValueError('Users must have an email address')

        c,_ = City.objects.get_or_create(city=city,state=state)
        p,_ = Pincode.objects.get_or_create(pincode=pincode,city=c)
        a,_ = Address.objects.get_or_create(address=address,pincode=p)
        
        user = self.model(
            email=self.normalize_email(email),
            company_name=company_name,
            gst_number= gst_number,
            mobile=mobile,           
            address=a
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    

    def get_queryset(self):
        # this is to use your custom queryset methods
        return CompanyQuerySet(self.model, using=self._db)
        
       
    

class Company(AbstractBaseUser):
    company_name = models.CharField(max_length=20,unique=True)
    gst_number = models.CharField(max_length=20,unique=True)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    address = models.OneToOneField('Address',on_delete=models.CASCADE)
    objects = Company1Manager()
    company_distributors = models.ManyToManyField(Distributor,db_table='supplies')

    def get_full_name(self):
        # The user is identified by their email address
        return self.company_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.company_name

    def __str__(self):              # __unicode__ on Python 2
        return self.company_name

    def get_contact(self):
        return self.mobile

class CompanyProducts(models.Model):
    product_name = models.CharField(max_length=50)
    product_distributor_price = models.FloatField()
    product_distributor_margin = models.FloatField()
    product_retailer_price = models.FloatField()
    product_retailer_margin = models.FloatField()    
    product_mrp = models.FloatField()    
    product_discount = models.FloatField()
    product_company = models.ForeignKey(Company,on_delete=models.CASCADE)
    cg_gst = models.FloatField()
    sg_gst = models.FloatField()
    total_tax = models.FloatField()
    hsn_code = models.CharField(max_length=50,null=False,blank=False,default="")
    fssai_number = models.CharField(max_length=50,blank=True,null=True)

    def __str__(self):
        return self.product_name




