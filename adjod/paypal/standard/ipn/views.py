#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from paypal.standard.ipn.forms import PayPalIPNForm
from paypal.standard.ipn.models import PayPalIPN
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import payment_was_successful
from adjod.models import UserProfile

from django.contrib.sites.models import Site
from advertisement.models import PremiumPriceInfo, Product
from adjod.util import currency_of_country, format_redirect_url
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.db import transaction
from commerce.models import *
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext
from django.contrib import messages
import urllib

def show_me_the_money(sender, **kwargs):
	print "show_me_the_money"
	ipn_obj = sender
	if ipn_obj.payment_status == ST_PP_COMPLETED:
		# Undertake some action depending upon `ipn_obj`.
		if ipn_obj.custom == "Upgrade all users!":
			Users.objects.update(paid=True)
payment_was_successful.connect(show_me_the_money)

def store_transaction(request,ipn_obj):
	query = ipn_obj.query.split('&')
	data = dict(item.split("=") for item in ipn_obj.query.split("&"))
	print "data", data
	if request.COOKIES.get('product_id') and request.COOKIES.get('premiumplan'):
		print "product if"
		sub_type="product"
		if Product.objects.filter(id=request.COOKIES.get('product_id')).exists():
			product = Product.objects.get(id=request.COOKIES.get('product_id'))
			if ipn_obj.payment_status == "Pending":
				product.ispremium =False
				product.premium_plan =None
				product.status_isactive = False
				status = "pending"
			else:
				print "completed"
				premiumpriceinfo = PremiumPriceInfo.objects.get(id=request.COOKIES.get('premiumplan'))
				print "premiumpriceinfo", premiumpriceinfo
				if premiumpriceinfo.purpose == "urgent_subscription" or premiumpriceinfo.purpose == "top_subscription" or premiumpriceinfo.purpose == "urgent_top_subscription":
					product.ispremium = True
					product.premium_plan = PremiumPriceInfo.objects.get(id=request.COOKIES.get('premiumplan'))
					product.status_isactive = True
					order = Order()
					order.product = product
					order.subscription_plan = PremiumPriceInfo.objects.get(id=request.COOKIES.get('premiumplan'))
					order.save()
					transaction =  Transaction()
					transaction.userprofile = UserProfile.objects.get(id=request.user.id)
					transaction.transaction_mode = "online"
					transaction.amount = ipn_obj.mc_gross
					transaction.transaction_type = product.premium_plan.purpose
					transaction.order = order
					transaction.paypal = ipn_obj
					transaction.payment_status = ipn_obj.payment_status
					transaction.save()
					status = "completed"
			product.save()
	# elif request.COOKIES.get('transaction_type'):
	elif data['item_name'] == "Account+Subscription":
		print "transaction_type"
		sub_type="account"	
		premium_plan = PremiumPriceInfo.objects.get(purpose="account_subscription")
		if ipn_obj.payment_status == "Completed":
			order = Order()
			order.subscription_plan = PremiumPriceInfo.objects.get(id=premium_plan.id)
			order.save()
			transaction =  Transaction()
			transaction.userprofile = UserProfile.objects.get(id=request.user.id)
			transaction.transaction_mode = "online"
			transaction.amount = ipn_obj.mc_gross
			transaction.transaction_type = premium_plan.purpose
			transaction.order = order
			transaction.paypal = ipn_obj
			transaction.payment_status = ipn_obj.payment_status
			transaction.save()
			userprofile = UserProfile.objects.get(id=request.user.id)
			userprofile.is_subscribed = True
			userprofile.save()
			status = "completed"					
		else:
			status = "pending"
		print "status", status
	else:
		status = "failed"
		sub_type = "failed"
	return status, sub_type	
				

# @transaction.commit_on_success
@csrf_exempt
@require_POST
def ipn(request, item_check_callable=None):
	print "enter ipn"
	"""
	PayPal IPN endpoint (notify_url).
	Used by both PayPal Payments Pro and Payments Standard to confirm transactions.
	http://tinyurl.com/d9vu9d

	PayPal IPN Simulator:
	https://developer.paypal.com/cgi-bin/devscr?cmd=_ipn-link-session
	"""
	flag = None
	ipn_obj = None

	# Clean up the data as PayPal sends some weird values such as "N/A"
	data = request.POST.copy()
	date_fields = ('time_created', 'payment_date', 'next_payment_date', 'subscr_date', 'subscr_effective')
	for date_field in date_fields:
		if data.get(date_field) == 'N/A':
			del data[date_field]

	form = PayPalIPNForm(data)
	if form.is_valid():
		try:
			ipn_obj = form.save(commit=False)
		except Exception, e:
			flag = "Exception while processing. (%s)" % e
	else:
		flag = "Invalid form. (%s)" % form.errors

	if ipn_obj is None:
		ipn_obj = PayPalIPN()

	ipn_obj.initialize(request)
	if flag is not None:
		ipn_obj.set_flag(flag)
	else:
		# Secrets should only be used over SSL.
		if request.is_secure() and 'secret' in request.GET:
			ipn_obj.verify_secret(form, request.GET['secret'])
		else:
			ipn_obj.verify(item_check_callable)
	ipn_obj.user =  UserProfile.objects.get(id=request.user.id)
	ipn_obj.save()
	# own code
	error ={}
	status,sub_type = store_transaction(request, ipn_obj)
	print "status", status
	print "sub_type", sub_type
	if sub_type == "product":
		try:	
			print "try"
			if status == "completed":
				print "if"
				error['success'] = ugettext('Your Ad Successfully posted with succesfull payment')
				print "error['success']", error['success']
				raise ValidationError(error['success'], 5)
			else:
				print "else"
				error['success'] = ugettext('Error In Transaction')
				print "error['success']", error['success']
				raise ValidationError(error['success'], 6)
		except ValidationError as e:
				print "except"
				messages.add_message(request, messages.ERROR, e.messages[-1])
				redirect_path = "/postad/"
				print "redirect_path", redirect_path
				query_string = 'pt=%d' % e.code
				redirect_url = format_redirect_url(redirect_path, query_string)
	elif sub_type == "account":
		try:        
			if status == "completed":
				error['success'] = ugettext('Your account Successfully subscribed')
				raise ValidationError(error['success'], 5)
			else:
				error['success'] = ugettext('Error In Transaction')
				raise ValidationError(error['success'], 6)
		except ValidationError as e:
				messages.add_message(request, messages.ERROR, e.messages[-1])
				redirect_path = "/"
				query_string = 'pt=%d' % e.code
				redirect_url = format_redirect_url(redirect_path, query_string)
	else:
		redirect_url = "/"
	response = HttpResponseRedirect(redirect_url)		
	if request.COOKIES.get('product_id'):
		response.delete_cookie('product_id')
	if request.COOKIES.get('premiumplan'):
		response.delete_cookie('premiumplan')
	# if request.COOKIES.get('transaction_type'):
	# 	response.delete_cookie('transaction_type')
	return response
	

