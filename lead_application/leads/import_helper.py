from leads.models import Construction, DealType, Investor, Lead, ListSource, MailingType, PropertyStatus, Status, MailingHistory, PointOfContact
from leads.person import Person

from leads.csv_headers import *

import csv
from datetime import datetime
               
lead_data_to_always_import = [FOLIO_ID,
                              SITUS,
                              ASSESSED_VALUE,
                              USE_CODE,
                              LEGAL_DESCRIPTION,
                              TOTAL_BALANCE,
                              ANNUAL_BILL_BALANCE,
                              DEED_SALE,
                              PRIMARY_ZONE,
                              LAND_USE,
                              PREVIOUS_SALE,
                              PRICE,
                              OR_BOOK_PAGE,
                              PROPERTY_STREET_ADDRESS,
                              PROPERTY_CITY,
                              PROPERTY_STATE,
                              PROPERTY_ZIP_CODE,
                              KNOWN_ENCUMBRANCES,
                              BEDROOM_NUMBER,
                              BATHROOM_NUMBER,
                              INSIDE_SQ_FT,
                              LOT_SIZE,
                              PROPERTY_YEAR_BUILT,
                              BALANCE_OWED,
                              SHORT_SALE_LENDER_NAME,
                              SHORT_SALE_TELEPHONE,
                              SHORT_SALE_FAX,
                              SHORT_SALE_POC,
                              LENDER_VERIFY_INFO,
                              LOAN_NUMBER,
                              MAILING_COST,
                              LETTERS_MAILED]
    
    
def import_leads(file):
    """ Import Leads from the given file """
    reader = csv.DictReader(file.read().splitlines(), restval="")
    suffixes = GetPoCSuffixes(reader)
    
    for row in reader:
        folio_id = GetFieldData(row, FOLIO_ID)
        owner = Person()
        owner.loadFromOwnerData(row, GetFieldData)
        
        pocs = GetPoCPeople(suffixes, row)
        
        auction_date_string = GetFieldData(row, DATE_OF_AUCTION)
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
        print auction_date    
        lead.auction_date = auction_date
        lead.annual_bill_balance_year = datetime.now().year
        
        SetRelatedRecord(lead, row, INVESTOR, "investor", Investor, "name")
        SetRelatedRecord(lead, row, STATUS, "status", Status, "status")
        SetRelatedRecord(lead, row, LIST_SOURCE, "list_source", ListSource, "source")
        SetRelatedRecord(lead, row, MAILING_TYPE, "mailing_type", MailingType, "mailing_type")
        SetRelatedRecord(lead, row, DEAL_TYPE, "deal_type", DealType, "deal_type")
        SetRelatedRecord(lead, row, PROPERTY_STATUS, "property_status", PropertyStatus, "property_status")
        SetRelatedRecord(lead, row, CONSTRUCTION, "construction", Construction, "construction_type")
        
        for column in lead_boolean_fields:
            SetBooleanField(lead, row, column, csv_to_lead_field_mapping[column])
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
        if field in csv_to_lead_field_mapping:
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