#!/usr/bin/python

from urllib2 import Request, urlopen
import json



'''
Hitting published endpoints
Strings are interpreted inside the class for different API requests
Need to pass in id_token for each request

api_request = "create_trustshare_intent"
api_request = "get_s3_url"
api_request = "s3_upload_confirm"

api_request = "retrieve_trustshare_history"
api_request = "retrieve_file_history"
api_request = "retrieve_alias_history"
api_request = "retrieve_intent_history"
api_request = "retrieve_recipient_action_history"

'''

class EndpointHandler:

    baseURL = "https://api.au.secure2client.com/v1/"


    def hit_endpoint(self, api_request, token, api_key, headers=None, data=None):

        endpoint = self.baseURL + api_request

        # Make Authorized API Gateway request
        req = Request(endpoint)
        req.add_header('Content-Type', 'application/json')

        api_key_header = 'x-api-key'
        req.add_header(api_key_header, api_key)

        # Set the authorization header with JWT
        req.add_header('Authorization', token)

        if headers:
            unpacked_headers = json.loads(headers)
            for key, value in unpacked_headers.items():
                req.add_header(key, value)

        try:
            print endpoint
            contents = urlopen(req, data)
            print contents.code
            content = contents.read()
            return True, content

        except Exception as e:
            return False, ("Error hitting endpoint: %s", e.message)
