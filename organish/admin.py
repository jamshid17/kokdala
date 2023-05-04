from django.contrib import admin
from .models import Organish, OrganishGuruh, Tashkilot
from django.contrib.admin import AdminSite

# Register your models here.
admin.site.register(OrganishGuruh)
admin.site.register(Organish)
admin.site.register(Tashkilot)


