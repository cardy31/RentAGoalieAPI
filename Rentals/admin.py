from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Game)
admin.site.register(Location)
admin.site.register(Message)
admin.site.register(Profile)

