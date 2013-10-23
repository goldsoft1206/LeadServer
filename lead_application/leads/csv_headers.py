from leads.models import Construction, DealType, Investor, ListSource, MailingType, PropertyStatus, Status

# Standard Headers
FOLIO_ID = "Folio No"
ACTIVE = "Active"
DATE_OF_AUCTION = "Date of Auction"
SITUS = "Situs"
ASSESSED_VALUE = "Assessed Value"
USE_CODE = "Use Code"
LEGAL_DESCRIPTION = "Legal Description"
TOTAL_BALANCE = "Total Balance"
ANNUAL_BILL_BALANCE = "Annual Bill Balance (2012)"
DEED_SALE = "Deed Sale"
PRIMARY_ZONE = "Primary Zone"
LAND_USE = "Land Use"
PREVIOUS_SALE = "Previous Sale"
PRICE = "Price"
OR_BOOK_PAGE = "OR Book Page"

# Owner Headers
OWNER_DECEASED = "Deceased"
OWNER_NAME = "Owner"
OWNER_SECOND = "Owner Second"
OWNER_FIRST_NAME = "Owner First Name"
OWNER_LAST_NAME = "Owner Last Name"
OWNER_STREET_ADDRESS = "Street Address"
OWNER_CITY = "City"
OWNER_STATE = "State"
OWNER_ZIP_CODE = "Zip Code"
OWNER_TELEPHONE_1 = "Telephone 1"
OWNER_TELEPHONE_2 = "Telephone 2"
OWNER_TELEPHONE_3 = "Telephone 3"
OWNER_EMAIL = "Email"

# Property Headers
PROPERTY_STREET_ADDRESS = "Property Street Address"
PROPERTY_CITY = "Property City"
PROPERTY_STATE = "Property State"
PROPERTY_ZIP_CODE = "Property Zip Code"
KNOWN_ENCUMBRANCES = 'Known Encumbrances'
BEDROOM_NUMBER = 'Bedroom Number'
BATHROOM_NUMBER = 'Bathroom Number'
INSIDE_SQ_FT = 'Inside SQ FT'
LOT_SIZE = 'Lot Size'
PROPERTY_YEAR_BUILT = 'Property Year Built'
BALANCE_OWED = 'Balance Owed'
AUCTION_PENDING = "Auction Pending"

# Short Sale Lender Headers
SHORT_SALE_LENDER_NAME = 'Short Sale Lender Name'
SHORT_SALE_TELEPHONE = 'Short Sale Telephone'
SHORT_SALE_FAX = 'Short Sale Fax'
SHORT_SALE_POC = 'Short Sale PoC'
LENDER_VERIFY_INFO = 'Lender Verify Info'
LOAN_NUMBER = 'Loan Number'

# Campaign Mailing Headers
MAILING_COST = 'Mailing Cost'
LETTERS_MAILED = 'Letters Mailed'
CAN_MAIL_MULTIPLE_TIMES = "Can Mail Multiple Times"
RETURN_MAIL = "Return Mail"

# Data Relationship Headers
INVESTOR = "Investor"
STATUS = "Status"
LIST_SOURCE = "List Source"
MAILING_TYPE = "Mailing Type"
DEAL_TYPE = "Deal Type"
PROPERTY_STATUS = "Property Status"
CONSTRUCTION = "Construction"

# Point of Contact Headers
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
                             DATE_OF_AUCTION:"auction_date",
                             SITUS:"property_street_address",
                             ASSESSED_VALUE:"assessed_value",
                             USE_CODE:"use_code",
                             LEGAL_DESCRIPTION:"legal_description",
                             TOTAL_BALANCE:"total_balance",
                             ANNUAL_BILL_BALANCE:"annual_bill_balance",
                             DEED_SALE:"tax_auction",
                             PRIMARY_ZONE:"primary_zone",
                             LAND_USE:"land_use",
                             PREVIOUS_SALE:"previous_sale",
                             PRICE:"price",
                             OR_BOOK_PAGE:"or_book_page",
                             PROPERTY_STREET_ADDRESS:"property_street_address",
                             PROPERTY_CITY:"property_city",
                             PROPERTY_STATE:"property_state",
                             PROPERTY_ZIP_CODE:"property_zip_code",
                             KNOWN_ENCUMBRANCES:"known_encumbrances",
                             BEDROOM_NUMBER:"property_bedroom_number",
                             BATHROOM_NUMBER:"property_bathroom_number",
                             INSIDE_SQ_FT:"property_inside_sq_ft",
                             LOT_SIZE:"property_lot_size",
                             PROPERTY_YEAR_BUILT:"property_year_built",
                             BALANCE_OWED:"balance_owed",
                             SHORT_SALE_LENDER_NAME:"short_sale_lender_name",
                             SHORT_SALE_TELEPHONE:"short_sale_lender_telephone",
                             SHORT_SALE_FAX:"short_sale_lender_letter_fax",
                             SHORT_SALE_POC:"point_of_contact",
                             LENDER_VERIFY_INFO:"lender_verify_info",
                             LOAN_NUMBER:"loan_number",
                             MAILING_COST:"cost",
                             LETTERS_MAILED:"letters_mailed",
                             OWNER_NAME:"last_name",
                             OWNER_SECOND:"last_name",
                             OWNER_FIRST_NAME:"first_name",
                             OWNER_LAST_NAME:"last_name",
                             OWNER_STREET_ADDRESS:"owner_street_address",
                             OWNER_CITY:"owner_city",
                             OWNER_STATE:"owner_state",
                             OWNER_ZIP_CODE:"owner_zip_code",
                             OWNER_TELEPHONE_1:"telephone1",
                             OWNER_TELEPHONE_2:"telephone2",
                             OWNER_TELEPHONE_3:"telephone3",
                             OWNER_EMAIL:"email",
                             ACTIVE:"active",
                             OWNER_DECEASED:"deceased",
                             AUCTION_PENDING:"auction_pending",
                             CAN_MAIL_MULTIPLE_TIMES:"can_mail_multiple_times",
                             RETURN_MAIL:"return_mail",
                             INVESTOR:"investor",
                             STATUS:"status",
                             LIST_SOURCE:"list_source",
                             MAILING_TYPE:"mailing_type",
                             DEAL_TYPE:"deal_type",
                             PROPERTY_STATUS:"property_status",
                             CONSTRUCTION:"construction"}
                             
lead_boolean_fields = [ACTIVE,
                       OWNER_DECEASED,
                       AUCTION_PENDING,
                       CAN_MAIL_MULTIPLE_TIMES,
                       RETURN_MAIL]
                       
lead_date_fields = [DATE_OF_AUCTION]
                       
lead_relation_fields = [INVESTOR,
                        STATUS,
                        LIST_SOURCE,
                        MAILING_TYPE,
                        DEAL_TYPE,
                        PROPERTY_STATUS,
                        CONSTRUCTION]
                        
lead_relation_header_to_model = {INVESTOR:Investor,
                                 STATUS:Status,
                                 LIST_SOURCE:ListSource,
                                 MAILING_TYPE:MailingType,
                                 DEAL_TYPE:DealType,
                                 PROPERTY_STATUS:PropertyStatus,
                                 CONSTRUCTION:Construction}

lead_relation_header_to_field = {INVESTOR:"name",
                                 STATUS:"status",
                                 LIST_SOURCE:"source",
                                 MAILING_TYPE:"mailing_type",
                                 DEAL_TYPE:"deal_type",
                                 PROPERTY_STATUS:"property_status",
                                 CONSTRUCTION:"construction_type"}
                                 
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