import logging
import time
import traceback

from datetime import datetime, timedelta
from django.utils.timezone import utc

from core import  helper
from models import *
from django.db.models import Q

class WorkerMaster(object):

  def __init__(self, heartbeat=2, debug=False):
    self.workers = {}
    self.handlers = {}
    self.heartbeat = heartbeat
    self.debug = debug


    if debug:
      root = logging.getLogger()
      # root.setLevel(logging.DEBUG)
      if root.handlers:        
        for handler in root.handlers:
          root.removeHandler(handler)

      logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

      # console = logging.StreamHandler()
      # console.setLevel(logging.INFO)
      # formatter = logging.Formatter('%(message)s')
      # console.setFormatter(formatter)
      # logging.getLogger().addHandler(console) 

      self.create_dummyworks()


  def create_dummyworks(self):
    print 'create_dummyworks'
    pass
    
    # from leads.models import Lead
    #Lead.objects.get(pk=3).save()

  def start(self):
    logging.info("Starting worker")
    logging.debug("Started with debug: " + str(self.debug))

    workers = Worker.objects.filter(active=True)

    for worker in workers:
      cls = helper.object_from_path(worker.cls_path, safe=True)
      if cls is None:

        logging.error("Class not found for "+ worker.name + ":" + worker.cls_path)
        continue

      self.workers[worker.id] = {
        'time': helper.get_now(),
        'next': worker.interval,
        'worker_obj': cls(worker),
        'worker': worker
      }

    self.loop()


  def loop(self):

    while True:
      t = helper.get_now()
      for work in self.workers.values():
        try:
          worker = work['worker']
          worker_obj = work['worker_obj']

          # d = work['time'] - t
          d = t - work['time']

          if d.seconds >= worker.interval:
            work['time'] = helper.get_now()

            worker_obj.create_tasks()

            tasks = WorkerTask.objects.filter(
              worker=worker, status='scheduled', scheduled__lte=t)
            worker_obj.runtasks(tasks)
        except Exception, e:
          if 'worker' in work:
            worker = work['worker']
            logging.error("Error while doing " + worker.name)
          else:
            logging.error("Error while doing work, worker object is misisng")
          logging.critical(e)
          traceback.print_exc()

      time.sleep(self.heartbeat)


    
