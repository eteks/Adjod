import re
from django import forms
from collections import OrderedDict
from advertisement.models import *
from haystack.forms import SearchForm, FacetedSearchForm
from datetime import datetime
from django.http import HttpResponse, Http404
from search.searchresults import searchresults as productsearch
from haystack.query import SearchQuerySet
from haystack.inputs import Clean, Raw, AutoQuery, Exact
from haystack.query import SQ
from advertisement.models import Product
from adjod.util import *

class Partial(Clean):
    input_type_name = 'partial'
    post_process = True

    def __init__(self, query_string, **kwargs):
        self.original = query_string
        super(Partial, self).__init__(query_string, **kwargs)

    def prepare(self, query_obj):
        query_string = super(Partial, self).prepare(query_obj)
        query_string = query_string.lower()
        query_string = re.sub( '\s+', '* ', query_string).strip()

        if query_string[-1] != '*':
          query_string = query_string + u'*'

        return 

class ProductSearchFilter(FacetedSearchForm):
    model = None

    price_start = forms.FloatField(required=False)
    price_end = forms.FloatField(required=False)
    pricehigh = forms.FloatField(required=False)   
    pricelow = forms.FloatField(required=False)
    locality    = forms.CharField(required=False)
    price       = forms.FloatField(required=False)
    category    = forms.CharField(required=False)
    brandtype   = forms.CharField(required=False)
    subcategoryid = forms.CharField(required=False)
    sorteddata = forms.CharField(required=False)
    country=forms.CharField(required=False)
    ispremium=forms.CharField(required=False)
    premium_plan_id=forms.CharField(required=False)
    # lang = forms.CharField(required=False)
    city=forms.CharField(required=False)
    locality=forms.CharField(required=False)
    groupby = forms.CharField(required=False)
    status_isactive = forms.BooleanField(required=False)
   
    def no_query_found(self): 
      data = self.searchqueryset.all()  
        
      if hasattr(self, 'cleaned_data'):
          save_object = None

          if self.cleaned_data['sorteddata']:
              if (self.cleaned_data['sorteddata'] == "createddate"):
                data = data.filter(status_isactive=1).order_by('created_date')
                
              # if (self.cleaned_data['sorteddata'] == "modifieddate"):
              #  data = data.filter(status_isactive=1).order_by('modified_date')
              
              if (self.cleaned_data['sorteddata'] == "pricelow"):
                data = data.filter(status_isactive=1).order_by('price')
              
              if (self.cleaned_data['sorteddata'] == "pricehigh"):  
                data = data.filter(status_isactive=1).order_by('-price')
       
      return data
  
    def get_default_queryset(self, request):          
        sqs = SearchQuerySet().all()
        sqs = sqs.models(Product)
        currentcity = "Singapore"
        city_id = "1"
        return sqs.filter(status_isactive=1, city=int(city_id)).order_by('-ispremium')
        # currentcity = "Pondicherry"
        # return sqs.filter(status_isactive=1, city__city=currentcity).order_by('-ispremium')
        
    def get_default_filters(self):
      return None
    
    def get_default_search_field(self):
      return 'searchtext'

    def get_model_class(self):
      return Product

    def search(self, request):
      sqs = self.get_default_queryset(request)

      if not hasattr(self, 'cleaned_data'):
        return productsearch(model_cls=self.get_model_class(), 
          default_filters=self.get_default_filters())
        
      _params = [
        'locality',
        # 'keywords',
        # 'lang',
        'category',
        'price',
        'brandtype',
        'subcategoryid',
        'price_start',
        'price_end',
        'country',
        'ispremium',
        'premium_plan_id',
        'city', 
        'locality',
        'pricelow',
        'pricehigh',
      ]
      params = OrderedDict()
      for p in _params:
        if p in self.cleaned_data and self.cleaned_data[p]:
          params[p] =  self.cleaned_data[p]
        else:
          params[p] =  None

      if params['country']:
        params['country'] = params['country']
      
      if params['ispremium']:
        params['ispremium'] = params['ispremium']
        
      if params['pricelow']:     
        params['pricelow'] = params['pricelow']               
              
      if params['pricehigh']:           
        params['pricehigh'] = params['pricehigh']                    
              
      if params['city']:              
        params['city'] = params['city']              

      q = self.cleaned_data['q'] if 'q' in self.cleaned_data else None
      groupby = None
      orderby = None

      orderby_mappings = {
        'createddate': '-created_date',
#         'modifieddate': '-modified',
        'pricelow': 'price',
        'pricehigh': '-price',
        'ispremium': '-ispremium',
        'premium_plan_id': '-premium_plan_id',
      }
      
      # if self.cleaned_data['groupby']:
      #   groupby = self.cleaned_data['groupby']

      if self.cleaned_data['sorteddata']:
        orderby = self.cleaned_data['sorteddata']
      
      if orderby in orderby_mappings:
          orderby = orderby_mappings[orderby]

      if self.cleaned_data['groupby']:
        groupby = self.cleaned_data['groupby']
        sqs = sqs.facet(groupby)
        return sqs

      if not orderby:
        orderby = orderby_mappings['premium_plan_id'] 

      return productsearch(q, params, orderby, groupby, model_cls=self.get_model_class(), 
        default_filters=self.get_default_filters(), 
        default_search_field=self.get_default_search_field())