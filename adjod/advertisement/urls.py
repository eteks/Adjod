from django.conf.urls import patterns, include, url
from advertisment.views import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('advertisement.views',
        url(r'^admin/', include(admin.site.urls)),
)

