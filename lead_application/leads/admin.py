from leads.models import Construction, DealType, Investor, Lead, ListSource, MailingType, PropertyStatus, Status, MailingHistory, PointOfContact
from django.contrib import admin
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import forms
from django.conf.urls import patterns

import csv
from datetime import datetime

from dbindexer.api import register_index

register_index(Lead, {'property_street_address': 'icontains'})

csv_headers = [
               "Folio No",
               "Date of Auction",
               "Owner",
               "Owner Second",
               "Street Address",
               "City",
               "State",
               "Zip Code",
               "Situs",
               "Assessed Value",
               "Use Code",
               "Legal Description",
               "Total Balance",
               "Annual Bill Balance (2012)",
               "Deed Sale",
               'Primary Zone',
               'Land Use',
               'Previous Sale',
               'Price',
               'OR Book Page'
               ]
           
csv_to_lead_field_mapping = {"Folio No":"folio_id",
                             "Situs":"property_street_address",
                             "Assessed Value":"assessed_value",
                             "Use Code":"use_code",
                             "Legal Description":"legal_description",
                             "Total Balance":"total_balance",
                             "Annual Bill Balance (2012)":"annual_bill_balance",
                             "Deed Sale":"tax_auction",
                             "Primary Zone":"primary_zone",
                             "Land Use":"land_use",
                             "Previos Sale":"previous_sale",
                             "Price":"price",
                             "OR Book Page":"or_book_page",
                             }

class UploadFileForm(forms.Form):
    file  = forms.FileField()
    
class MailingHistoryInline(admin.StackedInline):
    model = MailingHistory
    extra = 1

class PointOfContactInline(admin.StackedInline):
    model = PointOfContact
    extra = 1
    
    fieldsets = [
        (None,                  {'fields': [('first_name', 'last_name', 'email')]}),
        ('Address',             {'fields': ['street_address', ('city', 'state', 'zip_code')], 'classes': ['collapse']}),
        ('Telephones', {'fields': [('telephone1', 'telephone2', 'telephone3')], 'classes': ['collapse']}),
    ]

class LeadAdmin(admin.ModelAdmin):
    class Media:
        css = {'all': ('admin/css/import.css',),}
    list_display = ('active_string', 'status', 'property_street_address', 'owner_name', 'telephone1', 'telephone2', 'auction_date')
    list_filter = ('active',)
    fieldsets = [
        (None,                  {'fields': ['investor', 'status', 'list_source', 'mailing_type', 'deal_type', 'active']}),    
        ('Owner',               {'fields': ['deceased', ('first_name', 'last_name'), 'owner_street_address', ('owner_city', 'owner_state', 'owner_zip_code'), ('telephone1', 'telephone2', 'telephone3'), 'email'], 'classes': ['collapse']}),
        ('Property information', {'fields': ['folio_id', 'property_street_address', ('property_city', 'property_state', 'property_zip_code'), 'property_status', 'known_encumbrances', 
                                             'assessed_value', 'use_code', 'legal_description', 'total_balance', ('annual_bill_balance', 'annual_bill_balance_year'), 'tax_auction', 'primary_zone', 'land_use', 'previous_sale', 'price', 'or_book_page' ,
                                             'property_bedroom_number', 'property_bathroom_number', 'property_inside_sq_ft', 'property_lot_size', 'construction', 'property_year_built', 'auction_pending', 'balance_owed', 'auction_date'], 'classes': ['collapse']}),
        ('Short Sale Lender information', {'fields': ['short_sale_lender_name', 'short_sale_lender_telephone', 'short_sale_lender_letter_fax', 'point_of_contact', 'lender_verify_info', 'loan_number'], 'classes': ['collapse']}),
        ('Mail/Campaign information', {'fields': ['cost', 'letters_mailed', 'can_mail_multiple_times', 'return_mail'], 'classes': ['collapse']}),
    ]
    
    inlines = [PointOfContactInline, MailingHistoryInline]
    actions = ['make_active', 'make_inactive']
    search_fields = ['property_street_address']
    ordering = ('idxf_property_street_address_l_icontains',)
    
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
        return HttpResponseRedirect('/admin/leads/lead')
        
    def import_leads(self, file):
        """ Import Leads from the given file """
        reader = csv.DictReader(file, fieldnames=csv_headers, restval="")
        reader.next()
        for row in reader:
            folio_id = self.getFieldData(row, "Folio No")
            owner_name = self.getFieldData(row, "Owner") + " " + self.getFieldData(row, "Owner Second")
            owner_street_address = self.getFieldData(row, "Street Address")
            owner_city = self.getFieldData(row, "City")
            owner_state = self.getFieldData(row, "State")
            owner_zip_code = self.getFieldData(row, "Zip Code")
            auction_date_string = self.getFieldData(row, "Date of Auction")
            try:
                auction_date = datetime.strptime(auction_date_string, "%B %d, %Y")
            except ValueError:
                auction_date = None
            
            lead = Lead.objects.filter(folio_id=folio_id)
            if len(lead) == 0:
                lead = None
            else:
                lead = lead[0]
            if lead is None:
                lead = Lead(last_name=owner_name, annual_bill_balance_year=datetime.now().year,
                            owner_street_address=owner_street_address, owner_city=owner_city, owner_state=owner_state, owner_zip_code=owner_zip_code)
                            
                lead.auction_date = auction_date 
                for column in csv_to_lead_field_mapping:
                    self.setFieldData(lead, row, column, csv_to_lead_field_mapping[column])
            else:
                lead.auction_date = auction_date
                lead.annual_bill_balance_year = datetime.now().year
                
                lead.pointofcontact_set.create(last_name=owner_name, street_address=owner_street_address,
                        city=owner_city, state=owner_state, zip_code=owner_zip_code)
                
            lead.save()
    
    def getFieldData(self, row, field):
        if field in row:
            return row[field].replace('"', '').replace('=', '')
        return ''
        
    def setFieldData(self, lead, row, columnName, fieldName):
        setattr(lead, fieldName, self.getFieldData(row, columnName))

admin.site.register(Construction)
admin.site.register(DealType)
admin.site.register(Investor)
admin.site.register(ListSource)
admin.site.register(MailingType)
admin.site.register(PropertyStatus)
admin.site.register(Status)
admin.site.register(Lead, LeadAdmin)