import os
import random
import string
import uuid
import urllib2
from django.conf import settings
from django.contrib.gis.geoip import GeoIP
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

def get_global_language(request):
    """ This function get global language based on following assets

        1. authenticated user's language
        2. cookie
        2. fixido select language
        3. query string
        4. brower setting
        5. default sweden
    """
    cookies_language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
    if cookies_language:
        select_language = request.POST.get('language', None)

        if select_language and select_language != cookies_language:
            cookies_language = select_language
    else:
       url_language = request.GET.get('la', request.POST.get('language', '')).strip()
       if url_language and url_language.lower() != 'none':
            cookies_language = url_language
       else:
            try:
                g = GeoIP()
                country = g.country_code(get_client_ip(request))
                language_list = ['en','sv','de']
                if country_language_dict[country] in language_list:
                    return country_language_dict[country]
                else:
                    selected_language = 'en'
                    return selected_language

            except Exception as e:
                cookies_language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en').split(',')[0]
    return cookies_language[:2]

def get_global_country(request):
    """ This function get global language based on following assets

        1. authenticated user's language
        2. cookie
        2. fixido select language
        3. query string
        4. brower setting
        5. default sweden
    """
    g = GeoIP()
    city=g.city(get_client_ip(request))
    country_code = city['country_code3']
    country = g.country_code(get_client_ip(request))
    return country,country_code

def get_current_country_cities(request):
    g = GeoIP()
    country = g.country_code(get_client_ip(request))
    # print "country", country
    current_country_cities = City.objects.filter(country_code=country)
    return current_country_cities

def get_global_city(request):
    """ This function get global language based on following assets

        1. authenticated user's language
        2. cookie
        2. fixido select language
        3. query string
        4. brower setting
        5. default sweden
    """
    g = GeoIP()
    #print 'dddddddddddddddddd',g.city
    # get global city
    city=g.city(get_client_ip(request))['city']
    print "city in util.py", city

    #get global city id from database
    try:
        if City.objects.filter(city=city).exists():
            city = City.objects.get(city=city)
            city_id=city.id
        else:
            country = get_global_country(request)
            city_model = City()
            city_model.city = city
            city_model.country_code = country
            city_model.country_name = g.country_name(get_client_ip(request))
            city_model.save()
            city_id = city_model.id
        print "city_id", city_id
    except:
        city = "Singapore"
        city_id = 7
    return city, city_id

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
    user_ip = globals.ip
    # local
    if user_ip.startswith('127.0.0') or user_ip.startswith('192.168.1'):
        user_ip = '114.69.235.2'
        # user_ip  = '219.75.27.16'
    g = GeoIP()
    country_id = g.country_code(user_ip)
    # print "user ip", user_ip
    # print "country_id", country_id
    for key,value in CURRENCIES_BY_COUNTRY_CODE.items():
        if str(key) == str(country_id):
            isocode=value
    current_country = isocode
    # base_currency= settings.BASE_CURRENCY
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
        'IND':'INR',
        'SGP':'SGD',
        'USA':'USD',
    }
    return currency_code[code]

def currency_conversion(price,country):
    currency_code = currency_of_country(country)
    adjod_exchange_rate = ExchangeRate.objects.get(currency=currency_code)
    return float(price)/float(adjod_exchange_rate.value)
