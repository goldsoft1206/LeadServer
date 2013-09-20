from leads.models import Construction, DealType, Investor, Lead, ListSource, MailingType, PropertyStatus, Status, PointOfContact
from django.contrib import admin
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.conf.urls import patterns

class UploadFileForm(forms.Form):
    file  = forms.FileField()

class PointOfContactInline(admin.StackedInline):
    model = PointOfContact
    extra = 1
    
    fieldsets = [
        (None,                  {'fields': [('first_name', 'last_name', 'email')]}),
        ('Address',             {'fields': ['street_address', ('city', 'state', 'zip_code')], 'classes': ['collapse']}),
        ('Telephones', {'fields': [('telephone1', 'telephone2', 'telephone3')], 'classes': ['collapse']}),
    ]

class LeadAdmin(admin.ModelAdmin):
    list_display = ('active_string', 'status', 'property_street_address', 'owner_name', 'telephone1')
    list_filter = ('active',)
    fieldsets = [
        (None,                  {'fields': ['investor', 'status', 'list_source', 'mailing_type', 'deal_type', 'active']}),    
        ('Owner',               {'fields': ['deceased', ('first_name', 'last_name'), 'owner_street_address', ('owner_city', 'owner_state', 'owner_zip_code'), ('telephone1', 'telephone2', 'telephone3'), 'email'], 'classes': ['collapse']}),
        ('Property information', {'fields': ['folio_id', 'property_street_address', ('property_city', 'property_state', 'property_zip_code'), 'property_status', 'known_encumbrances', 'property_bedroom_number', 'property_bathroom_number', 'property_inside_sq_ft', 'property_lot_size', 'construction', 'property_year_built', 'auction_pending', 'balance_owed', 'auction_date'], 'classes': ['collapse']}),
        ('Short Sale Lender information', {'fields': ['short_sale_lender_name', 'short_sale_lender_telephone', 'short_sale_lender_letter_fax', 'point_of_contact', 'lender_verify_info', 'loan_number'], 'classes': ['collapse']}),
        ('Mail/Campaign information', {'fields': ['cost', 'letters_mailed', 'can_mail_multiple_times', 'return_mail'], 'classes': ['collapse']}),
    ]
    
    inlines = [PointOfContactInline]
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        queryset.update(active=True)
    make_active.short_description = "Mark selected leads as active"

    def make_inactive(self, request, queryset):
        queryset.update(active=False)
    make_inactive.short_description = "Mark selected leads as inactive"
    
    def get_urls(self):
        urls = super(LeadAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^import/$', self.admin_site.admin_view(self.import_leads_view))
        )
        return my_urls + urls
        
    def import_leads_view(self, request):
        
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                self.import_leads(request.FILES['file'])
                return HttpResponseRedirect('/admin/leads/lead')
        else:
            form = UploadFileForm()
            
        c = {'form': form}
        c.update(csrf(request))
        return render_to_response('import.html', c)
        
    def import_leads(self, file):
        """ Import Leads from the given file """
        lines = file.readlines()
        for line in lines[1:]:
            fields = line.split(",")
            lead = Lead(folio_id=fields[0].replace('"', ''))
            lead.save()

admin.site.register(Construction)
admin.site.register(DealType)
admin.site.register(Investor)
admin.site.register(ListSource)
admin.site.register(MailingType)
admin.site.register(PropertyStatus)
admin.site.register(Status)
admin.site.register(Lead, LeadAdmin)