from __future__ import division

from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv46_address
from core import helper
from django.middleware import csrf
from advertisement.models import ProductStatistic, Product
from adjod.models import UserProfile

headers = (
    'HTTP_CLIENT_IP', 'HTTP_X_FORWARDED_FOR', 'HTTP_X_FORWARDED',
    'HTTP_X_CLUSTERED_CLIENT_IP', 'HTTP_FORWARDED_FOR', 'HTTP_FORWARDED',
    'REMOTE_ADDR'
)


def get_ip_address(request):
    for header in headers:
        if request.META.get(header, None):
            ip = request.META[header].split(',')[0]

            try:
                validate_ipv46_address(ip)
                return ip
            except ValidationError:
                pass


def total_seconds(delta):
    day_seconds = (delta.days * 24 * 3600) + delta.seconds
    return (delta.microseconds + day_seconds * 10**6) / 10**6

def update_product_viewed_count(request, product):
    """ Stores viewed product information
        with system id and user id
    """
    from adjod import globals
    system_id = request.COOKIES.get('csrftoken', csrf.get_token(request))
    ip_number = globals.ip   
    if product:   
        if request.user.is_authenticated():
            user = UserProfile.objects.get(id=request.user.id)
            try:
                statisticfilter = ProductStatistic.objects.get(product=product,user=user)  
            except:
                statisticfilter = None
        else:
            user = None  
            try:
                statisticfilter = ProductStatistic.objects.get(product=product,user=user,system_id=system_id)  
            except:
                statisticfilter = None
        if statisticfilter is None: 
            productviewed = ProductStatistic.objects.create(
                product=Product.objects.get(id=product), system_id=system_id,
                user=user, ip_number=ip_number,
                modified=helper.get_now()
            )        
        
        