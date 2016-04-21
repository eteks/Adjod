"""
Module to handle all search related tasks 
"""
import re
from collections import OrderedDict

from haystack.query import SearchQuerySet
# from haystack.utils.geo import Point, D
from haystack.inputs import Clean, Raw
from haystack.query import SQ


default_param_mappings = OrderedDict(
  #FieldName = Form Variable
  locality = 'locality',
  price = 'price',
  category = 'category',
  brandtype = 'brandtype',
  subcategoryid = 'subcategoryid',
  price_start = 'price__gte',
  price_end = 'price__lte',
  country= 'country__code',
  ispremium = 'ispremium',
  city = 'city',
  #keywords = 'keywords__in',
  # lang = 'language__in',  
  pricehigh = '-price',
  pricelow = 'price',
  createddate = 'created_date',
)

default_geo_params = {
  'method': 'bydistance',
  'radius': 20
}

default_orderby_mappings = {
  'createddate': 'created_date',
  # 'modifieddate': '-modified',
  'pricelow': 'price',
  'pricehigh': '-price',
  'ispremium': '-ispremium'
}

# default_lead_filters = {
#   'active': 1,
#   'status': 'active',
#   'available__gt': 0
# }

replace_regex = r'[/:]'
ignore_regex = r'[^\w^,]'
tokenizer_regex = re.compile(r'[,]', flags=re.UNICODE)

def tokenize(query, double_check=True):
  tokens = tokenizer_regex.split(query)
  return [q.strip() for q in tokens if q]

def prepare_search_query(query, search_field='searchtext'):
  query = query or ''
  qs = None

  query = re.sub(replace_regex, ' ', query, flags=re.UNICODE)
  tokens = tokenize(query)

  if tokens:
    cleand = Clean(query)
    qs = SQ(**{search_field:cleand})
    qs = qs | SQ(**{search_field + '__startswith': cleand})
    if len(tokens) > 1:
      for q in tokens:
        qs = qs | SQ(**{search_field:Clean(q)})
        qs = qs | SQ(**{search_field + '__startswith': Clean(q)})

  return qs

def searchresults(q=None, params=None, orderby=None, groupby=None, 
  geo_location=None, geo_params=None, geo_orderby='distance', 
  model_cls=None, default_filters=None, param_mappings=None,
  default_search_field='searchtext'):

  """Perform search leads using haystack"""
  print 'Leadsearch as Search'
  if not model_cls:
    model_cls = Product

  if params is None:
    params = OrderedDict([('locality', None), ('category', None), ('brandtype', None), ('price', None),('pricehigh', None),('pricelow', None), ('price_start', None), ('price_end', None), ('subcategory', None),('city', None),('country', None),('ispremium', None), ('locality', None)])   
  
  if orderby is None:
    # orderby = 'created_date'  
     orderby = '-premium_plan_id'

  if orderby:
     orderby_date = '-created_date'

  mappings = param_mappings or default_param_mappings

  sqs = SearchQuerySet().all()
  if q:
    qs = prepare_search_query(q, default_search_field)
    if qs:
      sqs = SearchQuerySet().filter(qs)
     
  sqs = sqs.models(model_cls)
  # sqs = sqs.filter(**default_filters)
  
  if params:
    sq_params = OrderedDict()
    for given_param, search_param in mappings.iteritems():      
      if has(params, given_param):
        sq_params[search_param] =  params[given_param]
    
    
  if sq_params:
    sqs = sqs.filter(**sq_params)
    
  if orderby:
    sqs = sqs.order_by(orderby,orderby_date)

  if groupby:
    sqs = sqs.facet(groupby)

  print "Created query", unicode(sqs.query), geo_location, geo_params
  # print "Created query", sqs
  return sqs

def has(dictobj, key):
  return (key in dictobj) and dictobj[key]