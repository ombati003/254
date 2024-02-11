from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse



class PhoneAPI(models.Model):
    ip_address = models.CharField(max_length=100)

    def __str__(self):
        return self.ip_address


class Video(models.Model):
    title = models.CharField(max_length=255)
    video_url = models.URLField()

    def __str__(self):
        return self.title
    
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(blank=True)
    code=models.CharField(max_length=12, unique=True, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    #referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_users')
    referred_users=models.ManyToManyField(User,  blank=True,  related_name='referral_users')

    def get_referral_link(self):
        
        print(f"Generating referral link for user: {self.user.username}")

        reverse('register') + f'?ref={self.code}'
        
        return f"http://127.0.0.1:8000/register/?ref={self.code}"
    

    def __str__(self) :
        return f"{self.user.username}-{self.code}"
    
    def get_recommended_profile(self):
        pass

    def save(self, *args, **kwargs):
        if self.code=="":
            code=generate_ref_code()
            self.code=code

        super().save(*args, **kwargs)

class Referral(models.Model):

    referred_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='referrer')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_user')
    referral_date_time = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # Check if a profile already exists for the user
        if not hasattr(instance, 'profile'):
            profile = Profile.objects.create(user=instance)
            profile.code = generate_ref_code()
            profile.save()
            #profile = Profile.objects.create(user=instance, code=generate_ref_code())

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

