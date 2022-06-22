from django.contrib import admin

# Register your models here.
from .models import Profile,Member,Saving
admin.site.register(Profile),
admin.site.register(Member),
admin.site.register(Saving),