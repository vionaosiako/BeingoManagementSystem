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

class Member(models.Model):
    profile_pic=CloudinaryField('image')
    fullname=models.CharField(max_length=100)
    email=models.EmailField(max_length=100,null=True)    
    phone_number=models.CharField(max_length=100,null=True) 
    hood = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    admin = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.fullname

class Saving(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date_contributed = models.DateTimeField(auto_now_add=True)
    admin= models.ForeignKey(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.member_id.fullname
    
    class Meta:
        ordering = ['-date_contributed']