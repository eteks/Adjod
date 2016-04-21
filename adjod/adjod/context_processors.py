# from django.contrib.gis.geoip import GeoIP
from adjod import globals
from advertisement.models import *

#For getting country and their language
from core.config import country_language_dict
from django.contrib.sites.models import Site

#For Future reference when use geo
# def global_activity(request):
# 	# print "global_activity"
# 	# user_ip = globals.ip
# 	user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
# 	# print "userip", user_ip
# 	if user_ip.startswith('127.0.0') or user_ip.startswith('192.168.1'):
# 		user_ip = '114.69.235.2'
# 		# user_ip  = '219.75.27.16'
# 	g = GeoIP()
# 	country = g.country_code(user_ip) #get country code from geo
# 	# print "country", country
# 	city=g.city(user_ip)['city']    #get current city from geo
# 	# print "city", city
# 	current_country_cities = City.objects.filter(country_code=country) # get current country cities from database
# 	# print "current_country_cities", current_country_cities
# 	#store city if not available in database
# 	try:
# 		if City.objects.filter(city=city).exists():
# 			city = City.objects.get(city=city)
# 			city_id=city.id
# 		else:
# 			country_code = country
# 			city_model = City()
# 			city_model.city = city
# 			city_model.country_code = country_code
# 			city_model.country_name = g.country_name(user_ip)
# 			city_model.save()
# 			city_id = city_model.id
# 	except:
# 		city = "Singapore"
# 		city_id = 7
# 	# print "cityid", city_id
# 	# get global language from dictionary
# 	language_list = ['en','sv','de']
# 	if country_language_dict[country] in language_list:
# 		global_language = country_language_dict[country]
# 	else:
# 		selected_language = 'en'
# 		global_language = selected_language

# 	# print "global_language", global_language

# 	path =  request.path
# 	category = Category.objects.all()
# 	subcategory = SubCategory.objects.all()
# 	recentad=Product.objects.filter(city=city_id).order_by('-id')[:4]
# 	if not recentad:
# 		recentad=Product.objects.filter().order_by('-id')[:4]

# 	#get authenticated user id
# 	if request.user.is_authenticated():
# 		userprofile=request.user
# 		print "userprofile in context processors", userprofile
# 	else:
# 		userprofile=None

# 	return {'country':country,'city': city,'current_country_cities':current_country_cities,
# 			'city_id':city_id,'language':global_language,'path':path,'category':category,
# 			'subcategory':subcategory, 'recentad':recentad,'user_det':userprofile,
# 			'user_ip':user_ip}


def global_activity(request):
	user_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '127.0.0.1'))
	if user_ip.startswith('127.0.0') or user_ip.startswith('192.168.1'):
		user_ip = '114.69.235.2'
		# user_ip  = '219.75.27.16'

	path =  request.path
	category = Category.objects.all()
	subcategory = SubCategory.objects.all()
	dropdown=Dropdown.objects.all()

	country = "Singapore"
	country_code = "SG"
	city="Singapore"
	city_id = "1"
	language= "en"

	locality = Locality.objects.all()
	recentad=Product.objects.filter(city=city_id, status_isactive=1).order_by('-id')[:4]
	if not recentad:
		recentad=Product.objects.filter().order_by('-id')[:4]

	#get premium plan info for user subscription
	try:
		premium_info_account = PremiumPriceInfo.objects.get(purpose="account_subscription")
	except:
		premium_info_account = None

	#get authenticated user id
	if request.user.is_authenticated() and not request.user.is_superuser:
		if UserProfile.objects.filter(id=request.user.id).exists():
			userprofile=UserProfile.objects.get(id=request.user.id)
			print "userprofile in context processors", userprofile
		else:
			userprofile=None
	else:
		userprofile=None
	current_site = Site.objects.get_current()

	return {'country':country,'country_code':country_code,'city': city,'city_id':city_id,'language':language,'path':path,'category':category,
			'subcategory':subcategory,'dropdown':dropdown, 'recentad':recentad,'userprofile':userprofile,'user_ip':user_ip,
			'locality':locality,'premium_info_account':premium_info_account, 'paypal_receiver_email':settings.PAYPAL_RECEIVER_EMAIL,
			'cancel_return': settings.PAYPAL_DICT['cancel_return'],'success_return': settings.PAYPAL_DICT['success_return'],
			'notify_url': settings.PAYPAL_DICT['notify_url'],'sandbox_url':settings.SANDBOX_URL,'current_site':current_site}

# def global_activity(request):
# 	path =  request.path
# 	category = Category.objects.all()
# 	subcategory = SubCategory.objects.all()
# 	recentad=Product.objects.filter().order_by('-id')[:4]
# 	current_country_cities = City.objects.all()
# 	if request.user.is_authenticated():
# 		userprofile=UserProfile.objects.get(user=request.user.id)
# 	else:
# 		userprofile=None
# 	return {'path':path,'category':category,
# 			'subcategory':subcategory, 'recentad':recentad,'user_det':userprofile,'current_country_cities':current_country_cities}
