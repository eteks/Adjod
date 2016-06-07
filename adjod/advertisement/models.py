from django.contrib.auth.models import *
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from haystack.query import SearchQuerySet
from datetime import timedelta
import datetime
from adjod.models import *

from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import payment_was_successful
from django.conf import settings
from django.core.validators import RegexValidator

TYPE = (
    ('buy', 'I Want to Buy'),
    ('sell', 'I Want to Sell'),
)

CONDITION = (
    ('used', 'Used'),
    ('new', 'New'),
)
SUBSCRIPTION_TYPE = (
    ('account_subscription', 'Account Subscription'),
    ('urgent_subscription', 'Urgent Subscription'),
    ('top_subscription', 'Top Subscription'),
    ('urgent_top_subscription', 'Urgent and Top Subscription'),
)


YOU=( ('individual','Individual'),('dealer','Dealer'))



class Category(models.Model):
    icon = models.ImageField(upload_to='icons', blank=True, verbose_name='Icon image',help_text='Please make sure image should be jpeg or png with 70 x 70 size (optional)')
    name = models.CharField(max_length=250,help_text='Enter Category Name',unique=True)
    category_type = models.CharField(max_length=250,help_text='Enter multiple category types separated with comma')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['id']

class SubCategory(models.Model):
    category = models.ForeignKey(Category,help_text='Choose any one of the Categories')
    name = models.CharField(max_length=50,help_text='Enter Subcategory name',verbose_name='Subcategory')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"
        unique_together = (("category", "name"),)
        ordering = ['id']

class Dropdown(models.Model):
    subcat=models.ManyToManyField(SubCategory,verbose_name='Subcategory')
    brand_name=models.CharField(max_length=50, default='',verbose_name='Brand name',help_text='Enter Brand name')

    def get_subcat(self):
            return self.brand_name.all()

    def __unicode__(self):
        return self.brand_name

    class Meta:
        verbose_name = "Subcategory Related field"
        verbose_name_plural = "Subcategory Related fields"
        ordering = ['id']

class City(models.Model):
    city=models.CharField(max_length=50,help_text='Enter City name (First letter caps)')
    country_code=models.CharField(max_length=10,help_text="Enter Country ISO code (First two letters with Capital letters).Please refer as <a href='https://countrycode.org/'>https://countrycode.org/</a>")
    country_name=models.CharField(max_length=50,help_text='Enter Country name (First letter caps)')

    def __unicode__(self):
        return self.city

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        unique_together = (("city", "country_code","country_name"),)
        ordering = ['id']

class Locality(models.Model):
    city_refid=models.ForeignKey(City,null=True,verbose_name='City name',help_text='Choose city')
    locality=models.CharField(max_length=50,verbose_name='locality',help_text='Enter locality')
    def __unicode__(self):
        return self.locality

    class Meta:
        verbose_name = "Locality"
        verbose_name_plural = "Localities"
        unique_together = (("city_refid", "locality"),)
        ordering = ['id']

class PremiumPriceInfo(models.Model):
    premium_price = models.DecimalField(max_digits=20, decimal_places=2, default=0.0,help_text='Enter amount with two decimal point in base currency')
    base_currency = models.CharField( blank=True,
                    max_length=6)
    purpose= models.CharField(max_length=30, choices=SUBSCRIPTION_TYPE,help_text='Choose Subscription option')
    duration=models.BigIntegerField(
        null=True, blank=True, help_text="No of days allowed")
    def __unicode__(self):
        return self.purpose

    def save(self, force_insert=False, force_update=False):
        from adjod.models import BaseCurrency
        base = BaseCurrency.objects.latest('id')
        self.base_currency = base.base_currency
        super(PremiumPriceInfo, self).save(force_insert, force_update)



    class Meta:
        unique_together = (("premium_price", "purpose"),)
        ordering = ['id']

class Product(models.Model):
    userprofile=models.ForeignKey(UserProfile, null=True, blank=True,help_text='Choose user name',verbose_name='User')
    category = models.ForeignKey(Category, null=False,help_text='Choose Category of the product',verbose_name='Category')
    subcategory =models.ForeignKey(SubCategory,null=False,help_text='Choose Subcategory',verbose_name='Subcategory')
    adtype= models.CharField(max_length=10, choices=TYPE, null=False,help_text='Choose what type ad',verbose_name='Type of AD')
    title = models.CharField(max_length=250, null=False,help_text='Choose what type ad',verbose_name='Title of Product')
    photos = models.ImageField(upload_to='products', blank=True, null=True, max_length=500,help_text='Upload images jpeg and png format(2mb)',verbose_name='Photos for your ad')
    thumbnail = models.ImageField(upload_to="product_thumbs", null=True, editable=False, max_length=500,help_text='Upload thumbnail images jpeg and png format(2mb)',verbose_name='Thumbnail for your ad')
    imagecount=models.IntegerField(null=True, blank=True,help_text='Mention how many image uploaded',verbose_name='Number of images')
    video=models.FileField(upload_to='videos',null=True, blank=True,help_text='If you have video about your ad please upload it',verbose_name='Videos for your ad')
    condition = models.CharField(max_length=10,choices=CONDITION, default="used",help_text='Choose condition of your product',verbose_name='Condition')
    price = models.FloatField(null=True, default=0.0,help_text='Mention maximum selling price',verbose_name='Price')
    ad_brand=models.ForeignKey(Dropdown, blank=True, null=True, related_name="ad_brand",help_text='Choose brand name',verbose_name='Brand')
    ad_year=models.CharField(max_length=10, blank=True,null=True,help_text='Year of the product',verbose_name='Product Year')
    city=models.ForeignKey(City, null=False,help_text='Choose your city',verbose_name='City')
    locality=models.ForeignKey(Locality, null=False,help_text='Choose your Locality',verbose_name='Locality')
    country_code=models.CharField(max_length=10,help_text="Enter Country ISO code (First two letters with Capital letters).Please refer as <a href='https://countrycode.org/'>https://countrycode.org/</a>",verbose_name='Country code')
    description = models.TextField(max_length=100, verbose_name="Description", null=False,help_text='Description about your product')
    you_are = models.CharField(max_length=20,choices=YOU,default='individual', null=False,help_text='Choose ad creaded user status',verbose_name='User Type')
    you_name = models.CharField(max_length=20, null=True,help_text='Enter ad creater name',verbose_name='Name')
    you_email = models.EmailField(max_length=30, null=False,help_text='Enter ad creater email',verbose_name='Email')
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # you_phone = models.CharField(validators=[phone_regex],max_length=15,blank=True, null=True,help_text='Enter ad creater phone number or mobile number',verbose_name='Contact number')
    you_phone = models.CharField(max_length=8,blank=True, null=True,help_text='Enter ad creater phone number or mobile number',verbose_name='Contact number')
    created_date =models.DateTimeField(default=datetime.datetime.now)
    modified_date =models.DateField(default=datetime.datetime.now)
    isregistered_user=models.BooleanField(default=False)
    ispremium=models.BooleanField(default=False)
    premium_plan=models.ForeignKey(PremiumPriceInfo, null=True, blank=True)
    expired_date=models.DateField(null=True,blank=True)
    status_isactive=models.BooleanField(default=False,verbose_name='Product Status')
    post_term_status=models.BooleanField(default=False)
    class Admin:
        pass
    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        self.city = City.objects.get(id=1)
        self.country_code = self.city.country_code
        self.expired_date = self.created_date + timedelta(days=30)
        super(Product, self).save(force_insert, force_update)

    @classmethod
    def get_related(cls,product):
        if product.ad_brand:
          qs =  SearchQuerySet().filter(subcategoryid=product.subcategory.id, adbrandid=product.ad_brand.id).exclude(id=product.id)
        else:
          qs =  SearchQuerySet().filter(subcategoryid=product.subcategory.id).exclude(id=product.id)
        print "qs", qs
        related_product=[]
        for product in qs:
            if product.object:
                related_product.append(product)
                print "related_product",related_product
        if not related_product:
          qs =  SearchQuerySet().all().exclude(id=product.id)
          related_product=qs
        return related_product


class FreeAlert(models.Model):
    alert_user=models.ForeignKey(UserProfile,verbose_name='User',help_text='Choose user',null=True)
    alert_category = models.ForeignKey(Category, verbose_name='Category',help_text='Choose category', null=False)
    alert_subcategory =models.ForeignKey(SubCategory,verbose_name='Subcategory',help_text='Choose subcategory',null=False)
    alert_brand=models.ForeignKey(Dropdown,null=True,verbose_name='Brand',help_text='Choose Brand',)
    alert_city=models.ForeignKey(City, null=False,verbose_name='City',help_text='Choose city',)
    alert_locality=models.ForeignKey(Locality, null=False,verbose_name='Locality',help_text='Choose Locality',)
    alert_email=models.EmailField(max_length=30, null=False,verbose_name='Email',help_text='Enter valid email',)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    alert_mobile=models.CharField(validators=[phone_regex], max_length=30, null=False,verbose_name='Mobile')
    mail_is_sent=models.BooleanField(default=False,verbose_name='Mail status')
    last_email_sent = models.DateTimeField(null=True,verbose_name='Delivery date')
    def __unicode__(self):
        return self.alert_email

    def get_matching_filters(cls, product):
        qs = FreeAlert.objects.filter(product=product)
        return qs

class ProductStatistic(models.Model):
  """
  Store every Products viewed in the system.
  """ 
  product = models.ForeignKey(Product)
  system_id =  models.CharField(max_length=60, null=True, blank=True, help_text="auto generated by system for identifying system")
  user = models.ForeignKey(UserProfile, null=True, help_text="Resell user")
  created = models.DateTimeField(auto_now_add=True, help_text="Auto generated by system.")
  modified = models.DateTimeField(auto_now_add=True, auto_now=True, help_text="Auto generated by system.")  
  ip_number = models.CharField(max_length=100, null=True, blank=True, help_text="stores the ip number")
  
  def __unicode__(self):
      return str(self.system_id)
