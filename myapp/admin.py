from django.contrib import admin
from .models import  UserProfile
from .models import Video
# Register your models here.

admin.site.register(UserProfile)

admin.site.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_url')