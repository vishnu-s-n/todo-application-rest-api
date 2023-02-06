from django.db import models
# Create your models here.

class UserRegistration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phonenumber = models.IntegerField()

class TodoTask(models.Model):
    user = models.ForeignKey(UserRegistration,on_delete=models.CASCADE,related_name="TodoTask_user")
    title = models.CharField(max_length=200)
    description = models.TextField( null=True, blank=True)
    complete = models.BooleanField(default=True)

class UserLoginOtp(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name="UserLoginOtp_user")
    otp = models.IntegerField()
    active = models.BooleanField()