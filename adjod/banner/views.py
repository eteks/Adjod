# Create your views here.
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from banner.models import BannerPlan
from django.http import HttpResponseRedirect, HttpResponse
#Generate JSON documents
from django.utils import simplejson
import simplejson as json

@csrf_exempt
def get_banner_height_width(request):
	if request.method == 'POST':
		banner_plan = BannerPlan.objects.get(id=request.POST.get('selected_option'))
		results = {'banner_height':banner_plan.height, 'banner_width':banner_plan.width}
		return HttpResponse(simplejson.dumps(results), mimetype='application/json')
