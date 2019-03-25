#!/usr/bin/python

from secure2client_cognito_token import CognitoTokenHandler



class CreateCognitoTokenHandler:

    def __init__(self):

        self.region = "ap-southeast-2"
        self.user_pool_id = "ap-southeast-2_X9Fo2vP8u"
        self.client_id = "4ijnd8rn87co8h54a8p8cotm5c"


        self.password = "<PASSWORD>"
        self.username = "<USERNAME>"
        self.api_key = '<APIKEY>'


    def get_handler(self):

        try:
            cognito_token_handler = CognitoTokenHandler(self.region, self.user_pool_id, self.client_id, self.api_key,
                                                        self.username, self.password)

        except Exception as e:
            err_msg = ("Error setting up cognito token handler with msg: %s" % e.message)
            return False, err_msg

        return True, cognito_token_handler
