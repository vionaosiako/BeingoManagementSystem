from django.db import models
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import datetime as dt

# Create your models here.

class Profile(models.Model):
    profile_pic=CloudinaryField('image')
    fullname=models.CharField(max_length=100)
    bio=models.TextField()
    email=models.EmailField(max_length=100,null=True)    
    phone_number=models.CharField(max_length=100,null=True) 
    hood = models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.user.username
    
    @classmethod
    def search_profile(cls, fullname):
        return cls.objects.filter(user__username__icontains=fullname).all()
    
    @receiver(post_save,sender=User)
    def createUserProfile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
            
    @receiver(post_save,sender=User)
    def saveUserProfile(sender, instance, **kwargs):
        instance.profile.save()
    def saveProfile(self):
        self.user()
        
class Saving(models.Model):
    amount = models.IntegerField()
    member_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date_contributed = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_contributed']