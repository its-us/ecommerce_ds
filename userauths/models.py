from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    bio = models.CharField(max_length = 100)
    
    def __str__(self):
        return self.username
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="image")
    full_name = models.CharField(max_length=200, null = True, blank=True)
    bio = models.CharField(max_length = 200, null = True, blank=True)
    phone = models.CharField(max_length=200)
    verified = models.BooleanField(default = False)

    def _str_(self):
        return self.user.username
    
   


class contactUs(models.Model):
    full_name = models.CharField(max_length=20) 
    email = models.CharField(max_length=50) 
    phone = models.CharField(max_length=15) 
    subject = models.CharField(max_length=100)
    message = models.TextField()

    class Meta :
        verbose_name=  "contactUs"
        verbose_name_plural= "contactUs"

    def _str_(self) :
        return self.full_name
    

def create_user_profile(sender, instance, created,**kwargs,):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance,**kwargs) :
    instance.profile.save()

post_save.connect(create_user_profile, sender= User)
post_save.connect(save_user_profile, sender= User)