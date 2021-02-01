from django.shortcuts import render
from .models import *


# Create your views here.

def index(request):
    return render(request,"car/index.html")

def home(request):
    return render(request,"car/index.html")

def login(request):
    return render(request,"car/login.html")

def aboutus(request):
    return render(request,"car/about-us.html")

def contactus(request):
    return render(request, "car/contact-us.html")

def trackorder(request):
    return render(request,"car/track-order.html")

def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        password = request.POST.get('password')
        reg = customer(fname = fname,lname=lname,email=email,mobile_no=mobile_no,gender=gender,address=address,password=password)
        reg.save()
        text = "You have Successfully Registred!"
        return render(request,"car/customerregister.html",{"text":text})
    else:
        return render(request,"car/customerregister.html")

def customerlogin(request):
    return render(request,"car/account-login.html")


def changepassword(request):
    return render(request,"car/change-password.html")

def forgotpassword(request):
    return render(request,"car/forgotpassword.html")


#======================================================================#
#                  Customer Related Views                              #
#======================================================================#

def customerbase(request):
    return render(request,"car/customerindex.html")
def feedback(request):
    return render(request,"car/feedback.html")
