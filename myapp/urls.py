from django.urls import path, include
from . import views


urlpatterns=[
    path('net', views.net, name='net'),
    path('about', views.about, name='about'),
    path('speednet', views.speednet, name='speednet'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('welcome', views.welcome, name='welcome'),
    path('mpesa', views.mpesa, name='mpesa'),
    path('rewards', views.rewards, name='rewards'),
    path('daraja/stk-push', views.stk_push_callback, name='mpesa_stk_push_callback'),
    path('finance', views.finance, name='finance'),
    path('make', views.make, name='make'),
    path('online', views.online, name='online'),
    path('videolist', views.videolist, name='videolist'),
    path('mine', views.mine, name='mine'),
    path('register', views.register, name='register'),
    path('', views.index, name='index'),
    path('signin', views.signin, name='signin'),
    path('sendemail', views.sendemail, name='sendemail'),
    path('display_referral_link/', views.display_referral_link, name='display_referral_link'),
    path('<str:ref_code>/', views.profile, name='profile'),
    path('activate/<uid64>/<token>', views.activate, name='activate'),
    #path('mk', include('MpesaApiDemo.urls')),
    path('config_net', views.config_net, name='config_net'),
    path('invited_friends', views.invited_friends, name='invited_friends'),
    path('financial_report/', views.financial_report, name='financial_report'),
    path('about_us/', views.about_us, name='about_us'),
    
]