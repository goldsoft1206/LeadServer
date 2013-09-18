import datetime
from django.utils import timezone
from django.db import models

class Lead(models.Model):
    investor_name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.investor_name

class Owner(models.Model):
    lead = models.ForeignKey(Lead)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name
