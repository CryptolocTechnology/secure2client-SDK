#!/usr/bin/python

import boto3
from urllib2 import Request, urlopen
import urllib
import jwt
import json
import time
import jose
from jose import jwk  # , jwt
from jose import jwt as josejwt
from jose.utils import base64url_decode



class CognitoTokenHandler:

    def __init__(self, region, user_pool_id, client_id, api_key, username, password):

        # User pool info
        self.region = region
        self.user_pool_id = user_pool_id
        # User pool client id for app with Admin NO SRP Auth enabled
        self.client_id = client_id

        # User login details
        self.username = username
        self.password = password

        self.api_key = api_key

        self.token = None
        self.id_token = None
        self.refresh_token = None

        self.get_cognito_token()


    def get_cognito_token(self):

        if self.token is None:
            try:
                self._request_token()

            except Exception as e:
                return False, ("Error retrieving token: %s", e.message)

        return True, self.token


    def decode_id_token(self):

        if self.id_token:
            try:
                decoded_token = jwt.decode(self.id_token, verify=False)
                return True, decoded_token

            except Exception as e:
                err_msg = ("Error extracting tokens: %s" % e.message)
                return False, err_msg

        else:
            return False, ("No existing id token")


    def get_validated_id_token(self):

        if not self.token:
            if not self._request_token():
                return False, ("Error requesting token")

        if not self.id_token:
            if not self._extract_tokens():
                return False, ("Error extracting tokens")

        if not self._verify_id_token():
            try:
                if not self._re_token():
                    return False, ("Error refreshing token")

            except Exception as e:
                return False, ("Error verifying id token: %s" % e.message)

        return True, self.id_token


    def _request_token(self):

        # Get JWT token for the user
        provider_client = boto3.client('cognito-idp', region_name=self.region)
        auth_data = {'USERNAME': self.username, 'PASSWORD': self.password}

        try:
            self.token = provider_client.initiate_auth(AuthFlow='USER_PASSWORD_AUTH', AuthParameters=auth_data,
                                                       ClientId=self.client_id)
            return True

        except Exception as e:
            print ("Error creating token: %s" % e.message)
            return False


    def _extract_tokens(self):

        try:
            self.id_token = self.token['AuthenticationResult']['IdToken']
            # Get the refresh token for when the 60 min session expires
            self.refresh_token = self.token['AuthenticationResult']['RefreshToken']
            return True

        except Exception as e:
            print ("Error extracting tokens: %s" % e.message)
            return False

    def _verify_id_token(self):

        try:
            keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(self.region,
                                                                                              self.user_pool_id)
            response = urllib.urlopen(keys_url)
            keys = json.loads(response.read())['keys']

            # get the kid from the headers prior to verification
            headers = josejwt.get_unverified_headers(self.id_token)
            kid = headers['kid']
            # search for the kid in the downloaded public keys
            key_index = -1
            for i in range(len(keys)):
                if kid == keys[i]['kid']:
                    key_index = i
                    break
            if key_index == -1:
                print('Public key not found in jwks.json')
                return False
            # construct the public key
            public_key = jwk.construct(keys[key_index])
            # get the last two sections of the token,
            # message and signature (encoded in base64)
            message, encoded_signature = str(self.id_token).rsplit('.', 1)
            # decode the signature
            decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
            # verify the signature
            if not public_key.verify(message.encode("utf8"), decoded_signature):
                print('Signature verification failed')
                return False
            print('Signature successfully verified')
            # since we passed the verification, we can now safely
            # use the unverified claims
            claims = josejwt.get_unverified_claims(self.id_token)
            # additionally we can verify the token expiration
            if time.time() > claims['exp']:
                print('Token is expired')
                return False
            # and the Audience  (use claims['client_id'] if verifying an access token)
            if claims['aud'] != self.client_id:
                print('Token was not issued for this audience')
                return False
            # now we can use the claims
            # print(claims)
            return True

        except Exception as e:
            print ("Error verifying token: %s" % e.message)
            return False


    def _re_token(self):

        if self.refresh_token:
            try:
                provider_client = boto3.client('cognito-idp', region_name=self.region)
                self.token = provider_client.initiate_auth(
                    ClientId=self.client_id,
                    AuthFlow='REFRESH_TOKEN',
                    AuthParameters={
                        'REFRESH_TOKEN': self.refresh_token
                    }
                )

            except Exception as e:
                print ("Error refreshing token: %s" % e.message)
                print ("Attempting to create new token")

                try:
                    self._request_token()

                except Exception as e:
                    print ("Error creating token: %s" % e.message)
                    return False

        else:
            # No existing refresh token
            try:
                self._request_token()

            except Exception as e:
                print ("Error creating token: %s" % e.message)
                return False

        try:
            self._extract_tokens()
            return True

        except Exception as e:
            print ("Error extracting token: %s" % e.message)
            return False
