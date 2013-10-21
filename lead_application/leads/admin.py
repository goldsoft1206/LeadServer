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
               'OR Book Page',
               'Investor',
               'Status',
               'List Source',
               'Mailing Type',
               'Deal Type',
               'Active',
               'Deceased',
               'Telephone 1',
               'Telephone 2',
               'Telephone 3',
               'Email',
               'Property Street Address',
               'Property City',
               'Property State',
               'Property Zip Code',
               'Property Status',
               'Known Encumbrances',
               'Bedroom Number',
               'Bathroom Number',
               'Inside SQ FT',
               'Lot Size',
               'Construction',
               'Property Year Built',
               'Auction Pending',
               'Balance Owed',
               'Short Sale Lender Name',
               'Short Sale Telephone',
               'Short Sale Fax',
               'Short Sale PoC',
               'Lender Verify Info',
               'Loan Number',
               'Mailing Cost',
               'Letters Mailed',
               'Can Mail Multiple Times',
               'Return Mail'
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
                             "Property Street Address":"property_street_address",
                             "Property City":"property_city",
                             "Property State":"property_state",
                             "Property Zip Code":"property_zip_code",
                             'Known Encumbrances':"known_encumbrances",
                             'Bedroom Number':"property_bedroom_number",
                             'Bathroom Number':"property_bathroom_number",
                             'Inside SQ FT':"property_inside_sq_ft",
                             'Lot Size':"property_lot_size",
                             'Property Year Built':"property_year_built",
                             'Balance Owed':"balance_owed",
                             'Short Sale Lender Name':"short_sale_lender_name",
                             'Short Sale Telephone':"short_sale_lender_telephone",
                             'Short Sale Fax':"short_sale_lender_letter_fax",
                             'Short Sale PoC':"point_of_contact",
                             'Lender Verify Info':"lender_verify_info",
                             'Loan Number':"loan_number",
                             'Mailing Cost':"cost",
                             'Letters Mailed':"letters_mailed"
                             }
                             
csv_to_lead_boolean_fields = {"Active":"active",
                              "Deceased":"deceased",
                              "Auction Pending":"auction_pending",
                              "Can Mail Multiple Times":"can_mail_multiple_times",
                              "Return Mail":"return_mail"
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
        
    readonly_fields = ('created_at', 'updated_at',)
    list_display = ('active_string', 'status', 'property_street_address', 'owner_name', 'telephone1', 'telephone2', 'auction_date')
    list_filter = ('active',)
    fieldsets = [
        (None,                  {'fields': [('created_at', 'updated_at'), 'investor', 'status', 'list_source', 'mailing_type', 'deal_type', 'active']}),    
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
            owner_telephone1 = self.getFieldData(row, "Telephone 1")
            owner_telephone2 = self.getFieldData(row, "Telephone 2")
            owner_telephone3 = self.getFieldData(row, "Telephone 3")
            owner_email = self.getFieldData(row, "Email")
            
            auction_date_string = self.getFieldData(row, "Date of Auction")
            try:
                auction_date = datetime.strptime(auction_date_string, "%B %d, %Y")
            except ValueError:
                auction_date = None
            
            investor_string = self.getFieldData(row, "Investor")
            investor = None
            if not investor_string == "":
                investors = Investor.objects.filter(name=investor_string)
                if len(investors) == 0:
                    investor = Investor(name=investor_string)
                    investor.save()
                else:
                    investor = investors[0]
                
            status_string = self.getFieldData(row, "Status")
            status = None
            if not status_string == "":
                statuses = Status.objects.filter(status=status_string)
                if len(statuses) == 0:
                    status = Status(status=status_string)
                    status.save()
                else:
                    status = statuses[0]
                
            list_source_string = self.getFieldData(row, "List Source")
            source = None
            if not list_source_string == "":
                sources = ListSource.objects.filter(source=list_source_string)
                if len(sources) == 0:
                    source = ListSource(source=list_source_string)
                    source.save()
                else:
                    source = sources[0]
                
            mailing_type_string = self.getFieldData(row, "Mailing Type")
            mailing_type = None
            if not mailing_type_string == "":
                mailing_types = MailingType.objects.filter(mailing_type=mailing_type_string)
                if len(mailing_types) == 0:
                    mailing_type = MailingType(mailing_type=mailing_type_string)
                    mailing_type.save()
                else:
                    mailing_type = mailing_types[0]
                
            deal_type_string = self.getFieldData(row, "Deal Type")
            deal_type = None
            if not deal_type_string == "":
                deal_types = DealType.objects.filter(deal_type=deal_type_string)
                if len(deal_types) == 0:
                    deal_type = DealType(deal_type=deal_type_string)
                    deal_type.save()
                else:
                    deal_type = deal_types[0]
                
            property_status_string = self.getFieldData(row, "Property Status")
            property_status = None
            if not property_status_string == "":
                property_statuses = PropertyStatus.objects.filter(property_status=property_status_string)
                if len(property_statuses) == 0:
                    property_status = PropertyStatus(property_status=property_status_string)
                    property_status.save()
                else:
                    property_status = property_statuses[0]
                    
            construction_string = self.getFieldData(row, "Construction")
            construction = None
            if not construction_string == "":
                constructions = Construction.objects.filter(construction_type=construction_string)
                if len(constructions) == 0:
                    construction = Construction(construction_type=construction_string)
                    construction.save()
                else:
                    construction = constructions[0]
            
            lead = Lead.objects.filter(folio_id=folio_id)
            if len(lead) == 0:
                lead = None
            else:
                lead = lead[0]
            if lead is None:
                lead = Lead(last_name=owner_name, annual_bill_balance_year=datetime.now().year,
                            owner_street_address=owner_street_address, owner_city=owner_city, owner_state=owner_state, owner_zip_code=owner_zip_code,
                            telephone1=owner_telephone1, telephone2=owner_telephone2, telephone3=owner_telephone3, email=owner_email)
                            
                lead.auction_date = auction_date
                self.setForeignKey(lead, investor, "investor")
                self.setForeignKey(lead, status, "status")
                self.setForeignKey(lead, source, "list_source")
                self.setForeignKey(lead, mailing_type, "mailing_type")
                self.setForeignKey(lead, deal_type, "deal_type")
                self.setForeignKey(lead, property_status, "property_status")
                self.setForeignKey(lead, construction, "construction")
                
                for column in csv_to_lead_boolean_fields:
                    self.setBooleanField(lead, row, column, csv_to_lead_boolean_fields[column])
                for column in csv_to_lead_field_mapping:
                    self.setFieldData(lead, row, column, csv_to_lead_field_mapping[column])
            else:
                lead.auction_date = auction_date
                lead.annual_bill_balance_year = datetime.now().year
                
                lead.pointofcontact_set.create(last_name=owner_name, street_address=owner_street_address,
                        city=owner_city, state=owner_state, zip_code=owner_zip_code,
                        telephone1=owner_telephone1, telephone2=owner_telephone2, telephone3=owner_telephone3, email=owner_email)
                
            lead.save()
    
    def getFieldData(self, row, field):
        if field in row:
            return row[field].replace('"', '').replace('=', '')
        return ''
        
    def setFieldData(self, lead, row, columnName, fieldName):
        data = self.getFieldData(row, columnName)
        if data != "":
            setattr(lead, fieldName, data)
        
    def setForeignKey(self, lead, field, fieldName):
        """ Set a foreign key value """
        if field is not None:
            setattr(lead, fieldName, field)
            
    def setBooleanField(self, lead, row, columnName, fieldName):
        """ Set a boolean field of lead data """
        boolean_string = self.getFieldData(row, columnName)
        setattr(lead, fieldName, boolean_string.strip().lower() == "yes")

admin.site.register(Construction)
admin.site.register(DealType)
admin.site.register(Investor)
admin.site.register(ListSource)
admin.site.register(MailingType)
admin.site.register(PropertyStatus)
admin.site.register(Status)
admin.site.register(Lead, LeadAdmin)