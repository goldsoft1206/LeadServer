from leads.models import Construction, DealType, Investor, Lead, ListSource, MailingType, PropertyStatus, Status, MailingHistory, PointOfContact
from leads.person import Person

from leads.csv_headers import *

import csv
from datetime import datetime

lead_data_headers = [
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
               
lead_data_to_always_import = [FOLIO_ID,
                              SITUS,
                              ASSESSED_VALUE,
                              USE_CODE,
                              "Legal Description",
                              "Total Balance",
                              "Annual Bill Balance (2012)",
                              "Deed Sale",
                              "Primary Zone",
                              "Land Use",
                              "Previos Sale",
                              "Price",
                              "OR Book Page",
                              "Property Street Address",
                              "Property City",
                              "Property State",
                              "Property Zip Code",
                              'Known Encumbrances',
                              'Bedroom Number',
                              'Bathroom Number',
                              'Inside SQ FT',
                              'Lot Size',
                              'Property Year Built',
                              'Balance Owed',
                              'Short Sale Lender Name',
                              'Short Sale Telephone',
                              'Short Sale Fax',
                              'Short Sale PoC',
                              'Lender Verify Info',
                              'Loan Number',
                              'Mailing Cost',
                              'Letters Mailed']
    
    
def import_leads(file):
    """ Import Leads from the given file """
    reader = csv.DictReader(file.read().splitlines(), restval="")
    suffixes = GetPoCSuffixes(reader)
    
    for row in reader:
        folio_id = GetFieldData(row, "Folio No")
        owner = Person()
        owner.loadFromOwnerData(row, GetFieldData)
        
        pocs = GetPoCPeople(suffixes, row)
        
        auction_date_string = GetFieldData(row, "Date of Auction")
        try:
            auction_date = datetime.strptime(auction_date_string, "%B %d, %Y")
        except ValueError:
            auction_date = None
        
        leads = Lead.objects.filter(folio_id=folio_id)
        needNewLead = len(leads) == 0
        if needNewLead:
            lead = Lead()
        else:
            lead = leads[0]
            
        lead.auction_date = auction_date
        lead.annual_bill_balance_year = datetime.now().year
        
        SetRelatedRecord(lead, row, "Investor", "investor", Investor, "name")
        SetRelatedRecord(lead, row, "Status", "status", Status, "status")
        SetRelatedRecord(lead, row, "List Source", "list_source", ListSource, "source")
        SetRelatedRecord(lead, row, "Mailing Type", "mailing_type", MailingType, "mailing_type")
        SetRelatedRecord(lead, row, "Deal Type", "deal_type", DealType, "deal_type")
        SetRelatedRecord(lead, row, "Property Status", "property_status", PropertyStatus, "property_status")
        SetRelatedRecord(lead, row, "Construction", "construction", Construction, "construction_type")
        
        for column in csv_to_lead_boolean_fields:
            SetBooleanField(lead, row, column, csv_to_lead_boolean_fields[column])
        for column in lead_data_to_always_import:
            SetFieldData(lead, row, column, csv_to_lead_field_mapping[column])
          
        lead.save()
          
        for poc in pocs:
            poc.addPoCDataToLead(lead)
            
        if needNewLead:
            owner.addOwnerDataToLead(lead)
        else:
            owner.addPoCDataToLead(lead)
            
        lead.save()

def GetFieldData(row, field):
    if field in row:
        return row[field].replace('"', '').replace('=', '')
    return ''
    
def SetFieldData(lead, row, columnName, fieldName, ignoreEmptyString=False):
    data = GetFieldData(row, columnName)
    if ignoreEmptyString or data != "":
        setattr(lead, fieldName, data)
        
def SetRelatedRecord(lead, row, columnName, fieldName, recordClass, recordFieldName):
    """ Set a related record of the lead class """
    record = GetRelatedRecord(row, columnName, recordClass, recordFieldName)
    SetForeignKey(lead, record, fieldName)
    
def SetForeignKey(lead, field, fieldName):
    """ Set a foreign key value """
    if field is not None:
        setattr(lead, fieldName, field)
        
def SetBooleanField(lead, row, columnName, fieldName):
    """ Set a boolean field of lead data """
    boolean_string = GetFieldData(row, columnName)
    setattr(lead, fieldName, boolean_string.strip().lower() == "yes")
    
def GetRelatedRecord(row, columnName, recordClass, fieldName):
    """ Return the record related to the given row or create it if it does not exist """
    data = GetFieldData(row, columnName)
    record = None
    if not data == "":
        records = recordClass.objects.filter(**{fieldName:data})
        if len(records) == 0:
            record = recordClass(**{fieldName:data})
            record.save()
        else:
            record = records[0]
            
    return record
    
def GetPoCSuffixes(reader):
    """ Get Point of Contact People suffixes """
    pocSuffixes = {}
    for field in reader.fieldnames:
        if field in lead_data_headers:
           continue
        suffix = field
        for header in csv_poc_headers:
            suffix = suffix.replace(header, "").strip()
        if suffix not in pocSuffixes:
            pocSuffixes[suffix] = []
        pocSuffixes[suffix].append(field)
    return pocSuffixes
    
def GetPoCPeople(suffixes, row):
    """ Get PoC Person Wrappers """
    pocs = []
    for suffix in suffixes:
        poc = Person()
        poc.loadFromPoCData(row, suffixes[suffix], SetFieldData)
        pocs.append(poc)
    return pocs