"""CarCareCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CCC import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('home/', views.home),

    path('aboutus/',views.aboutus),
    path('contactus/', views.contactus),
    path('trackorder/',views.trackorder),
    path('register/',views.register),
    # path('customerbase',views.customerlogin),
    path('changepassword',views.changepassword,name="changepassword"),
    path('forgotpassword',views.forgotpassword),

    # Customer Url
    path('customerbase',views.customerbase,name ='customerbase'),
    path('login',views.customerlogin,name='customerlogin'),
    path("customer_dashboard",views.customer_dashboard , name='customer_dashboard'),
    path("invoice" ,views.invoice),
    path("service",views.service),
    path("customer_view_request",views.customer_view_request,name='customer_view_request'),
    path("customer_add_request",views.customer_add_request,name='customer_add_request'),
    path("customer_view_approved_request",views.customer_view_approved_request),
    path("customer_approved_request_bill",views.customer_approved_request_bill),
    path("customer_logout",views.customer_logout,name="customer_logout"),
    path("del_customer_request/<int:id>",views.del_customer_request,name='del_customer_request'),
    path('customer_feedback',views.customer_feedback),
    path('customer_profile',views.customer_profile),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('check_otp',views.check_otp,name="check_otp"),
    path('forgotpasschange',views.forgotpasschange,name="forgotpasschange"),

    #Mechanic URL

    path('mechaniclogin',views.mechaniclogin,name='mechaniclogin'),
    path('mechanic_base',views.mechanic_base,name='mechanic_base'),
    path('mechanicindex',views.mechanicindex,name = 'mechanicindex'),
    path('mechanic_service',views.mechanic_service,name='mechanic_service'),
    path('mechanic_feedback',views.mechanic_feedback,name='mechanic_feedback'),
    path('mechanic_update_status/<int:id>',views.mechanic_update_status,name='mechanic_update_status'),
    path('mechanic_logout',views.mechanic_logout),
   
]
