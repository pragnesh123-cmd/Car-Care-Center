from django.contrib import admin
from .models import *

# Register your models here.
class customeradmin(admin.ModelAdmin):
    list_display = ['fname','lname','email','mobile_no','gender','address']

admin.site.register(customer,customeradmin)