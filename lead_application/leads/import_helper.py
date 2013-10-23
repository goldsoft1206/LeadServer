from leads.models import Construction, DealType, Investor, Lead, ListSource, MailingType, PropertyStatus, Status, PointOfContact
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
                              LETTERS_MAILED,
                              ACTIVE,
                              OWNER_DECEASED,
                              AUCTION_PENDING,
                              CAN_MAIL_MULTIPLE_TIMES,
                              RETURN_MAIL,
                              INVESTOR,
                              STATUS,
                              LIST_SOURCE,
                              MAILING_TYPE,
                              DEAL_TYPE,
                              PROPERTY_STATUS,
                              CONSTRUCTION,
                              DATE_OF_AUCTION]
    
    
def import_leads(file):
    """ Import Leads from the given file """
    reader = csv.DictReader(file.read().splitlines(), restval="")
    suffixes = GetPoCSuffixes(reader)
    
    for row in reader:
        folio_id = GetFieldData(row, FOLIO_ID)
        
        owner = Person()
        owner.loadFromOwnerData(row, GetFieldData)
        pocs = GetPoCPeople(suffixes, row)
        
        lead, isNewLead = GetLead(folio_id)
        lead.annual_bill_balance_year = datetime.now().year
        
        for column in lead_data_to_always_import:
            SetFieldData(lead, row, column)
        lead.save() # Save so PoC Creation has a record to attach to
          
        for poc in pocs:
            poc.addPoCDataToLead(lead)
            
        if isNewLead:
            owner.addOwnerDataToLead(lead)
        else:
            owner.addPoCDataToLead(lead)
            
        lead.save()
        
def GetLead(folio_id):
    """ Get the Lead for the given Folio ID or create one if one does not exist """
    leads = Lead.objects.filter(folio_id=folio_id)
    needNewLead = len(leads) == 0
    if needNewLead:
        lead = Lead()
    else:
        lead = leads[0]
    return lead, needNewLead

def GetFieldData(row, field):
    if field in row:
        return row[field].replace('"', '').replace('=', '')
    return ''
    
def SetFieldData(lead, row, columnName):
    """ Set Lead field data """
    fieldName = csv_to_lead_field_mapping[columnName]
    
    if columnName in lead_relation_fields:
        SetRelatedRecord(lead, row, columnName, fieldName)
    elif columnName in lead_boolean_fields:
        SetBooleanField(lead, row, columnName, fieldName)
    elif columnName in lead_date_fields:
        SetDateField(lead, row, columnName, fieldName)
    else:
        SetStringField(lead, row, columnName, fieldName)
        
def SetStringField(lead, row, columnName, fieldName, ignoreEmptyString=False):
    """ Set a string field of data """
    data = GetFieldData(row, columnName)
    if ignoreEmptyString or data != "":
        setattr(lead, fieldName, data)
        
def SetRelatedRecord(lead, row, columnName, fieldName):
    """ Set a related record of the lead class """
    recordClass = lead_relation_header_to_model[columnName]
    recordFieldName = lead_relation_header_to_field[columnName]
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
    
def SetDateField(lead, row, columnName, fieldName):
    """ Set a Date Field """
    date_string = GetFieldData(row, columnName)
    try:
        date = datetime.strptime(date_string, "%B %d, %Y")
        setattr(lead, fieldName, date)
    except ValueError:
        pass # Do nothing since the date field was malformed
    
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
        poc.loadFromPoCData(row, suffixes[suffix], SetStringField)
        pocs.append(poc)
    return pocs