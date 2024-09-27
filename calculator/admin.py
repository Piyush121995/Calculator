from django.contrib import admin
from django.contrib.auth.models import User
from calculator.models import UserCalculationHistory

# Register your models here.
# class SignupAdmin(admin.ModelAdmin):
#     list_display = ['First_name','Last_name','gender','Email','password']
# admin.site.register(Signup, SignupAdmin)
class UserCalculationHistoryAdmin(admin.ModelAdmin):
    list_display = ['user','expression','result','Created_at']
admin.site.register(UserCalculationHistory,UserCalculationHistoryAdmin)