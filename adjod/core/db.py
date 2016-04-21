import logging
from core import helper

def import_defaults(sender, **kwargs):
  """
  Whenever new database is created (afterdb), 'default_data' static method
  is called from each model. Its optional to have 'default_data' for each
  model. This method can be used to import default data for each model whenever
  the database is created
  
  Example Usage: 
  On Actor Model defintion, add the following code
  
  @staticmethod
  def default_data():
  
    # Saving default actor 1
    Actor(email='roger@fixido.com').save()
    
    # Saving default actor 2
    actor2 = Actor(email='roacket@fixido.com')
    actor2.address = "moon, universe, milkyway - 23813"
    actor2.save()

  """  
  for name, model in helper.get_local_models().iteritems():
    init_function = getattr(model, 'default_data', None)    
    if init_function:
      print(">> Importing Default Data for : %s" % model.__name__)
      init_function()