import datetime
from django.utils import timezone
from django.db import models

class Lead(models.Model):
    investor_name = models.CharField(max_length=200)
    
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
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
