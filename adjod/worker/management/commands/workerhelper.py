from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
  help = "Util functions for worker"

  option_list = BaseCommand.option_list + (
      make_option('--init', action='store_true', dest='init', 
        default=False,help='Init worker settings'),
      make_option('--cleartasks', dest='cleartasks', help='Clear tasks of given lead id and create new one'),
    )


  def handle(self, *args, **options):
    # if options['init']:
    #   self.initworker()
    pass


  # def initworker(self):
  #   from ...models import Worker

  #   workers = Worker(id='freealert_notice_email')
  #   worker.name = 'Freealert Notice Email'
  #   worker.cls_path = 'worker.workers.EmailNotificationWorker'
  #   worker.save()