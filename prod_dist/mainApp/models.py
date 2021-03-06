from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
# Create your models here.
from django.contrib.auth.backends import ModelBackend #BaseBackend

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




class RetailerManager(BaseUserManager):
    def create_retailer(self,email,mobile,
                        address,state,city,pincode,
                        first_name,last_name=None,password=None,gst_number=''):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            address=address,
            state=state,
            city=city,
            pincode=pincode,
            gst_number=gst_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class Retailer(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100,blank=False,null=False)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    mobile = models.CharField(max_length=15)
    address = models.TextField(max_length=500)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    gst_number = models.CharField(max_length=50,unique=True,default="")
    
    objects = RetailerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','mobile','address','state','city','pincode'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name+" "+self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.first_name

    def get_contact(self):
        return self.mobile


class DistributorManager(BaseUserManager):
    def create_distributor(self,email,mobile,
                        address,state,city,pincode,first_name,
                        last_name=None,password=None,gst_number=''):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            address=address,
            state=state,
            city=city,
            pincode=pincode,
            gst_number=gst_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class Distributor(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100,blank=False,null=False)
    last_name = models.CharField(max_length=100,blank=True,null=True)
    mobile = models.CharField(max_length=15)
    address = models.TextField(max_length=500)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    gst_number = models.CharField(max_length=50,unique=True,default="")
    distributor_retailers = models.ManyToManyField(Retailer,db_table='distributes')
    
    objects = DistributorManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','mobile','address','state','city','pincode'] # Email & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name+" "+self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    #def __str__(self):              # __unicode__ on Python 2
    #    return self.first_name

    def get_contact(self):
        return self.mobile

class CompanyManager(BaseUserManager):
    def create_company(self,email,company_name,mobile,
                        address,state,city,pincode,password,gst_number):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            company_name=company_name,
            mobile=mobile,
            address=address,
            state=state,
            city=city,
            pincode=pincode,
            gst_number=gst_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class Company(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255,unique=True,error_messages={'unique':'This field should be unique'})
    mobile = models.CharField(max_length=15)
    address = models.TextField(max_length=500)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    company_distributors = models.ManyToManyField(Distributor,db_table='supplies')
    gst_number = models.CharField(max_length=50,unique=True,default="")
    objects = CompanyManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name','mobile','address','state','city','pincode'] # Email & Password are required by default.

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

class Company1Manager(BaseUserManager):
    def create_company(self,email,company_name,mobile,
                        address,state,city,pincode,password):
        if not email:
            raise ValueError('Users must have an email address')

        c,_ = City.objects.get_or_create(city=city,state=state)
        p,_ = Pincode.objects.get_or_create(pincode=pincode,city=c)
        a,_ = Address.objects.get_or_create(address=address,pincode=p)
        
        user = self.model(
            email=self.normalize_email(email),
            company_name=company_name,            
            address=a
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def get_queryset(self):
        return super().get_queryset().select_related('address__pincode').all()
    





class City(models.Model):
    city = models.CharField(max_length=20,primary_key=True)
    state = models.CharField(max_length=20)

class Pincode(models.Model):
    pincode = models.CharField(max_length=20,primary_key=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE)


class Address(models.Model):
    address = models.CharField(max_length=50,primary_key=True)
    pincode = models.ForeignKey(Pincode,on_delete=models.CASCADE)

class Company1(AbstractBaseUser):
    company_name = models.CharField(max_length=20,unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    address = models.OneToOneField('Address',on_delete=models.CASCADE)
    objects = Company1Manager()