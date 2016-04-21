import datetime
from haystack.indexes import *
# from haystack.sites import *
from models import Product
from models import *
# from core.config import COUNTRIES_DICT
from django.db.models import F
from search.searchsites import *
from django.contrib.auth.models import User
from advertisement.models import *
from haystack.management.commands import update_index
from django.template import RequestContext

class ProductIndex(SearchIndex, Indexable):  
    text = CharField(document=True, use_template=True)
    searchtext = CharField()
    title = CharField(model_attr='title')
    description = CharField(model_attr='description')
    price = FloatField(model_attr='price')
    #locality = MultiValueField(null=True)
    # keywords = MultiValueField(null=True)
    # category = CharField(model_attr='category', null=True)
    category = CharField(model_attr='category__id')
    brandtype = CharField(model_attr='ad_brand__id', null=True)
    # locality = CharField(model_attr='locality__id')
    subcategoryid = CharField(model_attr='subcategory__id') 
    # adbrandid=CharField(model_attr='ad_brand__id') 
    created_date = DateTimeField(model_attr='created_date')
    modified_date = DateTimeField(model_attr='modified_date') 
    # geolocation = LocationField(model_attr='get_geolocation', null=True)
#     city = CharField(null=True, faceted=True)
    city = CharField(model_attr='city__id')
    locality = CharField(model_attr='locality__id')
    # country= CharField(model_attr='country__id')
    # country=CharField(model_attr='country__id') 
    ispremium=CharField(model_attr='ispremium') 
    premium_plan_id=CharField(model_attr='premium_plan__id',null=True)
    status_isactive=BooleanField(model_attr='status_isactive')

    def autoUpdateRebuild_index(self):
        update_index.Command().handle()
        rebuild_index.Command().handle()

    def prepare_searchtext(self, obj):
        text = []
        if obj.title:
            text.append(obj.title)
            # print"text title", text
        if obj.description:
            text.append(obj.description)
            # print"text description", text 
        # text += self.prepare_locations(obj)
        # text += obj.country
        # print "text", text
        search = []
        for t in text:
            t = re.sub(r'[^\w]', ' ', t, flags=re.UNICODE).split(' ')
            for q in t:
                if q and (not re.match(r'[^\w]', q, flags=re.UNICODE)):
                    search.append(q)
        return ' '.join(search)

    # def prepare_locations(self,obj):
    #     countrys=[]
    #     country=obj.country
    #     countrycode=Country.objects.get(code=country)
    #     print "country", country
    #     print "countrycode", countrycode.code
    #     countrys.append(countrycode.code)
    #     return countrys
    
    def get_model(self):
        return Product
    
    def index_queryset(self, **kwargs):
        product = Product.objects.filter(status_isactive=1)
        return product

# register_model_for_search(Product, ProductIndex)