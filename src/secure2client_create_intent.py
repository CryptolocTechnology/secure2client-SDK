#!/usr/bin/python

from secure2client_data import IntentData, RecipientData, RecipientsJson, IntentResponse



class CreateIntent:
    '''
    Secure2Client share types can be of these 3 types: "download", "sign_reciept", "sign_agree"
    Must be presented as below
    '''
    DOWNLOAD_SHARE_TYPE = "download"
    RECIEPT_SHARE_TYPE = "sign as recieved"
    SIGN_SHARE_TYPE = "sign and agree"


    def __init__(self, tokenIdentityHandler, tokenHandler, apiHandler):

        self.tokenIdentityHandler = tokenIdentityHandler
        self.tokenHandler = tokenHandler
        self.apiHandler = apiHandler

        self.intent_id = None
        self.file_id = None

        self.expiryDate = "2019-11-01"
        self.filename = "<PATH TO FILE>"
        self.filesize = <ACTUAL FILE SIZE IN BYTES>
        self.alias = "<ANY STRING>"
        self.shareType = self.SIGN_SHARE_TYPE


    def create_recipient_list(self):

        recipientList = []

        recipientList.append(RecipientData("<FIRSTNAME>", "<MIDDLENAME>", "<LASTNAME>", "<COUNTRYCODE>", "<MOBILENUMBER>",
                                            "<EMAIL>").json_recipient())
    
        recipient_list.append(RecipientData("<FIRSTNAME>", "<MIDDLENAME>", "<LASTNAME>", "<COUNTRYCODE>", "<MOBILENUMBER>",
                                                        "<EMAIL>").json_recipient())

        jsonRecipientListHandler = RecipientsJson(recipientList)

        return jsonRecipientListHandler.get_json_recipients()


    def get_json_intent_data(self):

        try:
            intent_data = IntentData(self.tokenIdentityHandler.username, self.tokenIdentityHandler.password,
                                        self.shareType, self.expiryDate, self.filename, self.filesize,
                                            self.create_recipient_list(), self.alias)

            intent_data_json = intent_data.json_intent_data()
            print intent_data_json
            return intent_data_json

        except Exception as e:
            print ("Error creating intent data: %s" % e.message)


    def extract_intent_response(self, intent_response):

        intent_response_data = IntentResponse(intent_response)

        self.intent_id = intent_response_data.get_intent_id()
        self.file_id = intent_response_data.get_file_id()

        return


    def send_intent(self):

        api_request = "create_trustshare_intent"
        request_headers = None
        data = self.get_json_intent_data()

        no_errors, validated_id_token = self.tokenHandler.get_validated_id_token()

        if no_errors:
            no_errors, create_trustshare_intent_response = self.apiHandler.hit_endpoint(api_request, validated_id_token,
                                                                self.tokenIdentityHandler.api_key, request_headers, data)
            print create_trustshare_intent_response
            self.extract_intent_response(create_trustshare_intent_response)
            return

