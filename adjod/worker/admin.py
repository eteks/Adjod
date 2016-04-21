from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.http import HttpResponse, Http404

import models
# from actors.models import Actor

from dateutil import tz
#from_zone = tz.tzutc()
to_zone = tz.tzlocal()

class WorkerAdmin(admin.ModelAdmin):
  fields = ['name','cls_path', 'interval','wait_for_approval','notify_for_approval','notify_for_errors']
  list_display = ('id', 'name', 'interval', 'wait_for_approval', 'active')
  list_filter = ['name', 'active']
  search_fields = ['name', 'cls_path', 'interval', 'wait_for_approval', 'active']

  def has_add_permission(self, request):
      return False
  def get_readonly_fields(self, request, obj=None):
      return self.readonly_fields + ('id', 'name','cls_path')


class WorkerTaskAdmin(admin.ModelAdmin):
  list_display = ('id', 'worker', 'notes', 'worker_options', 'status', 'completed', 'modified')
  list_filter = ['worker', 'status']
  search_fields = ['worker', 'notes', 'worker_options', 'status']

  list_per_page = 100

class UserTrackingAdmin(admin.ModelAdmin):
  fields = [ 'track_alert', 'email_sent_count', 'email_read_count', 'email_view_count', 'recent_email_fail_count', 'last_email_sent']
  list_display = ('id', 'track_alert', 'email_sent_count', 'email_read_count', 'email_view_count', 'recent_email_fail_count', 'last_email_sent')
  list_filter = ['recent_email_fail_count']
  search_fields = ['track_alert', 'last_email_sent']

  list_per_page = 100
  def has_add_permission(self, request):
      return False

  def has_delete_permission(self, request):
      return False

  def get_readonly_fields(self, request, obj=None):
      return self.readonly_fields + ('id', 'track_alert', 'email_sent_count', 'email_read_count', 'email_view_count', 'recent_email_fail_count', 'last_email_sent')

class WorkerNoticeEmailTaskAdmin(admin.ModelAdmin):
  fields = ['task','created_alert','product','tracking_code','iteration_count']
  list_display = ('id','task','created_alert','tracking_code','iteration_count')
  list_filter = ['product']
  search_fields = ['product', 'tracking_code']

  list_per_page = 100
  def has_add_permission(self, request):
      return False

  def has_delete_permission(self, request):
      return False

  def get_readonly_fields(self, request, obj=None):
      return self.readonly_fields + ('id','task','created_alert','product','tracking_code','iteration_count')

class ProductExpiredAdTrackingAdmin(admin.ModelAdmin):
  fields = ['product','email_sent_count','last_email_sent']
  list_filter = ['product']
  list_display = ('id','product','email_sent_count','last_email_sent')
  search_fields = ['product']

  list_per_page = 100
  def has_add_permission(self, request):
      return False

  def has_delete_permission(self, request):
      return False

  def get_readonly_fields(self, request, obj=None):
      return self.readonly_fields + ('id','product','email_sent_count','last_email_sent')

admin.site.register(models.Worker, WorkerAdmin)
admin.site.register(models.WorkerTask, WorkerTaskAdmin)
admin.site.register(models.UserTracking,UserTrackingAdmin)
# admin.site.register(models.NoticeEmailConfig)
admin.site.register(models.WorkerNoticeEmailTask,WorkerNoticeEmailTaskAdmin)
# admin.site.register(models.ProductEmailTracking)
admin.site.register(models.ProductExpiredAdTracking,ProductExpiredAdTrackingAdmin)
