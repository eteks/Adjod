from django import forms
from django.forms import widgets
from django.forms.util import flatatt
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy
from django.contrib import admin
from advertisement.models import *
import pprint
from django.http import HttpResponseRedirect
from django.http import HttpResponse, Http404

class CategoryAdmin(admin.ModelAdmin):
    fields=['name','category_type','icon',]
    list_display = ('id','name','category_type', 'icon')
    list_filter = ['name']
    search_fields = ['name']
    # readonly_fields =['id']
    list_per_page = 50

class SubCategoryAdmin(admin.ModelAdmin):
    fields=['category','name']
    list_display = ('id', 'category','name')
    list_filter = ['category']
    search_fields = ['name']
    # readonly_fields =['id']
    list_per_page = 50

class CityAdmin(admin.ModelAdmin):
    fields=['city','country_code','country_name']
    list_display = ('id', 'city','country_code','country_name')
    list_filter = ['country_name']
    search_fields = [ 'city','country_code','country_name']
    # readonly_fields =['id']
    list_per_page = 50

class LocalityAdmin(admin.ModelAdmin):
    fields=['city_refid','locality']
    list_display = ('id', 'locality','city_refid','country')
    list_filter = ['city_refid__country_name','city_refid__city']
    search_fields = ['id', 'locality','city_refid__country_name','city_refid__city']
    # readonly_fields =['id']
    list_per_page = 50

    def country(self, obj):
        return obj.city_refid.country_name
    country.short_description = 'Country'

class DropdownAdmin(admin.ModelAdmin):
    fields=['brand_name','subcat']
    list_display = ('id', 'brand_name','subcategory' )
    list_filter = ['subcat__category']
    search_fields = ['id', 'brand_name']
    # readonly_fields =['id']
    list_per_page = 50

    def subcategory(self, obj):
        return ",".join([p.name for p in obj.subcat.all()])

class FreeAlertAdmin(admin.ModelAdmin):
    fields=['alert_user','alert_category', 'alert_subcategory', 'alert_brand', 'alert_city','alert_locality', 'alert_email', 'alert_mobile']
    list_display = ('id', 'alert_user','alert_category', 'alert_subcategory', 'alert_brand', 'alert_city', 'alert_email', 'alert_mobile','mail_is_sent')
    list_filter = ['alert_category']
    search_fields = ['id', 'alert_email','alert_mobile','alert_user','alert_brand', 'alert_city', 'alert_subcategory' ]
    # readonly_fields =['id']
    list_per_page = 50

# class ProductAdmin(admin.ModelAdmin):
#     fields=['userprofile','category', 'subcategory', 'adtype', 'title', 'photos', 'video','condition', 'price',
#             'ad_brand','ad_year','city', 'locality', 'description', 'you_are', 'you_email','you_phone','created_date','modified_date']
#     list_display = ('id', 'userprofile','category', 'subcategory', 'adtype', 'title', 'photos', 'thumbnail', 'imagecount', 'video','condition', 'price',
#             'ad_brand','ad_year','city', 'locality', 'description', 'you_are', 'you_email','you_phone','created_date','modified_date')
#     # list_filter = ['alert_email', 'alert_mobile']
#     search_fields = ['id', 'you_email','you_phone']
#     # readonly_fields =['id']
#     list_per_page = 50

class PremiumPriceInfoAdmin(admin.ModelAdmin):
    fields=['premium_price','purpose','duration']
    list_display = ('id', 'premium_price','base_currency','purpose','duration')
    list_filter = ['purpose']
    search_fields = ['premium_price','base_currency','purpose']
    readonly_fields =['base_currency']
    list_per_page = 50


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'userprofile','category', 'subcategory', 'adtype', 'title', 'photos', 'thumbnail', 'imagecount','condition', 'price',
            'ad_brand','ad_year','city', 'locality', 'description', 'you_are','you_name', 'you_email','you_phone','ispremium','premium_plan','created_date','modified_date','status_isactive')
    list_filter = ['category', 'subcategory','ispremium','premium_plan']
    search_fields = ['^userprofile__username']
    readonly_fields =['city']
    fieldsets = [
      ('Product Details', {
          'fields': [ 'category', 'subcategory','ad_brand','adtype','title', 'description',
                      'photos', 'condition', 'price','ad_year','city','locality']
      }),

      ('Personal information', {
          'fields': ['userprofile','you_are', 'you_name','you_email', 'you_phone'],

      }),

      ('Product Subscription Details', {
          'fields': ['ispremium', 'premium_plan']
      }),

      ('Date', {
          'fields': ['created_date', 'modified_date']
      }),

      ('Active Status', {
          'fields': ['status_isactive']
      }),
    ]
    list_per_page = 50

admin.site.register(PremiumPriceInfo, PremiumPriceInfoAdmin)
admin.site.register(FreeAlert, FreeAlertAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Dropdown, DropdownAdmin)
admin.site.register(Locality, LocalityAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category,CategoryAdmin)
# admin.site.register(Country)
