from django.contrib import admin
from web.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=['id','image','username','first_name','last_name','email','phone','gender','house_name','street','city','state','pincode','country','is_staff','is_active']
admin.site.register(User,UserAdmin)
