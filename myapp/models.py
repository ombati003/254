from django.apps import AppConfig
from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code



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
class UserProfile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='referrer')
    bio=models.TextField(blank=True)
    refferal_code=models.CharField(max_length=12, blank=True)
    
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
  

    def __str__(self) :
        return f"{self.user.username}-{self.refferal_code}"
    
    def get_recommended_profile(self):
        pass

    def save(self, *args, **kwargs):
        if self.refferal_code == "":
            refferal_code = generate_ref_code()
            self.refferal_code = refferal_code

        super().save(*args, **kwargs)

    def refferal_count(self):
        return UserProfile.objects.filter(recommended_by = self.user).count()


class RefferalConfig(AppConfig):
    name = 'refferal'
    def ready(self):
        pass