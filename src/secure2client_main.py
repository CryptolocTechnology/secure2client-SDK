#!/usr/bin/python

from secure2client_identity import CreateCognitoTokenHandler
from secure2client_endpoints import EndpointHandler
#from secure2client_data import IntentData, RecipientData, RecipientsJson, S3UrlData, HistoryData
#from secure2client_response import IntentResponse
from secure2client_file_upload import FileUpload
from secure2client_create_intent import CreateIntent
from secure2client_s3_url import S3Url
from secure2client_history import History



# Setup token identity
token_identity_handler = CreateCognitoTokenHandler()

# Create token handler
no_errors, token_handler = token_identity_handler.get_handler()

# Setup API client
api_handler = EndpointHandler()

# Create intent
intentHandler = CreateIntent(token_identity_handler, token_handler, api_handler)
create_trustshare_intent_response = intentHandler.send_intent()

# Get S3 URL file upload location
s3UrlHandler = S3Url(token_identity_handler, token_handler, api_handler, intentHandler)
get_s3_url_response = s3UrlHandler.get_s3_url()

# Upload file
upload_handler = FileUpload(get_s3_url_response)
upload_result = upload_handler.s3_upload_small()
print upload_result

# Confirm file upload to initiate shares to recipients
final_response = s3UrlHandler.confirm_s3_upload()

# Output history from this date
history_date = "2017-11-01 00:00:00"
history_handler = History(token_identity_handler, token_handler, api_handler)
history_handler.output_all_history(history_date)
