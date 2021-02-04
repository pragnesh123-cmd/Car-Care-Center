from django.shortcuts import render,redirect
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
        try:
            if customer.objects.get(email = request.POST['email']):
                mail = "Already Registered with this email!"
                return render(request,"car/customerregister",{"mail":mail})
        except:
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
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            user =  customer.objects.get(email=email,password=password)
            if user:   
                request.session['user'] = user.fname
                return redirect('customer_dashboard')
        except:
            email = "invalid Login Credintials"
            return render(request,"car/login.html",{"text":email})           
    else:
            return render(request,"car/login.html")


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
def customer_dashboard(request):
    return render(request,"car/customer_dashboard.html")
def invoice(request):
    return render(request,"car/customer_invoice.html")
def service(request):
    return render(request,"car/customer_request.html")
def customer_view_request(request):
    return render(request,"car/customer_view_request.html")
def customer_add_request(request):
    return render(request,"car/customer_add_request.html")
def customer_view_approved_request(request):
    return render(request,"car/customer_view_approved_request.html")
def customer_approved_request_bill(request):
    return render(request,"car/customer_view_approved_request_bill.html")
def customer_logout(request):
    if user in request.session:
        del request.session['user']
    return redirect('customerlogin')