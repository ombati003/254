from django.contrib import admin
from .models import  Profile, Referral
from .models import Video
# Register your models here.

admin.site.register(Profile)

admin.site.register(Referral)

admin.site.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url')