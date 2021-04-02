
from django.urls import path,include
from . import views 
from django.contrib.auth import  views as auth_view


urlpatterns = [
    path('', views.dashboard, name='user-dashboard'),
    path('ref/<str:ref_code>/', views.dashboard, name="ref"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout_view, name='logout'),
    path('register/', views.registration_view, name='register'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),  
    path('verify/', views.email_temp, name='email_temp'),
    path('dashboard/', views.account, name='account'),
    path('deposite/', views.deposite, name='deposite'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transferlogs/', views.tranfer_log, name='tranfer_log'),
    path('referral/', views.account_refferal, name='account_refferal'),
    path('packages/', views.package, name='packages'),
    path('my-package/', views.my_package, name='my-packages'),
    path('my-notification/', views.notification, name='notification'),
    path('account-setup/', views.account_setup, name='account-setup'),




    

    #path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),

    
]