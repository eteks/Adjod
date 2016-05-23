import decimal
from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import *
from advertisement.models import *
from banner.models import *
from adjod.views import *
from adjod.util import currency_symbol
# from django.contrib.gis.geoip import GeoIP
register = template.Library()

@register.filter
def get_photos(photo):
	photo=str(photo).split(',')
	return photo[0]

# @register.filter
# def get_videos(video):
# 	video=str(video).split(',')
# 	return video[0]

@register.filter
def get_videos(video):
	if "=" in str(video):
		video=str(video).split('=')
		return "https://www.youtube.com/embed/"+video[1]
	else:
		return str(video)

@register.filter
def get_categories(initial_load):
	category=Category.objects.all()
	return category

@register.filter
def get_subcategories(categoryId):
	subcategories = SubCategory.objects.filter(category_id=categoryId)
	return subcategories

@register.filter
def get_subcategoriesCount(subCategoryId):
	subcategoriescounts = Product.objects.filter(subcategory_id=subCategoryId, status_isactive=1).count()
	# subcategoriescounts = Product.objects.filter(subcategory_id=subCategoryId).annotate(Count('subcategory'))
	return subcategoriescounts

@register.filter
def get_brandforsubcategory(subCategoryId):
	brandforsubcategory = Dropdown.objects.filter(subcat__id=subCategoryId).exclude(brand_name='')
	return brandforsubcategory

@register.filter
def get_banner(banner):
	banners=PostBanner.objects.filter(admin_status = 1)
	# print banners
	return banners

@register.filter
def conversion(price):
	return convert(price)

@register.filter
def get_symbol(country):
	return currency_symbol(country)

@register.filter
def quantize(value,arg=None):
	"""
	Takes a float number (23.456) and uses the
	decimal.quantize to round it to a fixed
	exponent. This allows you to specify the
	exponent precision, along with the
	rounding method.

	Examples (assuming value="7.325"):
	{% value|quantize %} -> 7.33
	{% value|quantize:".01,ru" %} -> 7.33 (this is the same as the default behavior)
	{% value|quantize:".01,rd" %} -> 7.32

	Available rounding options (taken from the decimal module):
	ROUND_CEILING (rc), ROUND_DOWN (rd), ROUND_FLOOR (rf), ROUND_HALF_DOWN (rhd),
	ROUND_HALF_EVEN (rhe), ROUND_HALF_UP (rhu), and ROUND_UP (ru)

	Arguments cannot have spaces in them.

	See the decimal module for more info:
	http://docs.python.org/library/decimal.html
	"""
	num=decimal.Decimal(str(value))
	options=["ru","rf","rd","rhd","rhe","rhu"]
	precision=None;rounding=None
	if arg:
		args=arg.split(",")
		precision=args[0]
		rounding=str(args[1])
	if not precision: precision=".01"
	if not rounding: rounding=decimal.ROUND_UP
	if rounding not in options: rounding=decimal.ROUND_UP
	if rounding=="ru":rounding=decimal.ROUND_UP
	elif rounding=="rf": rounding=decimal.ROUND_FLOOR
	elif rounding=="rd": rounding=decimal.ROUND_DOWN
	elif rounding=="rhd": rounding=decimal.ROUND_HALF_DOWN
	elif rounding=="rhe": rounding=decimal.ROUND_HALF_EVEN
	elif rounding=="rhu": rounding=decimal.ROUND_HALF_UP
	newnum=num.quantize(decimal.Decimal(precision),rounding=rounding)
	return newnum
