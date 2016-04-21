from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from adjod.views import *
from adjod.util import error_404,error_500
from advertisement.views import *
from django.contrib import admin
from advertisement.models import Product

# from haystack.views import SearchView, FacetedSearchView

# Custom Search View
from search.adjodsearch import AdjodSearchView
from search.searchform import ProductSearchFilter
# from advertisement.searchform import ProductSearchFilter

#For language translation
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.defaults import handler404, handler500
from paypal.standard.ipn import *

admin.autodiscover()

js_info_dict = {
    'packages': ('adjod',),
}

#For Django chat
from chat.views import *

#For loading global functions
from django.template.loader import add_to_builtins
add_to_builtins('advertisement.templatetags.app_filters')

urlpatterns = patterns('',
    url(r'^(?i)admin/', include(admin.site.urls)),
    url(r'^$', 'adjod.views.home', name='home'),

    # Home page URL
    url(r'^home/$', 'adjod.views.home', name='home'),

    # URL for enter post form page
    url(r'^postad/$', 'advertisement.views.product_form',name='product_form'),

    # User login verfication
    url(r'^login/$', 'adjod.views.user_login', name='user_login'),

    # User Dashboard page after login
    url(r'^start/$', 'adjod.views.start',name='start'),

    # New user Registration URL
    url(r'^new_user/$', 'adjod.views.register', name='register'),

    # Email confirmation URL, it calls when user click the URL from their mail for user verification
    url(r'^confirm/(?P<confirmation_code>.*)/(?P<username>.*)/', 'adjod.views.confirm',name='confirm' ),

    # For view full detail of particular product with their id
    url(r'^ads/(?P<pk>\d+)/$', 'advertisement.views.product_detail',name='product_detail'),

    # For save product
    url(r'^addproduct/$', 'advertisement.views.product_save',name='product_save'),

    # Paypal
    url(r'^paypal/$', include('paypal.standard.ipn.urls')),
    url(r'^test_paypal/$', 'adjod.views.test_paypal',name='test_paypal'),

    # Find locality for city when ajax call
    url(r'^localities_for_city/$','advertisement.views.localities_for_city', name='localities_for_city'),

    # AutoComplete for Keywords
    url(r'^(?i)autocomplete_keyword/$', 'adjod.views.autocomplete_keyword', name='autocomplete_keyword'),

    # Search & Advance Search
    url(r'^(?i)search/', AdjodSearchView(
      template='search/search.html',
      form_class=ProductSearchFilter,
      #results_per_page=settings.SEARCH_PAGE_NUMBER_OF_LEADS
    ), name='newsearchPageV2'),

    # Logout URL
    url(r'^logout/$', 'adjod.views.logout_view', name='logout_view'),

    # Find Subcategory when ajax call
    url(r'^subcategory_for_category/$', 'advertisement.views.subcategory_for_category',name='subcategory'),

    # Find Brand when ajax call
    url(r'^brand_for_subcategory/$', 'advertisement.views.brand_for_subcategory',name='brand'),

    # Find Subcategory with pass category dynamically in url (Comment this for future reference)
    # url(r'^(?i)categories/(?P<pname>.*)/$', 'advertisement.views.sub_category',name='sub_category'),

    #For language translation
    url(r'^(?i)i18n/', include('django.conf.urls.i18n')),
    url(r'^(?i)jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    # save free alert url
    url(r'^create_free_alert/$', 'advertisement.views.freealert_save',name='free_alert'),

    # expired_ad_conformation
    url(r'^expired_ad_conformation/$', 'advertisement.views.expired_ad_conformation',name='expired_ad_conformation'),

    #Django chat
    url(r'^get/$', 'chat.views.get'),
    # url(r'^get_product/$', 'chat.views.get_product'),
    url(r'^post/$', 'chat.views.post'),

    #Node.js chat
    # url(r'^chat/$', 'adjod.views.chat'),
    url(r'^toolbar/$', 'adjod.views.toolbar'),
    url(r'^store_user_active_list/$', 'chat.views.store_user_active_list'),

    url(r'^store_chat_record/$', 'chat.views.store_chat_record'),

    #For Password Reset
    url(r'^(?i)password_reset/$', 'django.contrib.auth.views.password_reset', {
      'template_name':'registration/password_reset_form.html',
      'email_template_name':'registration/password_reset_email.html'
    }, name="password_reset"),
    url(r'^(?i)user/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/user/password/reset/done/'}),
    url(r'^(?i)user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^(?i)user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'adjod.views.password_reset_confirm',
        {'post_reset_redirect' : '/user/password/done/'}),
    url(r'^(?i)user/password/done/$',
        'django.contrib.auth.views.password_reset_complete'),

    url(r'^get_user_products/$', 'advertisement.views.get_user_products',name='get_user_products'),
    url(r'^loadbasecurrency/$', 'adjod.views.loadbasecurrency',name='loadbasecurrency'),

    #  url for user_profile updated by Ramya
    url(r'^user_manage/$', 'adjod.views.user_manage',name='user_manage'),
    # url(r'^my_chats/$', 'adjod.views.my_chats',name='my_chats'),
    url(r'^edit_postad_detail/(?P<pk>\d+)/$', 'adjod.views.edit_postad_detail',name='edit_postad_detail'),
    url(r'^delete_ad/$', 'adjod.views.delete_ad',name='delete_ad'),
    url(r'^update_product/(?P<pk>\d+)/$', 'adjod.views.update_success',name='update_product'),



    # url for login using social Auth By Priya
    url(r'', include('social_auth.urls')),
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),

    # Test for geo location (comment for future reference)
    # url(r'^(?i)testpage/$', 'adjod.views.geosearch'),

    url(r'^(?i)handler404/$', 'adjod.views.custom_404', name='custom_404'),
    url(r'^(?i)get_banner_height_width/$', 'banner.views.get_banner_height_width', name='get_banner_height_width'),

    url(r'^(?i)autocomplete_product_search/$', 'advertisement.views.autocomplete_product_search', name='autocomplete_product_search'),

)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
