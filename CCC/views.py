from django.shortcuts import render,redirect
from .models import *
from django.db.models import Sum
from django.http  import HttpResponse
import math
import random
import smtplib
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv
from random import *
import string
from CCC import Checksum

from CCC.utils import VerifyPaytmResponse
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa 
from io import BytesIO
from django.template import loader 
from django.template.loader import get_template
from django.views.generic import View

from xhtml2pdf import pisa

###################Paytm#############



def payment(request,id):
    if 'user' in request.session:
        cust = customer.objects.get(fname = request.session['user'])
        order_id = Checksum.__id_generator__()
        obj = cus_request.objects.filter(id = id)
        cost = str(obj[0].cost)
        cust_id = str(randint(0000,9999))
        # bill_amount = "100"
        data_dict = {
            'MID': settings.PAYTM_MERCHANT_ID,
            'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
            'WEBSITE': settings.PAYTM_WEBSITE,
            'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
            'CALLBACK_URL': settings.PAYTM_CALLBACK_URL,
            'MOBILE_NO': customer.objects.get(id = cust.id).mobile,
            'EMAIL':  customer.objects.get(id = cust.id).email,
            'CUST_ID': cust_id,
            'ORDER_ID':order_id,
            'TXN_AMOUNT':cost,
        } # This data should ideally come from database
        data_dict['CHECKSUMHASH'] = Checksum.generate_checksum(data_dict, "mA&OnVHKf%aur&J8")
        paytm(Customer_id= cust.id,Cus_Request_id = id,ORDER_ID=order_id).save()
        context = {
            'payment_url': settings.PAYTM_PAYMENT_GATEWAY_URL,
            'comany_name': settings.PAYTM_COMPANY_NAME,
            'data_dict': data_dict
        }
    return render(request, 'car/payment.html', context)


@csrf_exempt
def response(request):
    resp = VerifyPaytmResponse(request)
    if resp['verified']:
        ORDER_ID=resp['paytm']['ORDERID']
        TXN_AMOUNT=resp['paytm']['TXNAMOUNT']
        BANKTXNID=resp['paytm']['BANKTXNID']
        BANKNAME=resp['paytm']['BANKNAME']
        TXNDATE=resp['paytm']['TXNDATE']
        STATUS=resp['paytm']['STATUS']
        paytm.objects.filter(ORDER_ID =ORDER_ID).update(TXN_AMOUNT=TXN_AMOUNT,BANKTXNID=BANKTXNID,BANKNAME=BANKNAME,STATUS=STATUS)
        obj = paytm.objects.filter(ORDER_ID=ORDER_ID)
        id = obj[0].Cus_Request.id
        obj1 = cus_request.objects.filter(id=id).update(payment_status = True)
       
        # save success details to db; details in resp['paytm']
        return redirect('invoice')
    else:

        # check what happened; details in resp['paytm']
        return HttpResponse("<center><h1>Transaction Failed</h1><center>", status=400)
       

        
###########End Paytm###############
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
#======================================================================#
#                  Customer Related Views                              #
#======================================================================#


def changepassword(request):
    return render(request,"car/change-password.html")

def forgotpassword(request):
    if request.method == 'POST':         
        try:
            useremail = request.POST.get('email')

            mail = customer.objects.get(email = useremail)
            num = "1234567890"
            otp = randint(000000,99999)
            # for i in range(4):
                # otp += num[math.floor(random.random() * 10)]
            request.session['email'] = mail.email
            request.session['otp'] = otp
            send_mail('Forgot Password(car care Center)', f'Customer otp is: {otp}', 'jigarramani40@gmail.com', [f'{useremail}'])
            return redirect('check_otp')   
        except:
            text = "Email is not Registered!"
            return render(request,'car/forgot_password.html',{'mail':text})
    else:   
        return render(request,'car/forgot_password.html')

def check_otp(request):
    if request.method == 'POST':
        otppass = int(request.POST.get('otppass'))
        if otppass==request.session.get('otp'):
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
        text = 'Your Password has Succesfully Change!'
        return redirect('customerlogin')
    else:
        return render(request,'car/forgot_password_change.html')

def customerbase(request):
    return render(request,"car/customerindex.html")

def customerregister(request):
    if request.method == 'POST' and request.FILES['image']:
        try:
            if customer.objects.get(email = request.POST['email']):
                mail = "Already Registered with this email!"
                return render(request,"car/customerregister.html",{"mail":mail})
        except:
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile_no')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            char = string.ascii_letters + string.digits
            password ="".join(choice(char)
            for x in range(randint(6,10)))
            reg = customer(fname = fname,lname=lname,email=email,mobile=mobile,gender=gender,address=address,password=password,image=myfile)
            reg.save()
            stu = customer.objects.all()
            text = "Your Password Will Be Sent Your Registered Mail id..!"
            send_mail('Registered Successfully car care Center', f'You Are registered Successfuly in Our System!\n Your Password is: {password}', 'jigarramani40@gmail.com', [f'{email}'])
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
            email = "Invalid login credintials"
            return render(request,"car/login.html",{"text":email})           
    else:   
        return render(request,"car/login.html")

def cust_change_pass(request):
    if request.method == 'POST':
        cust = customer.objects.get(fname = request.session['user'])
        current = request.POST.get('current')
        newpass = request.POST.get('newpass')
        try:
            customer.objects.get(password=current)
            customer.objects.all().filter(id=cust.id).update(password=newpass)
            text = "Your Password Successfully Change..."
            return render(request,'car/cust_change_password.html',{'text':text,'user':cust})
        except:
            change = "Current Password is not Match"
            return render(request,'car/cust_change_password.html',{'change':change,'user':cust})
    else:
        if 'user' in request.session:
            cust = customer.objects.get(fname = request.session['user'])
            return render(request,'car/cust_change_password.html',{"user":cust})
        else:
            return redirect('customerlogin')

def customer_profile(request):
    if 'user' in request.session:
        cust = customer.objects.get(fname = request.session['user'])
        enquiry = cus_request.objects.all().filter(Customer_id = cust.id, status="Approved").order_by('date')
        cus= customer.objects.get(id=cust.id)
        return render(request,"car/customer_profile.html",{"user":cust,"stu":cus,'enquiry':enquiry})
    else:
        return redirect('customerlogin')


def cust_edit_profile(request):
    if request.method == 'POST':
        if 'user' in request.session and request.FILES['image']:
            cust = customer.objects.get(fname = request.session['user'])
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            mobile = request.POST.get('mobile')
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            enquiry = customer.objects.all().filter(id=cust.id).update(fname=fname,lname=lname,email=email,gender=gender,address=address,mobile=mobile,image=myfile)
            request.session['user']=fname
            return redirect('customer_profile')
        else:
            return redirect('customerlogin')
        
    else:
        if 'user' in request.session:
            cust = customer.objects.get(fname = request.session['user'])
            return render(request,'car/cust_profile_edit.html',{'user':cust})
        else:
            return redirect('customerlogin')



def customer_feedback(request):
    if request.method == 'POST':    
        if 'user' in request.session:
            cust = customer.objects.get(fname = request.session['user'])
            username = request.POST.get('username')
            email = request.POST.get('email')
            msg = request.POST.get('msg')
            feed = feedback(username=username,email=email,msg=msg)
            feed.save()
            text = 'Your Feedback Successfully Sent'
            return render(request,"car/feedback.html",{'user':cust,'text':text})
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
        # obj = paytm.objects.filter(Customer_id=cust.id,STATUS="TXN_SUCCESS")
        enquiry = cus_request.objects.all().filter(Customer_id = cust.id).exclude(status = 'Pending')
        # enquiry = paytm.objects.filter(Customer = cust.id)
        return render(request,"car/customer_invoice.html" ,{"user":cust,'enquiry':enquiry})
    else:
        return redirect('customerlogin')

# def cust_invoice(request):
#     if 'user' in request.session:
#         cust = customer.objects.get(fname = request.session['user'])
#         enquiry = paytm.objects.filter(Customer = cust.id)
#         return render(request,"car/payment_success.html" ,{"user":cust,'enquiry':enquiry})
#     else:
#         return redirect('customerlogin')

def pay_success(request):
    if 'user' in request.session:
        cust = customer.objects.get(fname = request.session['user'])
        obj = paytm.objects.filter(Customer_id=cust.id).exclude(STATUS="TXN_FAIL")
        return render(request,"car/payment_success.html" ,{"user":cust,'obj':obj})
    else:
        return redirect('customerlogin')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

class GeneratePDF(View):
    
    def get(self, request,order_id, *args, **kwargs):
        
        template = get_template('car/invoice.html')
        cust = customer.objects.get(fname = request.session['user'])
        obj = paytm.objects.filter(Customer_id=cust.id).exclude(STATUS="TXN_FAIL")
        data = paytm.objects.get(ORDER_ID=order_id)
        context = {
            'ORDER_ID' : data.ORDER_ID,
            'TXN_AMOUNT' : data.TXN_AMOUNT,
            'BANKTXNID' : data.BANKTXNID,
            'BANKNAME' : data.BANKNAME,
            'TXNDATE' : data.TXNDATE,
            'STATUS' : data.STATUS,
            'data':data

        }
        html = template.render(context)
        pdf = render_to_pdf('car/invoice.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = f'Payment invoice.pdf'
            content = "inline; filename= %s" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

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


def customer_logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect('customerlogin')
    else:
        return render(request,"car/customer_dashboard.html") 




#======================================================#
#  Mechanic Views                                      #
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

def mech_change_pass(request):
    if request.method == 'POST':
        user = mechanic.objects.get(fname = request.session['mec'])
        current = request.POST.get('current')
        newpass = request.POST.get('newpass')
        password = request.session.get('password')
        try:
            mechanic.objects.get(password=current)
            mechanic.objects.all().filter(id=user.id).update(password=newpass)
            text = "Your Password Successfully Change..."
            return render(request,'car/mech_change_pass.html',{'text':text,"mech":user})
        except:
            change = "Current Password is not Match"
            return render(request,'car/mech_change_pass.html',{'change':change,'mech':user})

    else:
        if 'mec' in request.session:
            user = mechanic.objects.get(fname = request.session['mec'])
            return render(request,'car/mech_change_pass.html',{'mech':user})
        else:
            return redirect('mechaniclogin')

def mechanic_profile(request):
    if 'mec' in request.session:
        user = mechanic.objects.get(fname = request.session['mec'])
        # enqiry = cus_request.objects.all().filter(Customer_id = cust.id, status="Approved").order_by('date')
        cus= mechanic.objects.get(id=user.id)
        return render(request,"car/mechanic_profile.html",{"mech":user,"stu":cus})
    else:
        return redirect('mechaniclogin')


def mech_edit_profile(request):
    if request.method == 'POST':
        if 'mec' in request.session and request.FILES['image']:
            user = mechanic.objects.get(fname = request.session['mec'])
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            mobile = request.POST.get('mobile')
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            enquiry = mechanic.objects.all().filter(id=user.id).update(fname=fname,lname=lname,email=email,gender=gender,address=address,mobile=mobile,image=myfile)
            request.session['mec']=fname
            return redirect('mechanic_profile')
        else:
            return redirect('mechaniclogin')        
    else:
        if 'mec' in request.session:
            user = mechanic.objects.get(fname = request.session['mec'])
            return render(request,'car/mech_edit_profile.html',{'mech':user})
        else:
            return redirect('mechaniclogin')


def career(request):
    job = job_desc.objects.all()
    return render(request,"car/career.html",{"job":job})

def applyjob(request):
    if request.method=='POST' and request.FILES['resume']:
        fname = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        dob = request.POST.get('dob')
        pname = request.POST.get('post_name')
        obj = post_name.objects.get(post=pname)
        qualification = request.POST.get('qualification')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        resume = request.FILES['resume']
        fs = FileSystemStorage()
        filename = fs.save(resume.name, resume)
        uploaded_file_url = fs.url(filename)
        job = job_apply(name=fname,email=email,mobile=mobile,dob=dob,post_name_id = obj.id,qualification=qualification,skills=skills,experience=experience,resume=resume)
        job.save()
        text = "Job Applied Successfully"
        name = post_name.objects.all()
        return render(request,"car/apply_job.html",{"text":text,'name':name})
    else:
        name = post_name.objects.all()
        return render(request,"car/apply_job.html",{'name':name})
    
def mechanicindex(request):
    if 'mec' in request.session:
        user = mechanic.objects.get(fname = request.session['mec'])
        count_req = cus_request.objects.all().filter(Mechanic_id = user.id, status = 'Approved').count()
        work_progress =  cus_request.objects.all().filter(Mechanic_id = user.id, status = 'Repairing').count()
        work_complete = cus_request.objects.all().filter(Mechanic_id = user.id, status = 'Repairing Done').count()
        Salary  = mechanic.objects.get(salary=user.salary)
        dict = {
            'mech':user,
            'count_req':count_req,
            'work_progress':work_progress,
            'work_complete':work_complete,
            'Salary':Salary
        }
        return render(request,"car/mechanicindex.html",context=dict)
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
            return redirect('mechanic_service')
        else:
            return redirect('mechaniclogin')
    else:
        if 'mec' in request.session:
            user = mechanic.objects.get(fname = request.session['mec'])
            return render(request,'car/mechanic_update_status.html',{'mech':user})
        else:  
            return redirect('mechanic_service')
def mechanic_leave(request):
    if 'mec' in request.session:
        user = mechanic.objects.get(fname=request.session['mec'])
        return render(request,'car/mechanicleave.html',{'mech':user})
    else:
        return redirect('mechaniclogin')

def mechanic_leave_form(request):
    if request.method == 'POST':
        if 'mec' in request.session:
            user = mechanic.objects.get(fname=request.session['mec'])
            reason = request.POST.get('reason')
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date') 
            leave = apply_leave(reason=reason,from_date=from_date,to_date=to_date,Mechanic_id=user.id) 
            leave.save()
            return render(request,'car/mechanic_apply_leave.html',{"mech":user})
        else:
            return redirect('mechaniclogin')
    else:
        if 'mec' in request.session:
            user = mechanic.objects.get(fname=request.session['mec'])
            return render(request,'car/mechanic_apply_leave.html',{"mech":user})
        else:
            return redirect('mechaniclogin')

def leave_status(request):
    if 'mec' in request.session:
        user = mechanic.objects.get(fname=request.session['mec'])
        leave_stat = apply_leave.objects.filter(Mechanic_id=user.id) 
        return render(request,'car/leave_status.html',{'mech':user,'leave_stat':leave_stat})
    else:
        return redirect('mechaniclogin')

def mechanicforgotpass(request):
    if request.method == 'POST':         
        try:
            useremail = request.POST.get('email')

            mail = mechanic.objects.get(email = useremail)
            num = "1234567890"
            otp = randint(0000,9999)
            # for i in range(4):
                # otp += num[math.floor(random.random() * 10)]
            request.session['email'] = mail.email
            request.session['otp'] = otp
            send_mail('Forgot Password(car care Center)', f'Mechnic otp is: {otp}', 'jigarramani40@gmail.com', [f'{useremail}'])
            return redirect('mechanic_check_otp')   
        except:
            text = "Email is not Registered!"
            return render(request,'car/mechanicforgotpass.html',{'mail':text})
    else:   
        return render(request,'car/mechanicforgotpass.html')

def mechanic_check_otp(request):
    if request.method == 'POST':
        otppass = int(request.POST.get('otppass'))
        if otppass==request.session.get('otp'):
            return redirect('mechanicforgotpasschange')  
        else:
            text = "you have entered wrong otp..!"
            return render(request,'car/mechanic_check_otp.html',{'otp':text})
    else:   
        return render(request,"car/mechanic_check_otp.html")

def mechanicforgotpasschange(request):
    if request.method == 'POST':
        newpass = request.POST.get('newpass')
        mechanic.objects.all().filter(email = request.session['email']).update(password=newpass)
        text = 'Your Password has Succesfully Change!'
        return redirect('mechaniclogin')
    else:
        return render(request,'car/mechanic_forgot_pass_change.html')


def mechanic_logout(request):
    if 'mec' in request.session:
        del request.session['mec']
        return redirect('mechaniclogin')


#Export csv file

def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=cus_request.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"category"),
        smart_str(u"number"),
        smart_str(u"name"),
        smart_str(u"model"),
        smart_str(u"brand"),
        smart_str(u"problem"),
        smart_str(u"date"),
        smart_str(u"status"),
        smart_str(u"cost"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.category),
            smart_str(obj.number),
            smart_str(obj.name),
            smart_str(obj.model),
            smart_str(obj.brand),
            smart_str(obj.problem),
            smart_str(obj.date),
            smart_str(obj.status),
            smart_str(obj.cost),
            
        ])
    return response
export_csv.short_description = u"Export CSV"

def paytm_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Payment.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"ORDER_ID"),
        smart_str(u"TXN AMOUNT"),
        smart_str(u"BANKTXNID"),
        smart_str(u"BANKNAME"),
        smart_str(u"TXNDATE"),
        smart_str(u"STATUS"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.ORDER_ID),
            smart_str(obj.TXN_AMOUNT),
            smart_str(obj.BANKTXNID),
            smart_str(obj.BANKNAME),
            smart_str(obj.TXNDATE),
            smart_str(obj.STATUS),
            
        ])
    return response
export_csv.short_description = u"Export CSV"