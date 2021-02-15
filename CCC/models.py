from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

from django.utils import timezone



class customer(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    gender = models.CharField(max_length=7)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images/') 


    def __str__(self):
        return self.fname   


class mechanic(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.EmailField()
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=20)
    designation = models.CharField(max_length=20)
    salary = models.FloatField(max_length=10)
    address = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images/',null = True,blank=True) 
    

    def __str__(self):
        return self.fname


class cus_request(models.Model):
    category = models.CharField(max_length=40)
    number = models.CharField(max_length=100)
    name = models.CharField(max_length=40)
    brand = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    problem = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    cost = models.PositiveIntegerField(null = True)
    Customer = models.ForeignKey('customer',on_delete=models.CASCADE,null=True)
    Mechanic = models.ForeignKey('mechanic',on_delete=models.CASCADE,null=True)
    stat = (('Pending','Pending'),('Approved','Approved'),('Repairing','Repairing'),('Repairing Done','Repairing Done'),('Released','Released'))
    status = models.CharField(max_length=40,choices=stat,default='Pending',null=True)

class feedback(models.Model):
    username = models.CharField(max_length=40)
    email = models.CharField(max_length=50)
    msg = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)

class contact(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    msg  = models.CharField(max_length=100)

class apply_leave(models.Model):
    reason = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    stat = (('Pending','Pending'),('Approved','Approved'),('Rejected','Rejected'))
    status = models.CharField(max_length=40,choices=stat,default='Pending',null=True)
    Mechanic = models.ForeignKey('mechanic',on_delete=models.CASCADE,null=True)
    admin_reason = models.CharField(max_length=100)


