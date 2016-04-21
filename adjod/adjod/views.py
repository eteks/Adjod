#User verification and token generation when user login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.http import Http404

#Different ways of rendering HTML page
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse

#For text conversion
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext, string_concat
from django.core.urlresolvers import reverse

#calling local apps such as models, forms, etc..
from django import forms
from advertisement.models import *
from banner.models import *
from templated_email import send_templated_mail
from adjod.util import *

#Others
import logging
import random
import string
from urllib import unquote, urlencode, unquote_plus
from django.conf import settings
from django.utils.encoding import smart_unicode, force_unicode
from time import time

#Generate JSON documents
from django.utils import simplejson
import simplejson as json

#Paypal transaction
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import payment_was_successful

# from django.contrib.sites.models import get_current_site
from adjod.util import format_redirect_url
from django.core.exceptions import ValidationError
from django.contrib import messages

#for currency conversion
from djmoney_rates.models import Rate
from adjod.models import BaseCurrency, ExchangeRate

# For Chat
from chat.models import *

# for delete_ad
import requests

#for transactions
from django.db import transaction

#for create path for images
from advertisement.views import create_path_for_photos_thumbanails, paypal_transaction
from django.contrib.sites.models import Site
from paypal.standard.ipn.views import *

#For Auto Login After reset password
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlencode, base36_to_int
from django.template.response import TemplateResponse


def test_paypal(request):
	# What you want the button to do.
	paypal_dict = {
		"business": settings.PAYPAL_RECEIVER_EMAIL,
		"amount": "1.00",
		"item_name": "name of the item",
		"notify_url": "http://192.168.1.100:8000/paypal/",
		"return_url": "http://192.168.1.100:8000/paypal/",
		"cancel_return": "http://192.168.1.100:8000/postad",
		"custom": "Upgrade all users!",  # Custom command to correlate to some function later (optional)
	}

	# Create the instance.
	form = PayPalPaymentsForm(initial=paypal_dict)
	context = {"form": form}
	return render_to_response('paypal_integration/payment.html',context, context_instance=RequestContext(request))

#Home page defintion
@csrf_exempt
def home(request):
	if request.user.is_superuser:
		logout(request)
		return HttpResponseRedirect('/')
	return render_to_response('adjod/userpage.html', context_instance=RequestContext(request))


@csrf_protect
def user_login(request):
	if request.method == 'POST':
		error={}
		username = request.POST['email_id']
		password = request.POST['password']
		if 'search' in request.POST['next']:
			next_url = request.POST['next'].split('&')[0]
		else:
			next_url = request.POST['next'].split('?')[0]
		print "next_url", next_url
		try:

			if '@' in username:
				if not User.objects.filter(email=username).exists():
					error['email_exists'] = ugettext('Email Doesnot exists')
					print "error['email_exists']",error['email_exists']
					raise ValidationError(error['email_exists'], 1)
			else:
				if not User.objects.filter(username=username).exists():
					error['username_exists'] = ugettext('Username Does not exists')
					print "error['username_exists']",error['username_exists']
					raise ValidationError(error['username_exists'], 2)
		except ValidationError as e:
			messages.add_message(request, messages.ERROR, e.messages[-1])
			if next_url == '/':
				redirect_path = "/login/"
			else:
				redirect_path = next_url
			query_string = 'si=%d' % e.code
			redirect_url = format_redirect_url(redirect_path, query_string)
			return HttpResponseRedirect(redirect_url)
		if not error:
			if not '@' in username:
				user = User.objects.get(username=username)
			else:
				user = User.objects.get(email=username)
			user.backend='django.contrib.auth.backends.ModelBackend'
			if user.is_superuser:
				return HttpResponseRedirect("/")
			try:
				if user.check_password(password):
					print user
				else:
					error['password'] = ugettext('Wrong password')
					raise ValidationError(error['password'], 3)
			except ValidationError as e:
				messages.add_message(request, messages.ERROR, e.messages[-1])
				if next_url == '/':
					redirect_path = "/login/"
				else:
					redirect_path = next_url
				query_string = 'si=%d' % e.code
				redirect_url = format_redirect_url(redirect_path, query_string)
				return HttpResponseRedirect(redirect_url)
			if user:
				# Is the account active? It could have been disabled.
				if user.is_active:
					# If the account is valid and active, we can log the user in.
					# We'll send the user back to the homepage.
					login(request, user)
					print user.id
					user_id=user.id
					# starturl=reverse('start',kwargs={ 'user_id': user.id })
					if next_url == '/':
						response=HttpResponseRedirect('/start/?user_id=' + str(user.id))
					else:
						response=HttpResponseRedirect(next_url)
					response.set_cookie("chat_email", user.email)
					response.set_cookie("chat_user", user.username)
					response.set_cookie("chat_userid", user_id)
					return response
				else:
					# An inactive account was used - no logging in!
					try:
						# error['inactive'] = ugettext('Your Account is already inactive due to non-maintanence')
						error['inactive'] = ugettext('Inactive Account')
						raise ValidationError(error['inactive'], 4)
					except ValidationError as e:
						messages.add_message(request, messages.ERROR, e.messages[-1])
						if next_url == '/':
							redirect_path = "/login/"
						else:
							redirect_path = next_url
						query_string = 'si=%d' % e.code
						redirect_url = format_redirect_url(redirect_path, query_string)
						return HttpResponseRedirect(redirect_url)
	else:
	  return render_to_response('adjod/userpage.html', context_instance=RequestContext(request))


def auto_login(request, user):
	user.backend = 'django.contrib.auth.backends.ModelBackend'
	login(request, user)
	request.session.set_expiry(12 * 30 * 24 * 60 * 60)


#User registration definition
@csrf_protect
def register(request):
	if request.method == 'POST' and request.user.is_anonymous():
		error={}
		email=request.POST['email_id']
		username=request.POST['user_id']
		try:
			if User.objects.filter(email=email).exists():
				error['email_exists'] = ugettext('Email already exists')
				print "error['email_exists']",error['email_exists']
				raise ValidationError(error['email_exists'], 1)
			if User.objects.filter(username=username).exists():
				error['username_exists'] = ugettext('Username already exists')
				print "error['username_exists']",error['username_exists']
				raise ValidationError(error['username_exists'], 2)
			if not error:
				userprofile = UserProfile()
				# userprofile.is_active = True
				userprofile.is_active = False
				userprofile.username=request.POST['user_id']
				userprofile.email=request.POST['email_id']
				userprofile.password=request.POST['password']
				userprofile.set_password(userprofile.password)
				userprofile.first_name=request.POST['user_id']
				userprofile.mobile=request.POST['your_mobile_number']
				try:
					userprofile.city=City.objects.get(city=request.COOKIES.get('city'))
				except:
					userprofile.city=None
				try:
					userprofile.language=request.COOKIES.get('adjod_language')
				except:
					userprofile.language=None
				try:
					userprofile.country_code=request.COOKIES.get('country_code')
				except:
					userprofile.country_code=None
				userprofile.age_status=request.POST.get('confirm')
				userprofile.confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
				userprofile.save()
				send_registration_confirmation(userprofile)
				# auto_login(request, userprofile)
				# return HttpResponseRedirect('/start/?user_id=' + str(userprofile.id))
				error['register_success'] = ugettext('Successfully Registered. Please check the mail and confirm your account')
				print "error['register_success']",error['register_success']
				raise ValidationError(error['register_success'], 5)
		except ValidationError as e:
			messages.add_message(request, messages.ERROR, e.messages[-1])
			redirect_path = "/"
			query_string = 'st=%d' % e.code
			redirect_url = format_redirect_url(redirect_path, query_string)
			return HttpResponseRedirect(redirect_url)


def send_registration_confirmation(userprofile):
	current_site = Site.objects.get_current()
	title = "Resell account confirmation"
	content = current_site.domain + "/confirm/" + str(userprofile.confirmation_code) + "/" + userprofile.username
	send_templated_mail(
				template_name = 'welcome',
				from_email = 'testmail123sample@gmail.com',
				recipient_list = [userprofile.email],
				context={
						 'user': userprofile,
						 'content':content,
						 'email':userprofile.email,
				},
			)

def confirm(request, confirmation_code, username):
	try:
		userprofile = UserProfile.objects.get(username=username)
		if userprofile.confirmation_code == confirmation_code:
			userprofile.is_emailverified=True
			userprofile.is_active=True
			userprofile.save()
			auto_login(request, userprofile)
		return HttpResponseRedirect('/start/?user_id=' + str(userprofile.id))
	except:
		return HttpResponseRedirect('/')


def start(request):
	try:
		last_active = LastActive.objects.create(user = UserProfile.objects.get(id=request.user.id), session = Session.objects.get(session_key = request.session.session_key))
		last_active.save()
	except:
		pass
	response = render_to_response('adjod/userpage.html',context_instance=RequestContext(request))
	response.set_cookie("chat_email", request.user.email)
	response.set_cookie("chat_user", request.user.username)
	response.set_cookie("chat_userid", request.user.id)
	return response


#User Logout definition
def logout_view(request):
	if LastActive.objects.filter(user = request.user.id).exists():
		last_active = LastActive.objects.get(user = request.user.id)
		last_active.delete()
	logout(request)
	response = HttpResponseRedirect("/")
	response.delete_cookie('chat_email')
	response.delete_cookie('chat_user')
	return response


# /*  Auto Complete for Category based Brands */
def autocomplete_keyword(request):
  from collections import OrderedDict
  val = OrderedDict()
  results = []
  keyterm = request.GET.get('term')
  if keyterm:
	unsort_dict = {}
	lead_keywords = Category.objects.filter(name__istartswith=keyterm)
	# print 'lead_keywords',lead_keywords
	for lead_keyword in lead_keywords:
	  keyword_strip = lead_keyword.name.strip()
	  keyword_title = keyword_strip.title()
	  unsort_dict[keyword_title] = {'id':lead_keyword.id, 'label':keyword_title, 'value':keyword_title}
	sorted_dic = OrderedDict(sorted(unsort_dict.iteritems(), key=lambda v: v[0]))
	for k, v in sorted_dic.iteritems():
	  results.append(v)
  return HttpResponse(simplejson.dumps(results), mimetype='application/json')


# /*  Auto Complete for Category based Brands , subCatId='none'*/
def autocomplete_brandlist(request):
  from collections import OrderedDict
  val = OrderedDict()
  results = []
  keyterm = request.GET.get('term')
  if keyterm:
	unsort_dict = {}
	# lead_keywords = Category.objects.filter(name__istartswith=keyterm)
	# print 'lead_keywords',lead_keywords
	# if subCatId
	#     lead_keywords = Category.objects.filter(name__istartswith=keyterm)
	# else
	lead_keywords = Dropdown.objects.filter(name__istartswith=keyterm)
	for lead_keyword in lead_keywords:
	  keyword_strip = lead_keyword.name.strip()
	  keyword_title = keyword_strip.title()
	  unsort_dict[keyword_title] = {'id':lead_keyword.id, 'label':keyword_title, 'value':keyword_title}
	sorted_dic = OrderedDict(sorted(unsort_dict.iteritems(), key=lambda v: v[0]))
	for k, v in sorted_dic.iteritems():
	  results.append(v)
  return HttpResponse(simplejson.dumps(results), mimetype='application/json')


#function for Chat
def toolbar(request):
	return render_to_response('views/toolbar.html', context_instance=RequestContext(request))


def loadbasecurrency(request):
	basecurrency = BaseCurrency.objects.get(id=1)
	adjod_base_currency = basecurrency.base_currency
	base_currency_rate = Rate.objects.get(currency= adjod_base_currency)
	open_exchange_rate = Rate.objects.all()
	ExchangeRate.objects.all().delete()
	for rates in open_exchange_rate:
		conversion = ExchangeRate()
		conversion.currency = rates.currency
		conversion.value = float(rates.value)/float(base_currency_rate.value)
		# conversion.value = float("{0:.2f}".format(rates.value))/float("{0:.2f}".format(base_currency_rate.value))
		conversion.save()
	return HttpResponse('Successfully updated')

#Test geo comment this for future reference
# def geosearch(request):
#     starttime = time()
# #     ipaddress = request.GET.get('ipaddress', '')
#     ipaddress=get_client_ip(request)
#     print 'newip', ipaddress
# #     if not ipaddress:
# #         ipaddress = globals.ip
#     g = GeoIP()
#     country = g.country_code(ipaddress)
#     print "country:", country
# #     language=get_global_language(country)
# #     print "language", language
#     timetaken = time() - starttime
#     language="None"
#     country_language_dict = {
#                     'AU':'en','IN':'en','SE':'sv','DE':'de','SG':'en','SX':'en',}
#     for key,value in country_language_dict.items():
#         if country==key:
#             language=value
#     city=g.city(ipaddress)['city']
#     return render_to_response('adjod/testpage.html', {
#         'country':country, 'ipaddress':ipaddress, 'timetaken':timetaken,'language':language,'city':city
#       }, context_instance=RequestContext(request))

def custom_404(request):
   return render_to_response('404.html')

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import View
from social_auth.views import complete



class AuthComplete(View):
	def get(self, request, *args, **kwargs):
		backend = kwargs.pop('backend')
		try:
			return complete(request, backend, *args, **kwargs)
		except :
			messages.error(request, "Your Google Apps domain isn't authorized for this app")
			return HttpResponseRedirect(reverse('login'))


class LoginError(View):
	def get(self, request, *args, **kwargs):
		return HttpResponse(status=401)

# changes made by ramya for update profile
@csrf_exempt
def user_manage(request):
	if request.user.is_authenticated():
		userprofile_id = request.user.id
		try:
			# my_products = Product.objects.filter(userprofile_id=userprofile_id,status_isactive=True)
			my_products = Product.objects.filter(userprofile_id=userprofile_id).order_by('-created_date') 
			userprofile = UserProfile.objects.get(id=request.user.id)
		except UserProfile.DoesNotExist:
			return render_to_response('404.html', context_instance=RequestContext(request))
		if request.method == 'POST':
			mobile = request.POST.get('your_mobile_no')
			user_age = request.POST.get('user_age')
			gender = request.POST.get('gender')
			user_address = request.POST.get('user_address')
			person_is = request.POST.get('person_is')
			is_marketing_person = request.POST.get('is_marketing_person')
			is_allow_sms = request.POST.get('is_allow_sms')
			locality = Locality.objects.get(id=request.POST['user_locality'])

			def handle_uploaded_file(f):
				print "settings.MEDIA_ROOT", settings.MEDIA_ROOT
				profile_picture = open(
					settings.MEDIA_ROOT + '/profile/' + '%s' % f.name, 'wb+')
				for chunk in f.chunks():
					profile_picture.write(chunk)
				profile_picture.close()

			if userprofile:
				# userprofile.city =City.objects.get(id=1)
				userprofile.mobile = mobile
				userprofile.locality = Locality.objects.get(id=int(locality.id))
				# userprofile.city = City.objects.get(id=request.POST['user_city'])
				if user_age:
					userprofile.user_age = user_age
				else:
					userprofile.user_age = None
				userprofile.gender = gender
				userprofile.user_address = user_address
				userprofile.person_is = person_is
				userprofile.is_marketing_person = is_marketing_person
				userprofile.is_allow_sms = is_allow_sms
				userprofile.last_name = request.POST.get('last_name')
				if 'profile_poster' in request.FILES:
					profile_picture = request.FILES['profile_poster']
					handle_uploaded_file(profile_picture)
					profile_picture = '/profile/' + str(profile_picture)
					userprofile.profile_picture = profile_picture
				else:
					userprofile.profile_picture = userprofile.profile_picture
				userprofile.save()
				if request.POST['pswd']:
					u = User.objects.get(username=request.user.username)
					u.set_password(request.POST.get('pswd'))
					u.save()
			ctx={'my_products':my_products, 'userprofile':userprofile}
		else:
			ctx={'my_products':my_products, 'userprofile':userprofile}
		return render_to_response('adjod/updateprofile.html', ctx, context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect('/')

@login_required
def edit_postad_detail(request , pk):
	edit_product = Product.objects.get(pk=int(pk))
	pic=[n for n in str(edit_product.photos).split(',')]
	return render_to_response('advertisement/ad_post.html', {'edit_product':edit_product, 'pic':pic}, context_instance=RequestContext(request))

@transaction.commit_on_success
def update_success(request, pk):
	updated_product = Product.objects.get(id=pk)
	print 'update_success', updated_product
	if request.method == 'POST':
		try:
			error = {}			
			updated_product.category=Category.objects.get(id=request.POST['category_name'])
			updated_product.subcategory=SubCategory.objects.get(id=request.POST['subcategory_name'])
			if request.POST['brand_name']:
				updated_product.ad_brand=Dropdown.objects.get(id=request.POST['brand_name'])
			else:
				updated_product.ad_brand=None
			updated_product.adtype= "sell"
			updated_product.title=request.POST.get('ad_title')
			updated_product.price = request.POST.get('your_price')
			updated_product.ad_year=request.POST.get('your_year')
			updated_product.description=request.POST.get('description')
			updated_product.you_are = request.POST.get('you_are_radio')
			updated_product.you_name = request.POST.get('your_name')
			updated_product.you_email = request.POST.get('your_email')
			updated_product.you_phone = request.POST.get('your_mobile_no')
			updated_product.city=City.objects.get(id=int(request.POST['your_city']))
			updated_product.locality=Locality.objects.get(id=request.POST['your_locality'])
			print 'updated_product.locality', updated_product.locality
			updated_product.country_code = request.COOKIES.get("country_code")
			# product.photos=request.FILES['photos']
			# if 'photos[]' in request.FILES:
			# 	photos =request.FILES.getlist('photos[]')
			# 	print 'photos>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', photos
			# 	updated_product.photos, updated_product.imagecount, updated_product.thumbnail = create_path_for_photos_thumbanails(photos, updated_product)
			# 	print 'image_receive', updated_product.photos
			photos =request.FILES.getlist('photos[]')
			print 'photos>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', photos
			updated_product.photos, updated_product.imagecount, updated_product.thumbnail = create_path_for_photos_thumbanails(photos, updated_product)
			print 'image_receive', updated_product.photos
			updated_product.video = request.POST.get('video_url')
			updated_product.created_date  = datetime.datetime.now()
			updated_product.modified_date  = datetime.datetime.now()
			updated_product.expired_date=datetime.datetime.now() + datetime.timedelta(days=30)
			updated_product.status_isactive  = True
			updated_product.post_terms=request.POST.get('terms_of_use')
			updated_product.save()			
			# if request.user.is_authenticated():
			if request.POST.get('premium_plan'):
				plan_price = request.POST["premium_plan"]
				updated_product.premium_plan = PremiumPriceInfo.objects.get(premium_price=plan_price)
				updated_product.ispremium = True
				updated_product_dict = {'userprofile':updated_product.userprofile.id, 'category':updated_product.category, 'subcategory':updated_product.subcategory,
							'adtype':updated_product.adtype,'title':updated_product.title, 'photos':updated_product.photos,'thumbnail':updated_product.thumbnail,
							'imagecount':updated_product.imagecount,'video':updated_product.video,'condition':updated_product.condition,'price':updated_product.price,
							'ad_year':updated_product.ad_year, 'city':updated_product.city, 'locality':updated_product.locality,'country_code':updated_product.country_code,
							'description':updated_product.description,'you_are':updated_product.you_are, 'you_name':updated_product.you_name,'you_email':updated_product.you_email,
							'you_phone':updated_product.you_phone,'isregistered_user':updated_product.isregistered_user,'ispremium':updated_product.ispremium,
							'premium_plan':updated_product.premium_plan,'expired_date':updated_product.expired_date,'status_isactive':updated_product.status_isactive,
							'post_term_status':updated_product.post_term_status,"premium_plan":updated_product.premium_plan.id}
				response = paypal_transaction(request,updated_product_dict)
				return response

			# else:
			# 	response = None
			# 	print 'else paypal'
			# 	error['success'] = ugettext('Ad Successfully updated')
			# 	raise ValidationError(error['success'], 7)
			else:
				response = None
				print 'response in else view', response
				error['success'] = ugettext('Ad Successfully updated')
				raise ValidationError(error['success'], 7)				
			updated_product.save()
			current_site = Site.objects.get_current()
			send_templated_mail(
					  template_name = 'post_ad',
					  from_email = 'testmail123sample@gmail.com',
					  recipient_list= [updated_product.you_email],
					  context = {
						 'subject': 'Alert Products',
						 'content':updated_product.title,
						 'user':updated_product.you_name ,
						 'current_site':current_site,

					  },
					)
			return response

		except ValidationError as e:
			messages.add_message(request, messages.ERROR, e.messages[-1])
			redirect_path = "/user_manage/"
			query_string = 'pt=%d' % e.code
			redirect_url = format_redirect_url(redirect_path, query_string)
			return HttpResponseRedirect(redirect_url)

	else:
		return HttpResponseRedirect("/user_manage/")

@csrf_exempt
def delete_ad(request):
	if request.method == 'POST':
		get_products = []
		product_list = request.POST.get('selected')
		print 'product_list', product_list
		list_items = product_list.split(',')
		print 'list_items', list_items
		get_products = [int(i) for i in list_items]
		products = Product.objects.filter(pk__in=get_products)
		print 'products', products
		for deactivate_product in products:
			print 'deactivate_product', deactivate_product
			deactivate_product.status_isactive = False
			deactivate_product.save()
		my_products = Product.objects.filter(userprofile_id=request.user.id, status_isactive=1)
		print 'my_products', my_products
	return render_to_response('adjod/updateprofile.html', {'my_products':my_products}, context_instance=RequestContext(request))

# Customized view for auto login
# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb36=None, token=None,
						   template_name='registration/password_reset_confirm.html',
						   token_generator=default_token_generator,
						   set_password_form=SetPasswordForm,
						   post_reset_redirect=None,
						   current_app=None, extra_context=None):
	"""
	View that checks the hash in a password reset link and presents a
	form for entering a new password. (Customized)
	"""
	assert uidb36 is not None and token is not None # checked by URLconf
	if post_reset_redirect is None:
		post_reset_redirect = reverse('django.contrib.auth.views.password_reset_complete')
	try:
		uid_int = base36_to_int(uidb36)
		user = User.objects.get(id=uid_int)
	except (ValueError, User.DoesNotExist):
		user = None

	if user is not None and token_generator.check_token(user, token):
		validlink = True
		if request.method == 'POST':
			form = set_password_form(user, request.POST)
			if form.is_valid():
				form.save()
				auto_login(request, user) # Auto login
				return HttpResponseRedirect(post_reset_redirect)
		else:
			form = set_password_form(None)
	else:
		validlink = False
		form = None
	context = {
		'form': form,
		'validlink': validlink,
	}
	if extra_context is not None:
		context.update(extra_context)
	return TemplateResponse(request, template_name, context,
							current_app=current_app)