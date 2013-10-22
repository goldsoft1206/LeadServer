
FOLIO_ID = "Folio No"
ASSESSED_VALUE = "Assessed Value"
USE_CODE = "Use Code"


SITUS = "Situs"

# Owner Data
OWNER_FIRST_NAME = "Owner First Name"
OWNER_LAST_NAME = "Owner Last Name"
OWNER_STREET_ADDRESS = "Street Address"
OWNER_CITY = "City"
OWNER_STATE = "State"
OWNER_ZIP_CODE = "Zip Code"

# Point of Contact Data
POC_FIRST_NAME = "PoC First Name"
POC_LAST_NAME = "PoC Last Name"
POC_STREET_ADDRESS = "PoC Street Address"
POC_CITY = "PoC City"
POC_STATE = "PoC State"
POC_ZIP_CODE = "PoC Zip Code"
POC_TELEPHONE_1 = "PoC Telephone 1"
POC_TELEPHONE_2 = "PoC Telephone 2"
POC_TELEPHONE_3 = "PoC Telephone 3"
POC_EMAIL = "PoC Email"

csv_to_lead_field_mapping = {FOLIO_ID:"folio_id",
                             SITUS:"property_street_address",
                             ASSESSED_VALUE:"assessed_value",
                             USE_CODE:"use_code",
                             "Legal Description":"legal_description",
                             "Total Balance":"total_balance",
                             "Annual Bill Balance (2012)":"annual_bill_balance",
                             "Deed Sale":"tax_auction",
                             "Primary Zone":"primary_zone",
                             "Land Use":"land_use",
                             "Previos Sale":"previous_sale",
                             "Price":"price",
                             "OR Book Page":"or_book_page",
                             "Property Street Address":"property_street_address",
                             "Property City":"property_city",
                             "Property State":"property_state",
                             "Property Zip Code":"property_zip_code",
                             'Known Encumbrances':"known_encumbrances",
                             'Bedroom Number':"property_bedroom_number",
                             'Bathroom Number':"property_bathroom_number",
                             'Inside SQ FT':"property_inside_sq_ft",
                             'Lot Size':"property_lot_size",
                             'Property Year Built':"property_year_built",
                             'Balance Owed':"balance_owed",
                             'Short Sale Lender Name':"short_sale_lender_name",
                             'Short Sale Telephone':"short_sale_lender_telephone",
                             'Short Sale Fax':"short_sale_lender_letter_fax",
                             'Short Sale PoC':"point_of_contact",
                             'Lender Verify Info':"lender_verify_info",
                             'Loan Number':"loan_number",
                             'Mailing Cost':"cost",
                             'Letters Mailed':"letters_mailed",
                             OWNER_FIRST_NAME:"first_name",
                             OWNER_LAST_NAME:"last_name",
                             OWNER_STREET_ADDRESS:"owner_street_address",
                             OWNER_CITY:"owner_city",
                             OWNER_STATE:"owner_state",
                             OWNER_ZIP_CODE:"owner_zip_code"}
                             
csv_to_lead_boolean_fields = {"Active":"active",
                              "Deceased":"deceased",
                              "Auction Pending":"auction_pending",
                              "Can Mail Multiple Times":"can_mail_multiple_times",
                              "Return Mail":"return_mail"
                             }

csv_poc_headers = {POC_FIRST_NAME:"first_name",
                   POC_LAST_NAME:"last_name",
                   POC_EMAIL:"email",
                   POC_STREET_ADDRESS:"street_address",
                   POC_CITY:"city",
                   POC_STATE:"state",
                   POC_ZIP_CODE:"zip_code",
                   POC_TELEPHONE_1:"telephone1",
                   POC_TELEPHONE_2:"telephone2",
                   POC_TELEPHONE_3:"telephone3"}