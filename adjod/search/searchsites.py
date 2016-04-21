from __future__ import unicode_literals
from advertisement.models import *
import logging
import pyelasticsearch
import requests
import BeautifulSoup
from django.utils.html import strip_tags
from haystack.utils import Highlighter
from haystack.backends.elasticsearch_backend import ElasticsearchSearchEngine, ElasticsearchSearchBackend, ElasticsearchSearchQuery
from haystack.forms import ModelSearchForm, FacetedSearchForm
from haystack.query import EmptySearchQuerySet
from haystack.indexes import *
from templated_email.backends.vanilla_django import TemplateBackend
from django.conf import settings
from django.template import Context, TemplateDoesNotExist
from django.template.loader import get_template
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack.forms import ModelSearchForm, FacetedSearchForm
from haystack.query import EmptySearchQuerySet

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 15)

class AdjodSearchBackend(ElasticsearchSearchBackend):

  def build_search_kwargs(self, *args, **kwargs):
    o = super(AdjodSearchBackend, self).build_search_kwargs(*args, **kwargs)
    if hasattr(self, 'default_operator'):
      q = o['query']['filtered']['query']
      if 'query_string' in q:
        q['query_string']['default_operator'] = self.default_operator

    return o  

  def percolator(self, uid, doc, params=None):
    try:    
      raw_results = self.conn.index(
        '_percolator', self.index_name, doc, id=uid)
    except (requests.RequestException, pyelasticsearch.ElasticHttpError) as e:
      if not self.silently_fail:
          raise
      self.log.error("Failed to query Elasticsearch using '%s': %s for %s", uid, e, doc)
      raw_results = {'ok': False}

    return raw_results['ok']

  def percolate(self, index, doc, params=None):
    prepped_data = index().full_prepare(doc)
    final_data = {}
    for key, value in prepped_data.items():
      final_data[key] = self._from_python(value)

    final_data = {'doc': final_data}    
    try:
      raw_results = self.conn.percolate(self.index_name, 'modelresult',
        final_data)
    except (requests.RequestException, pyelasticsearch.ElasticHttpError) as e:
      if not self.silently_fail:
          raise
      self.log.error("Failed to query Elasticsearch using '%s': %s", 
        self.index_name, e)
      raw_results = {}

    return raw_results   

class AdjodSearchQuery(ElasticsearchSearchQuery):
  
  def get_raw_query(self, spelling_query=None, **kwargs):
    query_string = self.build_query()
    _kwargs = self.build_params(spelling_query, **kwargs)
    # results = self.backend.search(query_string, **_kwargs)    

    if not self.backend.setup_complete:
      self.backend.setup()

    search_kwargs = self.backend.build_search_kwargs(query_string, **_kwargs)
    search_kwargs['from'] = _kwargs.get('start_offset', 0)

    order_fields = set()
    for order in search_kwargs.get('sort', []):
      for key in order.keys():
        order_fields.add(key)

    # geo_sort = '_geo_distance' in order_fields

    end_offset = _kwargs.get('end_offset')
    start_offset = _kwargs.get('start_offset', 0)
    if end_offset is not None and end_offset > start_offset:
      search_kwargs['size'] = end_offset - start_offset


    return search_kwargs


  def percolator(self, uid, params=None, **kwargs):
    search_kwargs = self.get_raw_query(**kwargs)
    return self.backend.percolator(uid, search_kwargs, params)

  def percolate(self, index, doc, params=None):
    return self.backend.percolate(index, doc, params)


class AdjodSearchEngine(ElasticsearchSearchEngine):
  backend = AdjodSearchBackend
  query = AdjodSearchQuery

class SearchView(object):
    template = 'search/search.html'
    extra_context = {}
    query = ''
    results = EmptySearchQuerySet()
    request = None
    form = None
    results_per_page = RESULTS_PER_PAGE

    def __init__(self, template=None, load_all=True, form_class=None, searchqueryset=None, context_class=RequestContext, results_per_page=None):      
        self.load_all = load_all
        self.form_class = form_class
        self.context_class = context_class
        self.searchqueryset = searchqueryset

        if form_class is None:
            self.form_class = ModelSearchForm

        if not results_per_page is None:
            self.results_per_page = results_per_page

        if template:
            self.template = template

    def __call__(self, request):        
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.request = request

        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results(request)

        return self.create_response()

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']

        return ''

    def get_results(self,request): 
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        return self.form.search(request)

    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
       
        if self.request.GET.get('page'):
            page_no = self.request.GET.get('page')
            if page_no > 1 :
                page_no = int(self.request.GET.get('page'))
            else:
                page_no = 1
        else:
            page_no = 1
            
      
        if self.request.GET.get('result_per_page'):
            result_display = self.request.GET.get('result_per_page')
            if result_display >  1 :
                result_display = int(self.request.GET.get('result_per_page'))
            else:
                result_display = RESULTS_PER_PAGE 
        else:
            result_display = RESULTS_PER_PAGE

        
        start_offset = (page_no - 1) * result_display
        self.results[start_offset:start_offset + result_display]

        paginator = Paginator(self.results, result_display)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise Http404("No such page!")

        return (paginator, page)

    def extra_context(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
        return {}

    def create_response(self):
        """
        Generates the actual HttpResponse to send back to the user.
        """
        (paginator, page) = self.build_page()

        context = {
            'query': self.query,
            'form': self.form,
            'page': page,
            'paginator': paginator,
            'suggestion': None,
        }

        if self.results and hasattr(self.results, 'query') and self.results.query.backend.include_spelling:
            context['suggestion'] = self.form.get_suggestion()

        context.update(self.extra_context())
        return render_to_response(self.template, context, context_instance=self.context_class(self.request))



