# coding: utf-8 
# -*- coding: utf-8 -*-
from django.shortcuts import redirect
# from haystack.views import SearchView
from search.searchsites import SearchView
from advertisement.models import *

class AdjodSearchView(SearchView):        
    def __call__(self, request):        
        if 'q' in request.REQUEST and unicode(request.REQUEST['q']).isdigit():          
            productid = long(request.REQUEST['q'])            
            if Product.objects.filter(id__exact=productid).exists():         
                return redirect('productDetail', productid)
        query_string = request.META.get('QUERY_STRING', '').split('&')
        qsl = [qs for qs in query_string if qs.startswith('q=')]
        query = qsl[0].replace('q=', '').decode('latin1') if qsl else u''         
        if u'�' in request.REQUEST.get('q', u''):
            if request.method == "GET": 
                request.GET._mutable = True
                request.GET['q'] = query
                request.GET._mutable = False              
            elif request.method == "POST":         
                request.POST._mutable = True
                request.POST['q'] = query
                request.POST._mutable = False                    
        return super(AdjodSearchView, self).__call__(request)