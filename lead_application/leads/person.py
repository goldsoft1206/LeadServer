from leads.csv_headers import *

class Person:
    """ A class to represent a person """
    
    def __init__(self):
        """ Initialize the Person """
        self.first_name = ""
        self.last_name = ""
        self.street_address = ""
        self.city = ""
        self.state = ""
        self.zip_code = ""
        self.telephone1 = ""
        self.telephone2 = ""
        self.telephone3 = ""
        self.email = ""
    
    def loadFromOwnerData(self, row, GetFieldData):
        """ Load Person Data from a row """
        self.first_name = ""
        self.last_name = GetFieldData(row, OWNER_NAME) + " " + GetFieldData(row, OWNER_SECOND)
        self.street_address = GetFieldData(row, OWNER_STREET_ADDRESS)
        self.city = GetFieldData(row, OWNER_CITY)
        self.state = GetFieldData(row, OWNER_STATE)
        self.zip_code = GetFieldData(row, OWNER_ZIP_CODE)
        self.telephone1 = GetFieldData(row, OWNER_TELEPHONE_1)
        self.telephone2 = GetFieldData(row, OWNER_TELEPHONE_2)
        self.telephone3 = GetFieldData(row, OWNER_TELEPHONE_3)
        self.email = GetFieldData(row, OWNER_EMAIL)
        
        if self.first_name.strip() == "":
            self.first_name = GetFieldData(row, OWNER_FIRST_NAME)
            
        if self.last_name.strip() == "":
            self.last_name = GetFieldData(row, OWNER_LAST_NAME)
        
    def loadFromPoCData(self, row, suffixHeaders, SetFieldData):
        """ Load PoC Data from a row with a given suffix """
        for fullHeader in suffixHeaders:
            for header in csv_poc_headers:
                if header in fullHeader:
                    SetFieldData(self, row, fullHeader, csv_poc_headers[header], ignoreEmptyString=True)
                    break
        
    def addOwnerDataToLead(self, lead):
        """ Add Owner's data to lead as a new Owner """
        if self.shouldAddData():
            lead.first_name=self.first_name
            lead.last_name=self.last_name
            lead.owner_street_address=self.street_address
            lead.owner_city=self.city
            lead.owner_state=self.state
            lead.owner_zip_code=self.zip_code
            lead.telephone1=self.telephone1
            lead.telephone2=self.telephone2
            lead.telephone3=self.telephone3
            lead.email=self.email
        
    def addPoCDataToLead(self, lead):
        """ Add Person's data to lead as a new Point of Contact """
        if self.shouldAddData():
            pocStreetAddresses = [poc.street_address for poc in lead.pointofcontact_set.all()]
            if self.street_address not in pocStreetAddresses:
                lead.pointofcontact_set.create(first_name=self.first_name, last_name=self.last_name, street_address=self.street_address,
                    city=self.city, state=self.state, zip_code=self.zip_code,
                    telephone1=self.telephone1, telephone2=self.telephone2, telephone3=self.telephone3, email=self.email)
                    
    def shouldAddData(self):
        """ Return if the data should be added to a lead """
        fields = [self.first_name,
                  self.last_name,
                  self.street_address,
                  self.city,
                  self.state,
                  self.zip_code,
                  self.telephone1,
                  self.telephone2,
                  self.telephone3,
                  self.email]
                  
        for field in fields:
            if field.strip() != "":
                return True
        else:        
            return False
