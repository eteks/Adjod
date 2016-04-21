import os
import random
import string
import uuid
import urllib2
from django.conf import settings
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
#from django.contrib.gis.geoip import GeoIP
from adjod import globals
from advertisement.models import *

#For Currency
from moneyed import Money
from djmoney_rates.utils import convert_money
from djmoney_rates.data import CURRENCIES_BY_COUNTRY_CODE

#For getting country and their language
from core.config import country_language_dict

def get_client_ip(request):
    ''' This utility gets client's IP address from the request
    '''
    ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
    if ip.startswith('127.0.0') or ip.startswith('192.168.1'):
        ip = '114.69.235.2'
        # ip  = '219.75.27.16'
    return ip

def format_redirect_url(redirect_path, query_string):
    ''' utility to format redirect url with fixido query string
    '''
    stop_popup = True if 'st=' in query_string else False

    url_join_str = '?'
    if url_join_str in redirect_path:
        redirect_path, qs = redirect_path.split(url_join_str, 1)
        query_string = qs + '&' + query_string

    qs = {}
    for q in query_string.split('&'):
        if '=' in q:
            k, v = q.split('=', 1)
            qs[k] = v

    if stop_popup:
        if qs.has_key('zr'): del qs['zr']
        if qs.has_key('lr'): del qs['lr']
        if qs.has_key('ler'): del qs['ler']
        if qs.has_key('thanks'): del qs['thanks']

    query_string = ''
    for k in qs:
        query_string += k + '=' + qs[k] + '&'

    return redirect_path + url_join_str + query_string[:-1]

# For Price Conversion
def convert(price):
    for key,value in CURRENCIES_BY_COUNTRY_CODE.items():
        if str(key) == str("SG"):
            isocode=value
    current_country = isocode
    adjod_exchange_rate = ExchangeRate.objects.get(currency=current_country)
    return float(price)*float(adjod_exchange_rate.value)

# def convert(price):
#     for key,value in CURRENCIES_BY_COUNTRY_CODE.items():
#         if str(key) == str("IN"):
#             isocode=value
#     current_country = isocode
#     # base_currency= settings.BASE_CURRENCY
#     base_currency= settings.CURRENCY_RATES
#     exchange_rate = convert_money(price,base_currency,current_country)
#     return exchange_rate

# Give input of two character of country code
def currency_symbol(country):
    currency = {
        'IN':u'\u20b9',
        'SG':u'\u0024',
    }
    return currency[country]

# Give input of three character of country code
def currency_of_country(code):
    currency_code = {
        # 'IND':'INR',
        'IN':'INR',
        # 'SGP':'SGD',
        'SG':'SGD',
        'USA':'USD',
    }
    return currency_code[code]

def currency_conversion(price,country):
    currency_code = currency_of_country(country)
    adjod_exchange_rate = ExchangeRate.objects.get(currency=currency_code)
    return float(price)/float(adjod_exchange_rate.value)

def error_404(request):
    return render_to_response('404.html', context_instance=RequestContext(request))

def error_500(request):
    return render_to_response('500.html', context_instance=RequestContext(request))
