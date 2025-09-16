
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from moneyheist.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
#from moneyheist.tokens import TokenGenerator
from .models import UserProfile
from moneyheist import settings
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime
from .models import generate_ref_code
from .models import Video
from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse
# Create your views here.
import requests
def welcome(request):
    return render(request, 'ttt.html')

def net(request):

    return render(request, 'net.html')

def speednet(request):
    return render(request, 'speednet.html')
def withdraw(request):
    return render(request, 'withdraw.html')

def mpesa(request):
    cl = MpesaClient()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer H3akuW16S4M1vgLQntBZUQZCXT6Z'
    }
    payload = {
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjUwOTE0MTkzNDU2",
        "Timestamp": "20250914193456",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254713968142,
        "PartyB": 174379,
        "PhoneNumber": 254713968142,
        "CallBackURL": "http://127.0.0.1:8000/mpesa",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X" 
    }
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, data = payload)
    print(response.text.encode('utf8'))
    return HttpResponse("SUccess")

    """eaders = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer 6xqLI5iorRDvpZp7nmIGk3L1YI7H'
    }

    payload = {
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjQwMjExMTQwNjQw",
        "Timestamp": "20240211140640",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254713968142,
        "PartyB": 174379,
        "PhoneNumber": 254713968142,
        "CallBackURL": "https://mydomain.com",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X" 
      }
    response = requests.request("POST", 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers = headers, json = payload)
    print(response.text.encode('utf8'))
    return HttpResponse(response)
    
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0713968142'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = ' http://127.0.0.1:8000/mpesa'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)
    #return redirect('signin')
    """
def rewards(request):
    return render(request, 'rewards.html')

from django.shortcuts import render, redirect
from .models import PhoneAPI

def about(request):
    return render(request, 'about.html' )
def config_net(request):
    if request.method == 'POST':
        ip_address = request.POST.get('ipaddress', '')

        if ip_address:
            phone_api = PhoneAPI.objects.create(ip_address=ip_address)
        
            # Optionally, you can do something after saving the phone API, such as redirecting to another page
            return redirect('speednet')  # Replace 'some_other_view_name' with the name of the view you want to redirect to


    return render(request, 'config_net.html')

def stk_push_callback(request):
        data = request.body
        
        return HttpResponse("STK Push in Django👋")

def index(request):
    return render(request, 'index.html' )


def finance(request):
    return render(request, 'finance.html' )

    
def online(request):
    return render(request, 'online.html' )

def make(request):
    return render(request, 'make.html' )

def mine(request):
    return render(request, 'mine.html' )

def videolist(request):
    videos = Video.objects.all()
    return render(request, 'watch.html', {'videos': videos})

def signin(request):
    if request.method=='POST':
        username=request.POST.get('username', '')
        password=request.POST.get('password', '')
    
        User=authenticate(username=username, password=password)


        
        if User is not None:
            name = username

            return render(request, 'index.html', {'name':name})
            """name=User.username
            profile = User.UserProfile
            referral_link = profile.get_referral_link()
            
            login(request,User)
            messages.success(request, 'login succesful')
            return render(request, 'index.html',  {'name':name, 'referral_link':referral_link} )"""

        
    
        else:
            messages.error(request, 'incorrect credentials')
    return render(request, 'login.html')

def activate(request):
    return render(request, 'index.html' )

@login_required(login_url="signin")
def profile(request, *args, **kwargs):
    refferal_code = str(kwargs.get('ref_code'))
    try:
        profile = UserProfile.objects.get(refferal_code=refferal_code)
        request.session['ref_profile'] = profile.id
        print("your id:", profile.id)

    except:
        messages.error(request, "Profile for user does not exist")

    print(request.session.get_expiry_age())
    return redirect('register')
def register(request):
    profile_id = request.session.get('ref_profile')
    print("Your Profile id:", profile_id)
    if request.method == 'POST':
    
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        #sg = sendgrid.SendGridAPIClient(api_key='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')

        if password != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists')
            return redirect('register')
        if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
        try:
            myuser = User.objects.create(username=username, email=email)

            if profile_id is not None:
                recommended_by_profile = UserProfile.objects.get(id=profile_id)
                myuser.is_active=True
                myuser.save()


                registered_user = User.objects.get(id = myuser.id)
                print(registered_user)

                registered_profile = UserProfile.objects.get(user = registered_user)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()

            else:
                myuser.is_active=True
                myuser.save()
                messages.error(request, "profile for user does not exist")

        except:
            messages.error(request, "An Error Occurred!!")
            return render(request, 'register.html')


            """#email welcoming
                subject=" welcome to money heist*kv* "
                message=" hello" + new_user.username + "\n" "welcome to we have sent a confirmation email bellow"
                from_email=settings.DEFAULT_FROM_USER
                to_list=[new_user.email]
                send_mail(subject, message, from_email, to_list, fail_silently=False)


                #email confirmation

                current_site=get_current_site(request)

                email_subject="confirm email"
                message2=render_to_string('email_confirmation.html',{
                    'name':new_user.username,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
                    #'token':TokenGenerator(new_user.username )
                })
                
                send_mail(email_subject, message2, from_email, to_list, fail_silently=True)"""

                
        return redirect('signin')

    else:
        return render(request, 'register.html')

@login_required
def display_referral_link(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    refferal_count = user_profile.refferal_count()
    referred_users = UserProfile.objects.filter(recommended_by = request.user)
    user_ref_code = user_profile.refferal_code
    user_ref_by = user_profile.recommended_by
    domain = get_current_site(request)

    context = {
        'created':created,
        'domain':domain,
        'user_ref_by':user_ref_by,
        'user_ref_code':user_ref_code,
        'refferal_count':refferal_count,
        'referred_users':referred_users
    }
    return render(request, 'index.html', context)
    

def config_net(request):
    return render(request, 'config_net.html')

def invited_friends(request):
    return render(request, 'invited_friends.html')


def financial_report(request):
    return render(request, 'finance.html')

def about_us(request):
    return render(request, 'about.html')

def sendemail(request):
    try:
            #email welcoming
                subject=" welcome to money heist*kv* "
                message=" hello"  "\n" "welcome to we have sent a confirmation email bellow"
                from_email=settings.DEFAULT_FROM_USER
                new_user = "thedesigncreative254@gmail.com"
                to_list=[new_user]
                send_mail(subject, message, from_email, to_list, fail_silently=False)


                #email confirmation

                """current_site=get_current_site(request)

                email_subject="confirm email"
                message2=render_to_string('email_confirmation.html',{
                    'name':new_user.username,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
                    #'token':TokenGenerator(new_user.username )
                })
                
                send_mail(email_subject, message2, from_email, to_list, fail_silently=True)"""
                return HttpResponse("Email sent succesfully")
    except:
        return HttpResponse("Error in  sending email!!")
