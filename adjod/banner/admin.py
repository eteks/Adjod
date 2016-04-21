from django.contrib import admin
from banner.models import *

class BannerPlanAdmin(admin.ModelAdmin):
    list_display = ('id','bannertype','page','position', 'price', 'plan_duration','height','width')
    list_filter = ['page', 'position','bannertype']
    search_fields = ['id', 'page','position','price','plan_duration','bannertype']
    # readonly_fields =['id']
    fieldsets = [
      ('Add BannerPlan', {
          'fields': [ 'page','position','price', 'plan_duration','bannertype','height','width']
      }),
    ]
    list_per_page = 50

    class Media:
        css = {'all': ('css/jquery-ui.css',)}
        js = ('js/jquery-1.11.3.min.js', 'js/jquery-ui-1.10.4.custom.min.js', 'js/admin.js')

class PostBannerAdmin(admin.ModelAdmin):
    # list_display = ('id','banner','link', 'bannerplan', 'startdate','enddate','admin_status')
    list_display = ('id','bannerplan','banner','source','link','startdate','enddate','admin_status')
    
    list_filter = ['bannerplan', 'admin_status']
    search_fields = ['id', 'bannerplan','admin_status']
    #readonly_fields =['id']
    fieldsets = [
      ('Add Banner', {
          'fields': ['bannerplan','banner','source','link','startdate','enddate','admin_status']
      }),
    ]
    list_per_page = 50

    class Media:
        css = {'all': ('css/jquery-ui.css',)}
        js = ('js/jquery-1.11.3.min.js', 'js/jquery-ui-1.10.4.custom.min.js', 'js/admin.js')


admin.site.register(PostBanner, PostBannerAdmin)
admin.site.register(BannerPlan, BannerPlanAdmin)