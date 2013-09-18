import datetime
from django.utils import timezone
from django.db import models

class Lead(models.Model):
    # Owner Information
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    
    # Property Information
    folio_id = models.CharField(max_length=200, blank=True, null=True)
    property_street_address = models.CharField(max_length=200, blank=True, null=True)
    property_city = models.CharField(max_length=200, blank=True, null=True)
    property_state = models.CharField(max_length=200, blank=True, null=True)
    property_zip_code = models.CharField(max_length=200, blank=True, null=True)
    
    def owner_name(self):
        return self.first_name + " " + self.last_name
    
    def __unicode__(self):
        return self.owner_name()

class PointOfContact(models.Model):
    lead = models.ForeignKey(Lead)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name
