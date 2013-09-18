from leads.models import Lead, PointOfContact
from django.contrib import admin

class PointOfContactInline(admin.TabularInline):
    model = PointOfContact
    extra = 1

class LeadAdmin(admin.ModelAdmin):
    list_display = ('property_street_address', 'owner_name')
    fieldsets = [
        (None,               {'fields': ['first_name', 'last_name']}),
        ('Property information', {'fields': ['folio_id', 'property_street_address', 'property_city', 'property_state', 'property_zip_code'], 'classes': ['collapse']}),
    ]
    
    inlines = [PointOfContactInline]

admin.site.register(Lead, LeadAdmin)