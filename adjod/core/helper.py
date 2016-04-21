import logging
from datetime import datetime
from django.conf import settings
from django.db.models import get_app, get_models
from django.utils.timezone import utc
from hashlib import sha512
from uuid import uuid4

def get_local_models():
  models = {} 
  for app_name in settings.INSTALLED_APPS:
    if '.' not in app_name: #FIXIT: find a better way to identify if the app is local
      app = get_app(app_name)
      for model in get_models(app):
        name = "%s.%s" % (app_name,model.__name__)
        models[name] = model
  return models

def get_now():
  return datetime.utcnow().replace(tzinfo=utc)

def import_from_string(cls_path, safe=False):
  try:
    mod = __import__(cls_path)
    components = cls_path.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
  except ImportError as error:
    if safe:
      return None
    else:
      raise error

def object_from_path(path, safe=False):
  location = path.split('.')
  class_name = location[-1]
  location.remove(class_name)
  location = '.'.join(location)
  cls = import_from_string(location, safe)
  if cls:
    if safe:
      if hasattr(cls, class_name):
        return getattr(cls, class_name)
      else:
        return None
    else:
      return getattr(cls, class_name)
  else:
    return None

def randomkey(length=32):
  return sha512(uuid4().hex).hexdigest()[0:length]

def image_resize(imagefield, size=None, 
  quality=90, formate="JPEG", extension="jpg"):
    image_path = imagefield.path
    if not size:
      size = settings.LEAD_THUMB_IMAGE_SIZE
    try:
        import Image
    except ImportError:
        try:
            from PIL import Image
        except ImportError:
            raise ImportError('Cannot import the Python Image Library.')
    image = Image.open(imagefield.path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.thumbnail(size, Image.ANTIALIAS)
    image.save(image_path, formate, quality=quality)