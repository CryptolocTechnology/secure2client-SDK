#!/usr/bin/python

from secure2client_data import S3UrlData



class S3Url:

    def __init__(self, tokenIdentityHandler, tokenHandler, apiHandler, intent):

        self.tokenIdentityHandler = tokenIdentityHandler
        self.apiHandler = apiHandler
        self.tokenHandler = tokenHandler

        self.intent_id = intent.intent_id
        self.file_id = intent.file_id


    def get_s3_url_data(self):

        try:
            get_s3_url_data = S3UrlData(self.tokenIdentityHandler.username, self.tokenIdentityHandler.password,
                                    self.intent_id, self.file_id)

            get_s3_url_data_json = get_s3_url_data.get_s3_url_json_data()
            print get_s3_url_data_json
            return get_s3_url_data_json

        except Exception as e:
            print ("Error extracting s3 URL data: %s" % e.message)


    def get_s3_url(self):

        api_request = "get_s3_url"
        request_headers = None
        data = self.get_s3_url_data()

        no_errors, validated_id_token = self.tokenHandler.get_validated_id_token()

        if no_errors:
            no_errors, get_s3_url_response = self.apiHandler.hit_endpoint(api_request, validated_id_token,
                                                            self.tokenIdentityHandler.api_key, request_headers, data)
            print get_s3_url_response
            return get_s3_url_response


    def confirm_s3_upload(self):

        api_request = "s3_upload_confirm"
        request_headers = None
        data = self.get_s3_url_data()

        no_errors, validated_id_token = self.tokenHandler.get_validated_id_token()

        if no_errors:
            no_errors, s3_upload_confirm_response = self.apiHandler.hit_endpoint(api_request, validated_id_token,
                                                            self.tokenIdentityHandler.api_key, request_headers, data)
            print s3_upload_confirm_response
            return s3_upload_confirm_response
