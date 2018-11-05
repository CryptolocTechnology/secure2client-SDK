#!/usr/bin/python

from secure2client_data import HistoryData



class History:

    def __init__(self, tokenIdentityHandler, tokenHandler, apiHandler):

        self.history_data = None

        self.tokenIdentityHandler = tokenIdentityHandler
        self.tokenHandler = tokenHandler
        self.apiHandler = apiHandler


    def output_all_history(self, fromDate):

        try:
            history_caller = HistoryData(self.tokenIdentityHandler.username, self.tokenIdentityHandler.password,
                                         fromDate)

            history_data = history_caller.get_history_data()
            self.history_data = history_data
            print history_data

        except Exception as e:
            print ("Error extracting history data: %s" % e.message)

        history_list = []
        history_list.append("retrieve_trustshare_history")
        history_list.append("retrieve_file_history")
        history_list.append("retrieve_alias_history")
        history_list.append("retrieve_intent_history")
        history_list.append("retrieve_recipient_action_history")

        request_headers = None
        data = self.history_data


        no_errors, validated_id_token = self.tokenHandler.get_validated_id_token()

        if no_errors:

            for api_request in history_list:
                no_errors, history_data_response = self.apiHandler.hit_endpoint(api_request, validated_id_token,
                                                    self.tokenIdentityHandler.api_key, request_headers,
                                                                            data)
                print history_data_response
