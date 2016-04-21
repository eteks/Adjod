from django.contrib.auth.models import User
from django.db import models
from advertisement.models import *
from django.utils.translation import ugettext_lazy as _

LANGUAGE = (
    ('en', 'English'),
    ('zh', 'Chinese'),
    ('ms', 'Malay'),
)

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
)

YOU=( ('individual','Individual'),('dealer','Dealer'))


#Model for storing user personal details
class UserProfile(User):
    mobile=models.CharField(max_length=15, null=True, blank=True,help_text='Enter mobile number international format')
    confirmation_code=models.CharField(max_length=500,help_text='Confirmation code will add automatically when user registration')
    city=models.ForeignKey('advertisement.City', null=True, blank=True,)
    language=models.CharField(max_length=5,choices=LANGUAGE,default='en',help_text='Choose any one language')
    age_status=models.BooleanField(default=False,help_text='Please verify user age as above 18')
    is_emailverified=models.BooleanField(default=False)
    ad_count=models.IntegerField(max_length=5, null=True, blank=True, default=0)
    is_subscribed=models.BooleanField(default=False,verbose_name='Paid user')
    subscribed_plan = models.ForeignKey('advertisement.PremiumPriceInfo', null=True, blank=True)
    #updated by ramya for  update userprofile    
    profile_picture=models.ImageField(
        upload_to='profile', null=True, blank=True, max_length=500)
    person_is=models.CharField(max_length=20,choices=YOU,default='individual', null=True, blank=True)
    gender=models.CharField(max_length=50, null=True, blank=True, choices=GENDER_CHOICES)
    user_age=models.IntegerField(null=True, blank=True)
    locality=models.ForeignKey('advertisement.Locality', null=True, blank=True)
    user_address=models.TextField(null=True, blank=True)
    is_marketing_person=models.BooleanField(default=False)
    is_allow_sms=models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False):
        from advertisement.models import City
        self.city = City.objects.get(id=1)
        super(UserProfile, self).save(force_insert, force_update)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.username


class ExchangeRate(models.Model):

    currency = models.CharField(max_length=3)
    value = models.DecimalField(max_digits=20, decimal_places=6,verbose_name='Amount',help_text='This is equvalence to one base_currency amount')

    class Meta:
        ordering = ['id']

    #commented by ramya for language translation    
    # def __str__(self):
    #     return _("%s at %.6f") % (self.currency, self.value)

class BaseCurrency(models.Model):
    base_currency = models.CharField(
        max_length=3,
        verbose_name='Base Currency',
        help_text="please refer as <a href='https://en.wikipedia.org/wiki/ISO_4217'>https://en.wikipedia.org/wiki/ISO_4217</a>" )
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Base Currency"
        verbose_name_plural = "Base Currency"

    #commented by ramya for language translation
    # def __str__(self):
    #     return _("%s rates update %s") % (
    #         self.base_currency, self.last_update)
