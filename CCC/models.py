from django.contrib.auth.models import AbstractUser
from django.db import models



class customer(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=20)
    gender = models.CharField(max_length=7)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    user_type_data = (("Admin", "Admin"), ("Mechanic", "Mechanic"), ("Customer", "Customer"))
    user_type = models.CharField(default="Customer", choices=user_type_data, max_length=10)


class mechanic(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField()
    gender = models.CharField(max_length=7)
    designation = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    user_type_data = (("Admin", "Admin"), ("Mechanic", "Mechanic"), ("Customer", "Customer"))
    user_type = models.CharField(default="Customer", choices=user_type_data, max_length=10)