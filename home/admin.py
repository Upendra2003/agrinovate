from django.contrib import admin
from .models import SoilHealth

class SoilHealthAdmin(admin.ModelAdmin):
    pass

admin.site.register(SoilHealth, SoilHealthAdmin)