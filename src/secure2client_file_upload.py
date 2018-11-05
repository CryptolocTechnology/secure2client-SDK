#!/usr/bin/python

import requests
import random



class FileUpload:

    def __init__(self, s3_url):

        self.s3_url = s3_url


    def s3_upload_small(self):

        try:

            in_file = open("<PATH TO FILE>", "rb")
            data = in_file.read()
            in_file.close()

            # file_data = bytes(random.getrandbits(8) for _ in bytes(1024 * 1024 * 6))
            session = requests.Session()
            content = session.put(self.s3_url, data)

        except Exception as e:
            return ("Error uploading file: %s", e.message)

        return content
