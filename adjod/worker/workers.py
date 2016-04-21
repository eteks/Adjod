import logging
import time
import traceback
import operator
from datetime import datetime, timedelta
from models import *
from django.conf import settings
from django.contrib.sites.models import Site
from advertisement.models import *
# from freealert import *
from templated_email import send_templated_mail
from core import helper
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
# from actors import globals as glb #couldn't work w/o request
from django.utils.encoding import smart_str
class WorkerBase(object):

  def __init__(self, worker):
    self.worker = worker

  def create_tasks(self):
    pass

  def prepare(self):
    pass

  def runtasks(self, tasks):
    pass

  def finish(self):
    pass

class EmailNotificationWorker(WorkerBase):  

  def create_tasks(self):    
    print "create_tasks1"
    workertask=WorkerTask.objects.get(worker=self.worker)
    workertask.status='init'
    workertask.save()   
    print "self.worker", self.worker.id
    tasks = WorkerTask.objects.filter(worker=self.worker, status='init')
    print "tasks", tasks
    for task in tasks:
      print "task.worker", task.worker
    # config = NoticeEmailConfig.objects.get(pk='default')
    if tasks.count():
      print "Got tasks", tasks.count()
    for task in tasks:
      try:
        now  = helper.get_now()
        if self.worker.wait_for_approval:
          now = now + timedelta(seconds = self.worker.wait_for_approval)
        task.scheduled = now
        task.status = 'scheduled'
        task.save()

        # logging.debug("scheduled Lead for notice email : " + ntask.product.title)
      except Exception, e:
        logging.critical(e)
        traceback.print_exc()
        task.status = 'failed'
        task.notes = "Error while creating task " + traceback.format_exc()
        task.save() 
   
  def runtasks(self, tasks):
    print "runtasks1"
    freealert=FreeAlert.objects.all()   
    for task in tasks:
      now = helper.get_now()
      task.status = 'started'
      task.started = now
      task.save()
      try:
        now  = helper.get_now()
        yesterday = now - timedelta(seconds=5)
        # yesterday = now - timedelta(hours=24)
        print "task", task

        for freealerts in freealert:   
          if freealerts.last_email_sent!= datetime.datetime.now().time():
            alert_id = Product.objects.all()
            alert_filter = Product.objects.filter(category_id=freealerts.alert_category_id, subcategory_id=freealerts.alert_subcategory_id,city_id=freealerts.alert_city_id,ad_brand_id=freealerts.alert_brand_id)             
            product=[]
            for alert_filters in alert_filter:
              if UserTracking.objects.filter(track_alert=freealerts.id):
                print "enter if"
                usertrack= UserTracking.objects.get(track_alert=freealerts.id)    
                usertrack.email_sent_count +=1              
                usertrack.last_email_sent=now
                usertrack.save()
              else:
                print "enter else"
                print "freealerts.id", freealerts.id
                usertracking=UserTracking()
                usertracking.track_alert=FreeAlert.objects.get(id=freealerts.id)
                usertracking.email_sent_count +=1            
                usertracking.last_email_sent=now
                usertracking.save()
                task.status = 'completed'
                task.completed = helper.get_now()
                task.save()
            print "alert_filter",alert_filter
            content = "http://" + settings.SITE_NAME + "/ads/" 
            print content,"content"
            print freealerts.alert_email
            cate = freealerts.alert_category.name
            print "cate",cate            
            current_site = Site.objects.get(id=1)              
            user=str(freealerts.alert_user.username)
            print "user",user
            ctx={'cate':cate,'alert_filter':alert_filter, 'content':content ,'user':user}
            print freealerts.alert_email,"freealerts.alert_email"
            self.send_mail(content, freealerts.alert_email,ctx)
            freealerts.mail_is_sent=True
            freealerts.last_email_sent=now
            freealerts.save()
            
            if WorkerNoticeEmailTask.objects.get(created_alert=freealerts.id):    
              ntask=WorkerNoticeEmailTask.objects.get(created_alert=freealerts.id)      
            else:
              ntask=WorkerNoticeEmailTask()
              ntask.task=task
              ntask.created_alert=FreeAlert.objects.get(id=freealerts.id)          
              ntask.tracking_code=helper.randomkey(26)
              ntask.iteration_count+=1
              ntask.mailissent = 1
              ntask.last_email_sent=now
              ntask.save()
              ntask.product = product
            
          else:
            print "cron again occur as today's date"
        
      except Exception, e:
        logging.critical(e)
        traceback.print_exc()
        task.status = 'failed'
        task.notes = "Error while running task " + traceback.format_exc()
        task.save()

  def send_mail(self, content, email,ctx):
    current_site = Site.objects.get(id=1),
    send_templated_mail(
              template_name = 'alert',
              from_email = 'testmail123sample@gmail.com',
              recipient_list= [email],
              context = ctx,
            )
    print "mail sent successfully"

  
class EmailNotification_ExpiredAds(WorkerBase):

  def create_tasks(self):    
    print "create_tasks"
    now  = helper.get_now() 
    product=Product.objects.all()

    for products in product:
      user_id = str(products.userprofile.user_ptr_id)
      user=str(products.userprofile.username)
      product_id = str(products.id)
      cat=str(products.category.name)
      subcat=str(products.subcategory.name)
      brand=str(products.ad_brand.brand_name)
      title=str(products.title)
      print "cat",cat
      print subcat
      print brand
      print title
      print "user",user
      print "user_id", user_id
      print "product_id", product_id
      result=(products.expired_date -  products.created_date).days
      print "result", result
      remaining_days = 30 - result
      if result >=25 and result < 30:       
        # subject="Your " + str(products.title) + " ads will be expired in " + repr(remaining_days) + " days"
        content="If u want 10 more days to be active your ads please click the link http://localhost:8000/expired_ad_conformation/?" +"user_id=" + user_id + "&ad_id=" + product_id + ", otherwise if you want to remove ads please click this link http://localhost:8000/expired_ad_conformation/?" +"user_id=" + user_id + "&ad_id=" + product_id 
        con=content
        print "con",con
      elif result == 30:
        products.expired_date = products.expired_date + datetime.timedelta(days=10)       
        # subject="Your " + str(products.title) + " ads is expired"
        content="If u want 10 more days to be active your ads please click the link http://localhost:8000"               
        con1=content
        print "con1" ,con1    
      elif result == 40:
          # subject = "Your " + str(products.title) + " ads is expired after some extra period"
          content= "Hi...Your ad is going to be inactive, Click the blow link and Please make your ad as Premium http://localhost:8000"
      active_link = "http://" + settings.SITE_NAME + "/postad/"
      products.status_isactive = False      
      ctx={'cat':cat,'subcat':subcat ,'brand':brand,'title':title,'user':user,'active_link':active_link}       
      self.sendmail(title, products.you_email,ctx)
      products.save()
        
  
  def runtasks(self, tasks):
    print "runtasks"

  def sendmail(self, title, email,ctx):
      current_site = Site.objects.get(id=1),
      send_templated_mail(
             template_name = 'product_alert',
             from_email = 'testmail123sample@gmail.com',
             recipient_list = [email],
             context = ctx,
        )
      print "mail successfully"