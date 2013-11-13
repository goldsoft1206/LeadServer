from leads.models import Construction, DealType, Investor, Lead, ListSource, MailingType, PropertyStatus, Status, MailingHistory, PointOfContact, LeadNote
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import render
from django import forms
from django.conf.urls import patterns
from django.contrib.admin.widgets import AdminDateWidget 

from leads.export_helper import export_leads
from leads.import_helper import import_leads

from dbindexer.api import register_index

from datetime import datetime
# register_index(Lead, {'property_street_address': 'icontains'})

class UploadFileForm(forms.Form):
    file  = forms.FileField()
    
class MailingDateForm(forms.Form):
    class Meta:
        widgets = {'mailing_date': forms.DateInput(attrs={'type': 'date'})}
    mailing_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    # mailing_date = forms.DateField(widget=AdminDateWidget)
    
class MailingHistoryInline(admin.StackedInline):
    model = MailingHistory
    extra = 1
    
class LeadNoteInline(admin.StackedInline):
    model = LeadNote
    extra = 1
    template = "admin/leads/lead/notes_stacked.html"
    
    readonly_fields = ('created_at', 'user',)
    
    fieldsets = [
        (None, { 'fields': ['note'] } ),
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'user', None) is None:
            obj.user = request.user
        obj.save()

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
    list_display = ('active_string', 'status', 'property_street_address', 'owner_name', 'telephone1', 'auction_date', 'most_recent_mailing_date', 'next_mailing_date')
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
    
    inlines = [PointOfContactInline, MailingHistoryInline, LeadNoteInline]
    actions = ['make_active', 'make_inactive', 'export', 'add_mailing_date']
    # search_fields = ['property_street_address']
    # ordering = ('idxf_property_street_address_l_icontains',)
    
    def make_active(self, request, queryset):
        queryset.update(active=True)
    make_active.short_description = "Mark selected leads as active"

    def make_inactive(self, request, queryset):
        queryset.update(active=False)
    make_inactive.short_description = "Mark selected leads as inactive"
    
    def export(self, request, queryset):
        return export_leads(queryset)
    export.short_description = "Export selected leads as csv for click2mail integration"
    
    def add_mailing_date(self, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/admin/leads/lead/add-mailings?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
    add_mailing_date.short_description = "Add mailing date to selected leads"
    
    def get_urls(self):
        urls = super(LeadAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^import/$', self.admin_site.admin_view(self.import_leads_view)),
            (r'^add-mailings$', self.admin_site.admin_view(self.add_mailing_dates)),
        )
        return my_urls + urls
        
    def import_leads_view(self, request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                import_leads(request.FILES['file'])
                return HttpResponseRedirect('/admin/leads/lead')
        else:
            form = UploadFileForm()
            
        c = {'form': form}
        c.update(csrf(request))
        return HttpResponseRedirect('/admin/leads/lead')
    
    def add_mailing_dates(self, request):
        """ Render the Mailing date page or add the submitted date """
        if request.method == "GET":
            form = MailingDateForm()
            object_ids = [long(value) for value in request.GET["ids"].split(",")]
            queryset = Lead.objects.filter(id__in=object_ids)
            return render(request, 'add_mailing_date.html', {'app_label':'leads', 'admin_urlname':'leads', 'queryset':queryset, 'object_ids':request.GET["ids"], 'form':form})
        else:
            object_ids = [long(value) for value in request.POST["ids"].split(",")]
            queryset = Lead.objects.filter(id__in=object_ids)
            date = datetime.strptime(request.POST['mailing_date'], "%Y-%m-%d")
            for lead in queryset:
                lead.mailinghistory_set.create(mailing_date=date)
            return HttpResponseRedirect('/admin/leads/lead')
        
    def save_formset(self, request, form, formset, change):
        if not change:
            instances = formset.save(commit=False)
            for instance in instances:
                if hasattr(instance, 'user') and not change:
                    has_user = True
                    instance.user = request.user
                    instance.save()
            formset.save_m2m()
        else:
            admin.ModelAdmin.save_formset(self, request, form, formset, change)
    

admin.site.register(Construction)
admin.site.register(DealType)
admin.site.register(Investor)
admin.site.register(ListSource)
admin.site.register(MailingType)
admin.site.register(PropertyStatus)
admin.site.register(Status)
admin.site.register(Lead, LeadAdmin)