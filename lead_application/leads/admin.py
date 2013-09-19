from leads.models import Lead, PointOfContact
from django.contrib import admin

class PointOfContactInline(admin.TabularInline):
    model = PointOfContact
    extra = 1

class LeadAdmin(admin.ModelAdmin):
    list_display = ('property_street_address', 'owner_name', 'telephone1')
    fieldsets = [
        #(None,                  {'fields': ['first_name', 'last_name', 'telephone1']}),    
        ('Owner',               {'fields': ['first_name', 'last_name', 'owner_street_address', 'owner_city', 'owner_state', 'owner_zip_code', 'telephone1', 'telephone2', 'telephone3', 'email'], 'classes': ['collapse']}),
        ('Property information', {'fields': ['folio_id', 'property_street_address', 'property_city', 'property_state', 'property_zip_code', 'property_bedroom_number', 'property_bathroom_number', 'property_inside_sq_ft', 'property_lot_size', 'property_year_built', 'auction_pending'], 'classes': ['collapse']}),
        ('Short Sale Lender information', {'fields': ['short_sale_lender_name', 'short_sale_lender_telephone', 'short_sale_lender_letter_fax', 'point_of_contact', 'lender_verify_info', 'loan_number'], 'classes': ['collapse']}),
    ]
    
    inlines = [PointOfContactInline]

admin.site.register(Lead, LeadAdmin)