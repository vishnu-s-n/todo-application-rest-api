from django.contrib import admin
from todo.models import *
# Register your models here.
admin.site.register(TodoTask)
admin.site.register(UserRegistration)
admin.site.register(UserLoginOtp)

