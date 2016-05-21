#Import the UserProfile model individually.
from adjod.models import *
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UserProfileAdmin(admin.ModelAdmin):

    fields=['username','first_name','last_name','password','email','mobile','city','language','is_subscribed','age_status']
    list_display = ('id','email','mobile','city','language','ad_count','is_emailverified','is_subscribed','age_status',)
    list_filter = ['city','language']
    search_fields = ['city', 'language','username','email','mobile']
    readonly_fields =['city']
    list_per_page = 50

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['city', 'password']
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(obj.password)
            obj.save()
        else:
            from templated_email import send_templated_mail
            send_templated_mail(
					template_name = 'welcome',
		            from_email = 'testmail123sample@gmail.com',
		            recipient_list = [obj.email],
		            context={
		                       'user': obj.username,
		                    },
		        )
            obj.save()



class ExchangeRateAdmin(admin.ModelAdmin):
    fields=['currency','value']
    list_display = ('id','currency','value','base_currency')
    search_fields = ['id','currency']
    readonly_fields =['currency','value']
    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def base_currency(self, obj):
        curr = BaseCurrency.objects.latest('id')
        return '1  '+curr.base_currency
    base_currency.short_description = 'Base Currency'

class BaseCurrencyAdmin(admin.ModelAdmin):
    fields=['base_currency']
    list_display = ('id','base_currency')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(BaseCurrency,BaseCurrencyAdmin)
admin.site.register(ExchangeRate,ExchangeRateAdmin)
