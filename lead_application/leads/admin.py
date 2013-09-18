from leads.models import Lead, Owner
from django.contrib import admin

class OwnerInline(admin.TabularInline):
    model = Owner
    extra = 1

class LeadAdmin(admin.ModelAdmin):
    list_display = ('investor_name',)
    inlines = [OwnerInline]

admin.site.register(Lead, LeadAdmin)