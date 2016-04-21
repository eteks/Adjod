import threading
globals = threading.local()

#For finding user global ip, that is internet ip address
def user_ip():
  if hasattr(globals, 'ip'):
    return globals.ip
  else:
    return None