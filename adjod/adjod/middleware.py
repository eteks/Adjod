from core import helper
from adjod import globals
from django.conf import settings
from adjod.util import get_client_ip
from advertisement.models import *

#Middleware class for finding global_lanugage, global_country, global_ip when user enter into the website
class Global(object):
    global_language = ''
    global_country=''
    global_country_code=''
    global_ip=''
    global_city=''
    global_city_id=''

    def process_request(self, request):
        globals.request = request
        globals.user = getattr(request, 'user', None)
        globals.ip = get_client_ip(request)
        if ',' in globals.ip:
            globals.ip = globals.ip.split(',')[0].strip()
        globals.sess = request.session.session_key
        self.global_country = "Singapore"
        self.global_country_code = "SG"
        self.global_city="Singapore"
        self.global_city_id = "1"
        self.global_ip = globals.ip
        self.global_language= "en"
        if request.user.is_authenticated():
            try:
                request.user.last_login = helper.get_now()
                request.user.save()
            except Exception, e:
                pass

    def process_response(self, request, response):
        """while response set cookie for language"""
        if self.global_language:
            language=self.global_language
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME,
                language, max_age = 365 * 24 * 60 * 60)

        if self.global_country:
            country=self.global_country
            response.set_cookie("country",
                country, max_age = 365 * 24 * 60 * 60)

        if self.global_country_code:
            country_code=self.global_country_code
            response.set_cookie("country_code",
                country_code, max_age = 365 * 24 * 60 * 60)

        if self.global_ip:
            ip=self.global_ip
            response.set_cookie("ip",
                ip, max_age = 365 * 24 * 60 * 60)

        if self.global_city:
            city=self.global_city
            response.set_cookie("city",
                city, max_age = 365 * 24 * 60 * 60)

        if self.global_city_id:
            city=int(self.global_city_id)
            response.set_cookie("global_city_id",
                                city, max_age = 365 * 24 * 60 * 60)
        return response
