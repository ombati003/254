
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
#from moneyheist.tokens import TokenGenerator
from .models import Profile, Referral
from moneyheist import settings
from django.core.mail import EmailMessage
from referral.models import UserReferrer
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
    

    """headers = {
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
    return HttpResponse(response)"""
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0713968142'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = ' http://127.0.0.1:8000/mpesa'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)
    #return redirect('signin')
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
            name=User.username
            profile = User.profile
            referral_link = profile.get_referral_link()
            
            login(request,User)
            messages.success(request, 'login succesful')
            return render(request, 'index.html',  {'name':name, 'referral_link':referral_link} )

        
    
        else:
            messages.error(request, 'incorrect credentials')
    return render(request, 'login.html')

def activate(request):
    return render(request, 'index.html' )

def register(request):
    ref_code = request.GET.get('ref_code')
    if request.method == 'POST':
    
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        #sg = sendgrid.SendGridAPIClient(api_key='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')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exists')
                return redirect('register')
            else:
                new_user = User.objects.create_user(username, email, password)
                # Create a profile for the new user
                #profile = Profile.objects.create(user=new_user, code=ref_code)
                #Profile.objects.create(user=new_user, code=ref_code)
                if ref_code:
                    try:
                        profile = Profile.objects.get(code=ref_code)
                        # Save the referral information
                        referral_date_time = datetime.now()
                        Referral.objects.create(referred_by=profile.user, referred_user=new_user, referral_date_time=referral_date_time)
                    except Profile.DoesNotExist:
                        pass
                messages.success(request, 'Registration successful. Please verify your email to login log in.')
                new_user.is_active = True
                new_user.save()

            

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
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
    else:
        return render(request, 'register.html')

def main_view(request, *args, **kwargs):
    code=str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile']=profile.id
        print('id', profile.id)

         # Save the referral information
        referral_date_time = datetime.now()
        Referral.objects.create(referred_by=profile.user, referred_user=request.user, referral_date_time=referral_date_time)
        #referred_users = request.user.profile.referred_users.all()
        #UserReferrer.objects.create(referred_by=profile.user, referred_user=request.user, referral_date_time=referral_date_time)
        
    
    except Profile.DoesNotExist:
        profile=None
        
    print(request.session.get_expiry_date())

    return render(request, 'register.html', {'ref_profile':profile})

def my_user_creation_view(request):
    ref_profile_id = request.session.get('ref_profile')
    if ref_profile_id:
        try:
            referrer_profile = Profile.objects.get(id=ref_profile_id)
            
            UserReferrer.objects.apply_referrer(User, referrer_profile.user, request)
        except Profile.DoesNotExist:
            pass

        return redirect('signin')

    return redirect('index')  

def create_profile(sender, instance, created, **kwargs):
    if created and not Profile.objects.filter(user=instance).exists():
        Profile.objects.create(user=instance)


@login_required
def display_referral_link(request):
    profile = Profile.objects.get(user=request.user)
    referral_link = profile.get_referral_link()
    return render(request, 'index.html', { 'referral_link': referral_link})
    

def config_net(request):
    return render(request, 'config_net.html')

def invited_friends(request):
    return render(request, 'invited_friends.html')


def financial_report(request):
    return render(request, 'finance.html')

def about_us(request):
    return render(request, 'about.html')
@login_required
def referred_users(request):
    profile = Profile.objects.get(user=request.user)
    referrals = Referral.objects.filter(referred_by=profile.user)
    referred_users = [referral.referred_user for referral in referrals]
    return render(request, 'invited_friends.html', {'referred_users': referred_users})


"""def invited_friends(request):
    try:
        profile = request.user.profile
        referred_users = profile.referred_users.all()
        return render(request, 'invited_friends.html', {'referred_users': referred_users})
    except Profile.DoesNotExist:
        # Handle the case where the user doesn't have a profile
        return render(request, 'index.html')  # Replace with your custom template or logic"""
   
    #referred_users = request.user.profile.referred_users.all()
    #return render(request, 'invited_friends.html')  {'referred_users': referred_users})

@login_required
def referred_users(request):
    profile = Profile.objects.get(user=request.user)
    referred_users = profile.referred_users.all()
    return render(request, 'referred_users.html', {'referred_users': referred_users})




