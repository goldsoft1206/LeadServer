
class Person:
    """ A class to represent a person """
    
    def loadFromOwnerData(self, row, GetFieldData):
        """  """
        self.first_name = ""
        self.last_name = GetFieldData(row, "Owner") + " " + GetFieldData(row, "Owner Second")
        self.street_address = GetFieldData(row, "Street Address")
        self.city = GetFieldData(row, "City")
        self.state = GetFieldData(row, "State")
        self.zip_code = GetFieldData(row, "Zip Code")
        self.telephone1 = GetFieldData(row, "Telephone 1")
        self.telephone2 = GetFieldData(row, "Telephone 2")
        self.telephone3 = GetFieldData(row, "Telephone 3")
        self.email = GetFieldData(row, "Email")
        
    def addOwnerDataToLead(self, lead):
        """ Add Owner's data to lead as a new Owner """
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
        lead.pointofcontact_set.create(last_name=self.last_name, street_address=self.street_address,
                    city=self.city, state=self.state, zip_code=self.zip_code,
                    telephone1=self.telephone1, telephone2=self.telephone2, telephone3=self.telephone3, email=self.email)