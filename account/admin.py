from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'photo', 'mobile_no', 'city', 'landmark', 'location']

admin.site.register(Profile, ProfileAdmin)
