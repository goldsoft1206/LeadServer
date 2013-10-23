import datetime
from django.utils import timezone
from django.db import models

class Construction(models.Model):
    construction_type = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.construction_type

class DealType(models.Model):
    deal_type = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.deal_type

class Investor(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name
        
class ListSource(models.Model):
    source = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.source
        
class MailingType(models.Model):
    mailing_type = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.mailing_type
        
class PropertyStatus(models.Model):
    property_status = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.property_status
        
class Status(models.Model):
    status = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.status

class Lead(models.Model):
    # Admin Data
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    # Core
    investor = models.ForeignKey(Investor, blank=True, null=True)
    status = models.ForeignKey(Status, blank=True, null=True)
    list_source = models.ForeignKey(ListSource, blank=True, null=True)
    mailing_type = models.ForeignKey(MailingType, blank=True, null=True)
    deal_type = models.ForeignKey(DealType, blank=True, null=True)
    active = models.BooleanField()
    
    # Owner Information
    deceased = models.BooleanField()
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    owner_street_address = models.CharField("Street address", max_length=200, blank=True, null=True)
    owner_city = models.CharField("City", max_length=200, blank=True, null=True)
    owner_state = models.CharField("State", max_length=200, blank=True, null=True)
    owner_zip_code = models.CharField("Zip code", max_length=200, blank=True, null=True)
    telephone1 = models.CharField("Telephone 1", max_length=200, blank=True, null=True)
    telephone2 = models.CharField("Telephone 2", max_length=200, blank=True, null=True)
    telephone3 = models.CharField("Telephone 3", max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    
    # Property Information
    folio_id = models.CharField("Folio ID", max_length=200, blank=True, null=True)
    property_street_address = models.CharField("Street address", max_length=200, blank=True, null=True)
    property_city = models.CharField("City", max_length=200, blank=True, null=True)
    property_state = models.CharField("State", max_length=200, blank=True, null=True)
    property_zip_code = models.CharField("Zip code", max_length=200, blank=True, null=True)
    property_status = models.ForeignKey(PropertyStatus, blank=True, null=True)
    known_encumbrances = models.CharField(max_length=200, blank=True, null=True)
    assessed_value = models.CharField(max_length=200, blank=True, null=True)
    use_code = models.CharField(max_length=200, blank=True, null=True)
    legal_description = models.CharField(max_length=200, blank=True, null=True)
    total_balance = models.CharField(max_length=200, blank=True, null=True)
    annual_bill_balance = models.CharField(max_length=200, blank=True, null=True)
    annual_bill_balance_year = models.IntegerField(default=0, blank=True, null=True)
    tax_auction = models.CharField(max_length=200, blank=True, null=True)
    primary_zone = models.CharField(max_length=200, blank=True, null=True)
    land_use = models.CharField(max_length=200, blank=True, null=True)
    previous_sale = models.CharField(max_length=200, blank=True, null=True)
    price = models.CharField(max_length=200, blank=True, null=True)
    or_book_page = models.CharField("OR Book Page", max_length=200, blank=True, null=True)
    # Property Characteristics
    property_bedroom_number = models.DecimalField("Number of bedrooms", max_digits=19, decimal_places=1, default=0, blank=True, null=True)
    property_bathroom_number = models.DecimalField("Number of bathrooms", max_digits=19, decimal_places=1, default=0, blank=True, null=True)
    property_inside_sq_ft = models.IntegerField("Inside SQ FT", default=0, blank=True, null=True)
    property_lot_size = models.IntegerField("Lot size", default=0, blank=True, null=True)
    construction = models.ForeignKey(Construction, blank=True, null=True)
    property_year_built = models.IntegerField("Year built", default=0, blank=True, null=True)
    # Tax Info
    auction_pending = models.BooleanField()
    balance_owed = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    auction_date = models.DateField(blank=True, null=True)
    
    # Short Sale Lender
    short_sale_lender_name = models.CharField("Lender name", max_length=200, blank=True, null=True)
    short_sale_lender_telephone = models.CharField("Telephone", max_length=200, blank=True, null=True)
    short_sale_lender_letter_fax = models.CharField("Letter fax", max_length=200, blank=True, null=True)
    point_of_contact = models.CharField(max_length=200, blank=True, null=True)
    lender_verify_info = models.CharField(max_length=200, blank=True, null=True)
    loan_number = models.CharField(max_length=200, blank=True, null=True)
    
    # Mail/Campaign Info
    cost = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    letters_mailed = models.IntegerField(default=0, blank=True, null=True)
    can_mail_multiple_times = models.BooleanField()
    return_mail = models.BooleanField()
    
    def active_string(self):
        if self.active:
            return "ACTIVE"
        else:
            return "INACTIVE"
    active_string.short_description = "Active"
    active_string.admin_order_field = 'active'
    
    def owner_name(self):
        name = ""
        if self.first_name is not None:
            name += self.first_name
            name += " "
        if self.last_name is not None:
            name += self.last_name
        
        return name
    
    def __unicode__(self):
        return self.owner_name()
        
class MailingHistory(models.Model):
    class Meta:
        verbose_name_plural = "mailing histories"
        
    lead = models.ForeignKey(Lead)
    returned_envelope = models.BooleanField()
    mailing_date = models.DateField(blank=True, null=True)
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name

class PointOfContact(models.Model):
    lead = models.ForeignKey(Lead)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=200, blank=True, null=True)
    telephone1 = models.CharField("Telephone 1", max_length=200, blank=True, null=True)
    telephone2 = models.CharField("Telephone 2", max_length=200, blank=True, null=True)
    telephone3 = models.CharField("Telephone 3", max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    
    def __unicode__(self):
        name = ""
        if self.first_name is not None:
            name += self.first_name
            name += " "
        if self.last_name is not None:
            name += self.last_name
        
        return name
