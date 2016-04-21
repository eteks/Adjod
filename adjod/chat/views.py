# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from chat.models import *
from django.contrib.sessions.models import Session
from django.shortcuts import render_to_response, HttpResponse, render
import datetime
import time
from adjod.models import *
from advertisement.models import *

@csrf_exempt
def find_online_users(userid):
    # print "userid", userid
    # print "datetime.datetime.now()", datetime.datetime.now()
    # print "datetime.timedelta(seconds=15)", datetime.timedelta(seconds=15)
    # print "result", datetime.datetime.now() - datetime.timedelta(seconds=15)
    # last_active_list = LastActive.objects.filter(received_at__gt = datetime.datetime.now() - datetime.timedelta(seconds=5))   
    last_active_list = LastActive.objects.filter(received_at__gt = datetime.datetime.now() - datetime.timedelta(seconds=5))
    print "last_active_list", last_active_list
    users_list = []
    for last_active in last_active_list:
        users_list.append(int(last_active.user.id)) 
        print "users_list", users_list
    users_list.remove(userid)
    user_product=None
    if users_list:
        userprofile=UserProfile.objects.filter(user__in=users_list)
        print "userprofile", userprofile
        user_product=Product.objects.filter(userprofile__in=userprofile)
        print "user_product", user_product
    if user_product:
        return ",".join(str(n) for n in user_product)
    else:
        return str(user_product)

def get(request):
    if not request.is_ajax():
        return  HttpResponse (" Not an AJAX request ")  
    if request.method == 'GET':              
        last_active = None
        try:
            last_active = LastActive.objects.get(user = request.user)
        except:        	
            last_active = LastActive.objects.create(user = request.user, session = Session.objects.get(session_key = request.session.session_key))
        last_active.save()
        
        chat_list = ChatMessage.objects.filter(receiver = request.user, is_read = False)
        print "chat_list", chat_list
        #session = Session.objects.get(session_key = request.session.session_key)        
        #print chat_list
        for chat in chat_list:  
            chat.is_read = True
            chat.save()
            print "chat status saved"
            return HttpResponse (chat.sender.first_name + ":" + chat.message)
    #print "========= After Scaling ==============="       
    return HttpResponse('ACTIVE:' + find_online_users(request.user.id))

# def get_product(request):
#     print "get_product"
#     print "users_list", request.GET.get('users_list')
#     users_list=request.GET.get('users_list')
#     user_group=[]

#     #only users
#     # for users_lists in request.GET.get('users_list').split(','):
#     #     print "users_list split", users_lists
#     #     userprofile=UserProfile.objects.get(user=users_lists)
#     #     user_group.append(int(userprofile.id))
#     # print "userprofile", user_group   
#     # return HttpResponse(",".join(str(n) for n in user_group))

#     #User with products
#     if not users_list:
#         print "none"
#         user_product=None  
#         return HttpResponse(user_product)     
#     else:
#         print "users available"
#         for users_lists in request.GET.get('users_list').split(','):
#             print "users_list split", users_lists
#             userprofile=UserProfile.objects.get(user=users_lists)
#             print "userprofile", userprofile
#             user_group.append(int(userprofile.id))
#         print "userprofile", user_group
#         user_product=Product.objects.filter(userprofile__in=user_group)
#         print "user_product", user_product
#         return HttpResponse(",".join(str(n) for n in user_product))

@csrf_exempt
def post(request):
    print "post"
    # time.sleep(2)
    if not request.is_ajax():
        HttpResponse (" Not an AJAX request ")
    if request.method == 'POST':
        if request.POST['message']:
            message = request.POST['message']
            print "message", message
            to_user = request.POST['to_user']
            print "to_user", to_user
            user_id=User.objects.get(first_name=str(to_user))
            print "user_id", user_id
            receiver = User.objects.get(id = user_id.id)
            print "receiver", receiver.id
            sender=User.objects.get(id = int(request.user.id))
            print "sender", sender.id
            # ChatMessage.objects.create(sender = request.user.id, receiver = User.objects.get(username = to_user), message = message,  session = Session.objects.get(session_key = request.session.session_key))
            ChatMessage.objects.create(sender = User.objects.get(id = sender.id), receiver = User.objects.get(id = receiver.id), message = message,  session = Session.objects.get(session_key = request.session.session_key))    
    return HttpResponse ("POST request ")

def store_user_active_list(request):
    print "request.GET.get('user_id')", request.GET.get('user_id')

@csrf_exempt
def store_chat_record(request):
    import json
    print "request.POST['data']", request.POST['data']
    data = json.loads(request.POST['data'])  
    print "data" , len(data.keys())
    if len(data.keys()) <= 1:
        return HttpResponse('chat record not stored successfully')
    else:
        print "data['sender']", data['sender']
        print "data['receiver']", data['receiver']
        print "data['message']", data['message']
        print "data['product']",data['product']
        # sender=User.objects.get(username=data['sender'])
        # print "sender", sender
        # receiver=User.objects.get(username=data['receiver'])
        # print "receiver", receiver
        # ChatMessage.objects.create(sender = UserProfile.objects.get(user=sender.id), receiver = UserProfile.objects.get(user=receiver.id), message = data['message'])
        product=Product.objects.get(id=data['product'])
        chatmessage =ChatMessage()
        chatmessage.sender = data['sender']
        chatmessage.receiver = data['receiver']
        chatmessage.product=product
        chatmessage.message=data['message']
        chatmessage.sender_image=data['sender_image']
        chatmessage.receiver_image=data['receiver_image']
        chatmessage.save()
        # ChatMessage.objects.create(sender = data['sender'], receiver =  data['receiver'],product=product.id, message = data['message'])
        print "store_chat_record successfully"
        return HttpResponse('chat record stored successfully')

