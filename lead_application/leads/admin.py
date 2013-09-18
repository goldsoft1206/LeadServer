from leads.models import Lead, PointOfContact
from django.contrib import admin

class PointOfContactInline(admin.TabularInline):
    model = PointOfContact
    extra = 1

class LeadAdmin(admin.ModelAdmin):
    list_display = ('owner_name',)
    #inlines = [OwnerInline]

admin.site.register(Lead, LeadAdmin)