from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

gen={
    ('Select','Select'),
    ('Male','Male'),
    ('Female','Female'),
    ('Other','Other')
}

class User(AbstractUser):
    image=models.ImageField(upload_to='user_profile', null=True, blank=True)
    phone = models.CharField(max_length=20,unique=True,null=True,blank=True,validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message='Enter a valid phone number')])
    gender=models.CharField(max_length=255,choices=gen,null=True,blank=True)
    house_name=models.CharField(max_length=255,null=True,blank=True)
    street=models.CharField(max_length=255,null=True,blank=True)
    city=models.CharField(max_length=255,null=True,blank=True)
    state=models.CharField(max_length=255,null=True,blank=True)
    pincode=models.CharField(max_length=255,validators=[RegexValidator(regex=r'^\d{6}$', message='Pincode must be exactly 6 digits')],null=True,blank=True)
    country=models.CharField(max_length=10,null=True,blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return f"{self.username}"
    
    def state_and_pincode(self):
        if self.state and self.pincode:
            return f"{self.state} - {self.pincode}"
        elif self.state:
            return self.state
        elif self.pincode:
            return self.pincode
        return ""
    