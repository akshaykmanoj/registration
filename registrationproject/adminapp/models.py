from django.db import models

# Create your models here.
class Member(models.Model):
    Username=models.CharField(max_length=100)
    Firstname=models.CharField(max_length=100)
    Lastname=models.CharField(max_length=100)
    Email=models.EmailField(max_length=100)