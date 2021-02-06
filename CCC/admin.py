from django.contrib import admin
from .models import *

# Register your models here.
class customeradmin(admin.ModelAdmin):
    list_display = ['fname','lname','email','mobile','gender','address']

admin.site.register(customer,customeradmin)

class mechanicadmin(admin.ModelAdmin):
    list_display = ('fname','lname','email','mobile','gender','designation','salary','address')
admin.site.register(mechanic,mechanicadmin)

class feedbackadmin(admin.ModelAdmin):
    list_display = ('username','email','msg','date')

admin.site.register(feedback, feedbackadmin)

class cust_reqadmin(admin.ModelAdmin):
    list_display = ('category','number','name','brand','model','problem','date','cost','status')

admin.site.register(cus_request, cust_reqadmin)