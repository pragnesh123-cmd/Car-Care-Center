from django.shortcuts import render,redirect
from .models import *
from django.db.models import Sum
import math
import random
import smtplib
from django.core.mail import send_mail
from django.conf import settings



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
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        msg = request.POST.get('msg')
        contacts = contact(name=name,email=email,msg=msg)
        contacts.save()
        return render(request,"car/contact-us.html")
    else:
        return render(request,"car/contact-us.html")
         
def trackorder(request):
    return render(request,"car/track-order.html")

def changepassword(request):
    return render(request,"car/change-password.html")

def check_otp(request):
    if request.method == 'POST':
        otppass = request.POST.get('otppass')
        if otppass==request.session['otp']:
            return redirect('forgotpasschange')
        else:
            text = "you have entered wrong otp..!"
            return render(request,'car/otp_check.html',{'otp':text})
    else:   
        return render(request,"car/otp_check.html")

def forgotpasschange(request):
    if request.method == 'POST':
        newpass = request.POST.get('newpass')
        customer.objects.all().filter(email = request.session['email']).update(password=newpass)
        del request.session['email']
        text = 'Your Password has Succesfully Change!'
        return redirect('customerlogin')
    else:
        return render(request,'car/forgot_password_change.html')

#======================================================================#
#                  Customer Related Views                              #
#======================================================================#

def customerbase(request):
    return render(request,"car/customerindex.html")

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
            mobile = request.POST.get('mobile_no')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            password = request.POST.get('password')
            reg = customer(fname = fname,lname=lname,email=email,mobile=mobile,gender=gender,address=address,password=password)
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
def customer_feedback(request):
    if request.method == 'POST':    
        if 'user' in request.session:
            cust = customer.objects.get(fname = request.session['user'])
            username = request.POST.get('username')
            email = request.POST.get('email')
            msg = request.POST.get('msg')
            feed = feedback(username=username,email=email,msg=msg)
            feed.save()
            return render(request,"car/feedback.html",{'user':cust})
        else:
            return redirect('customerlogin')     

    else:
        if 'user' in request.session:
            cust = customer.objects.get(fname = request.session['user'])
            return render(request,"car/feedback.html",{'user':cust})
        else:
            return redirect('customerlogin')
   
from django.db.models import Q
def customer_dashboard(request):
    if 'user' in request.session:
        cust = customer.objects.get(fname = request.session['user'])
        count_req = cus_request.objects.filter(Customer_id=cust.id).count()
        work_in_progress = cus_request.objects.all().filter(Customer_id = cust.id,status='Repairing').count()
        work_in_completed = cus_request.objects.all().filter(Customer_id = cust.id).filter(Q(status='Repairing Done') | Q(status = 'Released')).count
        bill = cus_request.objects.all().filter(Customer_id = cust.id).filter(Q(status='Repairing Done') | Q(status = 'Released')).aggregate(Sum('cost'))
        dict = {
            "user":cust,
            "count_req":count_req,
            'work_in_progress':work_in_progress,
            'work_in_completed':work_in_completed,
            'bill': bill['cost__sum']
        }
        return render(request,"car/customer_dashboard.html" ,context=dict)
    else:
        return redirect('customerlogin')
def invoice(request):
    if 'user' in request.session:
        cust = customer.objects.get(fname = request.session['user'])
        enquiry = cus_request.objects.all().filter(Customer_id = cust.id).exclude(status = 'Pending')
        return render(request,"car/customer_invoice.html" ,{"user":cust,'enquiry':enquiry})
    else:
        return redirect('customerlogin')
def service(request):
    if 'user' in request.session:
        cust = customer.objects.get(fname = request.session['user'])
        return render(request,"car/customer_request.html",{"user":cust})
    else:
        return render('customerlogin')
def customer_view_request(request):
    if 'user' in request.session:
        cust = customer.objects.get(fname = request.session['user'])
        enqiry = cus_request.objects.all().filter(Customer_id = cust.id, status="Pending")
        return render(request, "car/customer_view_request.html",{"user":cust,"enquiry":enqiry})
    else:
        return render('customerlogin')

def customer_add_request(request):
    if request.method == 'POST':
        if 'user' in request.session:
            cust = customer.objects.get(fname=request.session['user'])
            category = request.POST.get('category')
            number = request.POST.get('number')
            name = request.POST.get('name')
            brand = request.POST.get('brand')
            model = request.POST.get('model')
            problem = request.POST.get('problem')
            cust = customer.objects.get(fname=request.session['user'])
            req = cus_request(category=category,number=number,name=name,brand=brand,model=model,problem=problem,Customer_id=cust.id)
            req.save()
            return render(request,"car/customer_add_request.html",{"user":cust})
        else:
            return redirect("customerlogin")
    else:
        if 'user' in request.session:
            cust = customer.objects.get(fname=request.session['user'])
            return render(request,"car/customer_add_request.html",{"user":cust})
        else:
            return redirect("customerlogin")

def customer_view_approved_request(request):
    if 'user' in request.session:
        cust = customer.objects.get(fname = request.session['user'])
        enqiry = cus_request.objects.all().filter(Customer_id = cust.id, status="Approved")
        return render(request,"car/customer_view_approved_request.html",{"user":cust,"enquiry":enqiry})
    else:
        return render('customerlogin')
def customer_approved_request_bill(request):
    if 'user' in request.session:
        cust = customer.objects.get(fname = request.session['user'])
        enqiry = cus_request.objects.all().filter(Customer_id = cust.id).exclude(status='Pending')
        return render(request,"car/customer_view_approved_request_bill.html",{"user":cust,"enquiry":enqiry})
    else:
        return render('customerlogin')

def del_customer_request(request,id):
    if 'user' in request.session:
        cust = customer.objects.get(fname = request.session['user'])
        enquiry = cus_request.objects.get(id = id)
        enquiry.delete()
        return redirect('customer_view_request')
 
def customer_profile(request):
    if 'user' in request.session:
        cust = customer.objects.get(fname = request.session['user'])
        return render(request,"car/customer_profile.html",{'user':cust})

def forgotpassword(request):
    if request.method == 'POST': 
        try:
            useremail = request.POST.get('email')
            mail = customer.objects.get(email = useremail) 
            
            num = "1234567890"
            otp = ''
            for i in range(4):
                otp += num[math.floor(random.random() * 10)]
            request.session['email'] = mail.email
            request.session['otp'] = otp
            send_mail('Forgot Password(car care Center)', f'otp is {otp}', 'gohilbhavesh1997@gmail.com', [f'{useremail}'])
            return redirect('check_otp')   
        except:
            text = "Email is not Registered!"
            return render(request,'car/forgot_password.html',{'mail':text})
    else:   
        return render(request,'car/forgot_password.html')

def customer_logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect('customerlogin')
    else:
        return render(request,"car/customer_dashboard.html") 




#======================================================#
#  Mechanic Login                                      #
#======================================================#

def mechaniclogin(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')
            mec =  mechanic.objects.get(email=email,password=password)
            if mec:   
                request.session['mec'] = mec.fname
                return redirect('mechanicindex')
        except:
            email = "invalid Login Credintials"
            return render(request,"car/mechaniclogin.html",{"text":email})           
    else:   
        return render(request,"car/mechaniclogin.html")
    
def mechanicindex(request):
    if 'mec' in request.session:
        user = mechanic.objects.get(fname = request.session['mec'])
        return render(request,"car/mechanicindex.html",{'mech':user})
    else:
        return redirect('mechaniclogin')


def mechanic_base(request):
        return render(request,"car/mechanicbase.html")
    
def mechanic_service(request):
    if 'mec' in request.session:
        user = mechanic.objects.get(fname = request.session['mec'])
        enquiry = cus_request.objects.all().filter(Mechanic_id = user.id)
        return render(request,"car/mechanicservice.html",{"mech":user,"work":enquiry})
    else:
        return redirect('mechaniclogin')

def mechanic_feedback(request):
    if request.method == 'POST':
        if 'mec' in request.session:
            user = mechanic.objects.get(fname = request.session['mec'])
            username = request.POST.get('username')
            email = request.POST.get('email')
            msg = request.POST.get('msg')
            feed = feedback(username=username,email=email,msg=msg)
            feed.save()
            return render(request,'car/mechanic_feedback.html',{"mech":user})
        else:
            return redirect('mechaniclogin')
    else:
        if  'mec' in request.session:
            user = mechanic.objects.get(fname = request.session['mec'])
            return render(request,"car/mechanic_feedback.html",{"mech":user})
        else:
            return redirect('mechaniclogin') 


def mechanic_update_status(request,id):
    if request.method == 'POST':
        if 'mec' in request.session:
            user = mechanic.objects.get(fname = request.session['mec'])
            status = request.POST.get('status')
            cus_request.objects.filter(Mechanic_id=user.id).update(status=status)
            mech = cus_request.objects.all()
            return HttpResponseRedirect(request,'car/mechanicservice.html',{"mech":user,"work":mech})
        else:
            return redirect('mechaniclogin')
    else:
        if 'mec' in request.session:
            user = mechanic.objects.get(fname = request.session['mec'])
            return render(request,'car/mechanic_update_status.html',{'mech':user})
        else:  
            return redirect('mechanic_service')

def mechanic_logout(request):
    if 'mec' in request.session:
        del request.session['mec']
        return redirect('mechaniclogin')
