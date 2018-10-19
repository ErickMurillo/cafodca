
from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import SiteConfiguration, FotosPortada

class FotosInlines(admin.TabularInline):
    model = FotosPortada
    extra = 1

class SiteConfigAdmin(SingletonModelAdmin):
    inlines = [FotosInlines]


admin.site.register(SiteConfiguration, SiteConfigAdmin)
