from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

import csv

SITUS = "Situs"
OWNER_FIRST_NAME = "Owner First Name"
OWNER_LAST_NAME = "Owner Last Name"
OWNER_STREET_ADDRESS = "Street Address"
OWNER_CITY = "City"
OWNER_STATE = "State"
OWNER_ZIP_CODE = "Zip Code"


csv_headers = [SITUS,
               OWNER_FIRST_NAME,
               OWNER_LAST_NAME,
               OWNER_STREET_ADDRESS,
               OWNER_CITY,
               OWNER_STATE,
               OWNER_ZIP_CODE]

csv_headers_to_data = {SITUS:"property_street_address",
                       OWNER_FIRST_NAME:"first_name",
                       OWNER_LAST_NAME:"last_name",
                       OWNER_STREET_ADDRESS:"owner_street_address",
                       OWNER_CITY:"owner_city",
                       OWNER_STATE:"owner_state",
                       OWNER_ZIP_CODE:"owner_zip_code"}

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
    return csv_headers
    
def GetData(leads):
    """ Return the data for all the leads """
    data = []
    for lead in leads:
        data.append(GetDataFromLead(lead))
    return data
    
def GetDataFromLead(lead):
    """ Get the text data from a single lead """
    data = []
    for header in csv_headers:
        data.append(getattr(lead, csv_headers_to_data[header]))
    return data
    
def GetResponse():
    """ Return the HTTP Response """
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'
    return response