#!/usr/bin/python

from datetime import datetime
import json



class IntentResponse:

    def __init__(self, json_intent_response):

        self.intent_response = json_intent_response


    def get_intent_id(self):

        intent_dict = json.loads(self.intent_response)
        return intent_dict['intent_id']


    def get_file_id(self):

        intent_dict = json.loads(self.intent_response)
        return intent_dict['file_id']



class IntentData:

    share_types = ["download", "sign as recieved", "sign and agree"]

    def __init__(self, username, password, share_type, expiry, filename, filesize, json_recipient_list, notes="", alias="default-alias"):

        self.username = username
        self.password = password
        self.share_type = share_type
        self.alias = alias
        self.expiry = expiry
        self.filename = filename
        self.filesize = filesize
        self.notes = notes
        self.recipient_list = json_recipient_list

        return self._validate_init_data(share_type, expiry, filesize)


    def _validate_init_data(self, input_share_type, input_expiry, input_filesize):

        valid = self._validate_sharetype(input_share_type) and self._validate_filesize(input_filesize)
                            #  and self._validate_expiry(input_expiry)
        if valid:
            return None
        else:
            # This is to return an init validation failure
            return 1


    def _validate_sharetype(self, input_type):

        if input_type in self.share_types:
            return True
        else:
            return False


    def _validate_expiry(self, input_expiry):

        date_format = '%Y-%m-%dT%H:%M:%S%z'
        try:
            return datetime.strptime(input_expiry, date_format)
        except ValueError:
            return False


    def _validate_filesize(self, input_filesize):

        try:
            return int(input_filesize)
        except ValueError:
            return False


    def json_intent_data(self):

        data = {}
        data['username'] = self.username
        data['password'] = self.password
        data['alias_id'] = self.alias
        data['expiry'] = self.expiry
        data['trustshare_type'] = self.share_type
        data['recipients'] = json.loads(self.recipient_list)
        data['filename'] = self.filename
        data['filesize'] = self.filesize
        data['notes'] = self.notes

        return json.dumps(data)



class RecipientData:

    def __init__(self, first_name, middle_name, last_name, mobile_region, mobile_number, email):

        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.mobile_region = mobile_region
        self.mobile_number = mobile_number
        self.email = email


    def json_recipient(self):

        data = {}
        data['first_name'] = self.first_name
        data['middle_name'] = self.middle_name
        data['last_name'] = self.last_name
        data['mobile_region'] = self.mobile_region
        data['mobile_number'] = self.mobile_number
        data['email'] = self.email

        return json.dumps(data)



class RecipientsJson():

    def __init__(self, recipient_list):

        self.recipient_list = recipient_list
        self.json_recipients = self._json_recipient_list()


    def get_json_recipients(self):

        return self.json_recipients


    def _json_recipient_list(self):

        firstnames, middlenames, lastnames, mobileregions, mobilenumbers, emails = [], [], [], [], [], []

        for recipient in self.recipient_list:
            recipient_dict = json.loads(recipient)
            firstnames.append(recipient_dict['first_name'])

        for recipient in self.recipient_list:
            recipient_dict = json.loads(recipient)
            middlenames.append(recipient_dict['middle_name'])

        for recipient in self.recipient_list:
            recipient_dict = json.loads(recipient)
            lastnames.append(recipient_dict['last_name'])

        for recipient in self.recipient_list:
            recipient_dict = json.loads(recipient)
            mobileregions.append(recipient_dict['mobile_region'])

        for recipient in self.recipient_list:
            recipient_dict = json.loads(recipient)
            mobilenumbers.append(recipient_dict['mobile_number'])

        for recipient in self.recipient_list:
            recipient_dict = json.loads(recipient)
            emails.append(recipient_dict['email'])

        recipients = [{"first_name": f, "middle_name": m, "last_name": l, "mobile_region": r,
                          "mobile_number": n, "email": e} for f, m, l, r, n, e in zip(firstnames, middlenames,
                                lastnames, mobileregions, mobilenumbers, emails)]

        return json.dumps(recipients)



class S3UrlData:

    def __init__(self, username, password, intent_id, file_id):

        self.username = username
        self.password = password
        self.intent_id = intent_id
        self.file_id = file_id


    def get_s3_url_json_data(self):

        data = {}
        data['username'] = self.username
        data['password'] = self.password
        data['intent_id'] = self.intent_id
        data['file_id'] = self.file_id

        return json.dumps(data)



class HistoryData:

    def __init__(self, username, password, timestamp_string, page=0):

        self.username = username
        self.password = password
        self.timestamp_string = timestamp_string
        self.page = page


    def get_history_data(self):

        data = {}
        data['username'] = self.username
        data['password'] = self.password
        data['timestamp'] = self.timestamp_string
        data['page'] = self.page

        return json.dumps(data)
