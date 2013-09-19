import datetime
from django.utils import timezone
from django.db import models

class Investor(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name

class Lead(models.Model):
    # Core
    investor = models.ForeignKey(Investor, null=True)
    # status 
    
    # Owner Information
    deceased = models.BooleanField()
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    owner_street_address = models.CharField(max_length=200, blank=True, null=True)
    owner_city = models.CharField(max_length=200, blank=True, null=True)
    owner_state = models.CharField(max_length=200, blank=True, null=True)
    owner_zip_code = models.CharField(max_length=200, blank=True, null=True)
    telephone1 = models.CharField(max_length=200, blank=True, null=True)
    telephone2 = models.CharField(max_length=200, blank=True, null=True)
    telephone3 = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    
    # Property Information
    folio_id = models.CharField(max_length=200, blank=True, null=True)
    property_street_address = models.CharField(max_length=200, blank=True, null=True)
    property_city = models.CharField(max_length=200, blank=True, null=True)
    property_state = models.CharField(max_length=200, blank=True, null=True)
    property_zip_code = models.CharField(max_length=200, blank=True, null=True)
    # Property Characteristics
    property_bedroom_number = models.IntegerField(default=0, blank=True, null=True)
    property_bathroom_number = models.IntegerField(default=0, blank=True, null=True)
    property_inside_sq_ft = models.IntegerField(default=0, blank=True, null=True)
    property_lot_size = models.IntegerField(default=0, blank=True, null=True)
    property_year_built = models.IntegerField(default=0, blank=True, null=True)
    # Tax Info
    auction_pending = models.BooleanField()
    balance_owed = models.FloatField(default=0, blank=True, null=True)
    auction_date = models.DateField(blank=True, null=True)
    
    # Short Sale Lender
    short_sale_lender_name = models.CharField(max_length=200, blank=True, null=True)
    short_sale_lender_telephone = models.CharField(max_length=200, blank=True, null=True)
    short_sale_lender_letter_fax = models.CharField(max_length=200, blank=True, null=True)
    point_of_contact = models.CharField(max_length=200, blank=True, null=True)
    lender_verify_info = models.CharField(max_length=200, blank=True, null=True)
    loan_number = models.CharField(max_length=200, blank=True, null=True)
    
    def owner_name(self):
        return self.first_name + " " + self.last_name
    
    def __unicode__(self):
        return self.owner_name()

class PointOfContact(models.Model):
    lead = models.ForeignKey(Lead)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    zip_code = models.CharField(max_length=200, blank=True, null=True)
    telephone1 = models.CharField(max_length=200, blank=True, null=True)
    telephone2 = models.CharField(max_length=200, blank=True, null=True)
    telephone3 = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name
