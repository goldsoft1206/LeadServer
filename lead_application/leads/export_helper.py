from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

from leads.csv_headers import *

import csv

export_headers = [SITUS,
                  OWNER_FIRST_NAME,
                  OWNER_LAST_NAME,
                  OWNER_STREET_ADDRESS,
                  OWNER_CITY,
                  OWNER_STATE,
                  OWNER_ZIP_CODE]

def export_leads(leads):
    """ Export the given leads """
    response = GetResponse()
    writer = csv.writer(response)
    headers = GetHeaders(leads)
    data = GetData(leads)
    writer.writerow(headers)
    writer.writerows(data)
    return response
    
def GetHeaders(leads):
    """ Return the column headers for the csv file """
    return export_headers
    
def GetData(leads):
    """ Return the data for all the leads """
    data = []
    for lead in leads:
        data.append(GetDataFromLead(lead))
    return data
    
def GetDataFromLead(lead):
    """ Get the text data from a single lead """
    data = []
    for header in export_headers:
        data.append(getattr(lead, csv_to_lead_field_mapping[header]))
    return data
    
def GetResponse():
    """ Return the HTTP Response """
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'
    return response