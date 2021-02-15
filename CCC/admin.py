from django.contrib import admin
from .models import *
# import csv, datetime
from django.http import HttpResponse
from .views import export_csv


# Register your models here.
class customeradmin(admin.ModelAdmin):
    list_display = ['fname','lname','email','mobile','gender','address','image']
admin.site.register(customer,customeradmin)

class mechanicadmin(admin.ModelAdmin):
    list_display = ('fname','lname','email','mobile','gender','designation','salary','address','image')
admin.site.register(mechanic,mechanicadmin)

class feedbackadmin(admin.ModelAdmin):
    list_display = ('username','email','msg','date')

admin.site.register(feedback, feedbackadmin)

class cust_reqadmin(admin.ModelAdmin):
    list_display = ('category','number','name','brand','model','problem','date','cost','status')
    actions = [export_csv]


admin.site.register(cus_request, cust_reqadmin)

class contactadmin(admin.ModelAdmin):
    list_display=('name','email','msg')

admin.site.register(contact,contactadmin)

class leaveadmin(admin.ModelAdmin):
    list_display = ('Mechanic_id','reason','from_date','to_date','status','admin_reason')

    def Mechanic_id(self,obj):
        return obj.Mechanic.fname
admin.site.register(apply_leave,leaveadmin)


# User = customer()

# def export_to_csv(modeladmin, request, queryset):
#     opts = modeladmin.model._meta
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment;' 'filename{}.csv'.format(opts.verbose_name)
#     writer = csv.writer(response)
#     fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
#     # Write a first row with header information
#     writer.writerow([field.verbose_name for field in fields])
#     # Write data rows
#     for obj in queryset:
#         data_row = []
#         for field in fields:
#             value = getattr(obj, field.name)
#             if isinstance(value, datetime.datetime):
#                 value = value.strftime('%d/%m/%Y')
#             data_row.append(value)
#         writer.writerow(data_row)

#     return response

# export_to_csv.short_description = 'Export to CSV'  #short description

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     actions = [export_to_csv]

