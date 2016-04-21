from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


class Command(BaseCommand):
  option_list = BaseCommand.option_list + (
      make_option('--debug', action='store_true', dest='debug', 
        default=False, help='Run the worker in debug mode'),
      make_option('--heartbeat', dest='heartbeat', 
        default=2, help='heartbeat for worker in seconds'),
    )

  def handle(self, *args, **options):
    from ... import WorkerMaster

    debug = options['debug']
    heartbeat = float(options['heartbeat'])

    worker = WorkerMaster(heartbeat=heartbeat, debug=debug)
    worker.start()