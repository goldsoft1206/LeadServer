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
                  
poc_export_headers = [POC_FIRST_NAME,
                      POC_LAST_NAME,
                      POC_STREET_ADDRESS,
                      POC_CITY,
                      POC_STATE,
                      POC_ZIP_CODE]

def export_leads(leads):
    """ Export the given leads """
    response = GetResponse()
    writer = csv.writer(response)
    headers = GetHeaders(leads)
    data = GetData(leads, headers)
    writer.writerow(headers)
    writer.writerows(data)
    return response
    
def GetHeaders(leads):
    """ Return the column headers for the csv file """
    headers = export_headers + GetPoCHeaders(leads)
    AddDeedSaleHeader(headers)
    
    return headers
    
def GetPoCHeaders(leads):
    """ Return the necessary PoC Headers """
    max = 0
    for lead in leads:
        numPoCs = lead.pointofcontact_set.count()
        if numPoCs > max:
            max = numPoCs
    
    headers = []
    for i in range(max):
        for header in poc_export_headers:
            headers.append("{0} {1}".format(header, i+1))
    return headers
    
def AddDeedSaleHeader(headers):
    """ Adds the Deed Sale Header to the 15th column.
        Which is required for click2mail integration. """
    if len(headers) <= 14:
        for i in range(14-len(headers)): # This should be empty if there are already 14 headers
            headers.append("")
        headers.append(DEED_SALE)
    else:
        headers[14:14] = [DEED_SALE]
        
def GetData(leads, headers):
    """ Return the data for all the leads """
    data = []
    for lead in leads:
        data.append(GetDataFromLead(lead, headers))
    return data
    
def GetDataFromLead(lead, headers):
    """ Get the text data from a single lead """
    data = []
    
    for header in headers:
        fieldData = ""
        if header in export_headers or header == DEED_SALE:
            fieldData = GetLeadData(lead, header)
        elif header == "":
            fieldData = ""
        else:
            fieldData = GetPoCData(lead, header)
        data.append(fieldData)
    return data
    
def GetLeadData(lead, header):
    """ Get Data from a particular lead field """
    return getattr(lead, csv_to_lead_field_mapping[header])
    
def GetPoCData(lead, header):
    """ Get Data from a particular lead field """
    poc, realHeader = GetPointOfContactForHeader(lead, header)
    
    if poc is not None:
        return getattr(poc, csv_poc_headers[realHeader])
    else:
        return ""
    
def GetPointOfContactForHeader(lead, header):
    """ Return the Point of COntact associated with a particular header for a lead """
    poc = None
    pocIndexString = header
    
    for pocHeader in poc_export_headers:
        pocIndexString = pocIndexString.replace(pocHeader, "").strip()
    pocIndex = int(pocIndexString)
    
    if pocIndex < lead.pointofcontact_set.count():
        poc = lead.pointofcontact_set.all()[pocIndex]
    return poc, header.replace(pocIndexString, "").strip()
    
def GetResponse():
    """ Return the HTTP Response """
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'
    return response