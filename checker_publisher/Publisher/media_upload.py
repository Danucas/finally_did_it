#!/usr/bin/python3

import os, sys, time
import requests

class GifTweet:

    def __init__(self, filename, api):
        self.__api = api
        self.__image_filename = filename
        self.__image_size = os.path.getsize(filename)
        self.media_id = None
        self.__processing_info = None

    @property
    def media_id(self):
        return self.__media_id

    @media_id.setter
    def media_id(self, value):
        self.__media_id = value

    def upload_init(self, type):
        print('Init upload')
        self.__api.gen_nonce()
        sig_data = {"oauth_nonce": self.__api.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.__api.get_time(),

                    "oauth_consumer_key": self.__api.cons_k,
                    "oauth_token": self.__api.tok_k,
                    "oauth_version": "1.0"
        }
        pars = {"command": "INIT",
                "total_bytes": str(self.__image_size),
                "media_type": type
        }
        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://upload.twitter.com/1.1/media/upload.json'
        sign = self.__api.gen_sig(sig_data, ur, "POST")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.__api.gen_header(sig_data)
        heads = {'Authorization': head}
        ak = requests.post(ur, headers=heads, params=pars)
        print(ak.status_code)
        if ak.status_code > 399:
            print(ak.text)
        self.__media_id = ak.json()["media_id_string"]
        return ak

    def up_chunk(self, content, chunk):
        sig_data, pars, files = content[0], content[1], content[2]
        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://upload.twitter.com/1.1/media/upload.json'
        sign = self.__api.gen_sig(sig_data, ur, "POST")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.__api.gen_header(sig_data)
        heads = {'Authorization': head}
        ak = requests.post(ur, headers=heads, params=pars, files=files)
        print(ak.status_code)
        return ak


    def upload_append(self):
        print('appending to file...')
        self.__api.gen_nonce()
        sig_data = {"oauth_nonce": self.__api.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.__api.get_time(),
                    "oauth_consumer_key": self.__api.cons_k,
                    "oauth_token": self.__api.tok_k,
                    "oauth_version": "1.0"
        }
        pars = {"command": "APPEND",
                "media_id": self.__media_id,
                "segment_index": None
        }
        files = {
            'media': None
        }
        segment = 0
        bytes_sent = 0
        with open(self.__image_filename, "rb") as gif:
            while bytes_sent < self.__image_size:
                chunk = gif.read(4*1024*1024)
                print('chunk: ', len(chunk))
                pars["segment_index"] = str(segment)
                files["media"] = chunk
                res = self.up_chunk((sig_data, pars, files), chunk)
                if res.status_code < 200 or res.status_code > 299:
                    print(res.status_code)
                    print(res.text)
                    sys.exit(0)
                segment += 1
                bytes_sent = gif.tell()
                print("uploaded: ", str(bytes_sent), "of: ", str(self.__image_size))

    def upload_finish(self):
        print('upload finished...')
        self.__api.gen_nonce()
        sig_data = {"oauth_nonce": self.__api.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.__api.get_time(),
                    "oauth_consumer_key": self.__api.cons_k,
                    "oauth_token": self.__api.tok_k,
                    "oauth_version": "1.0"
        }
        pars = {"command": "FINALIZE",
                "media_id": self.__media_id
        }
        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://upload.twitter.com/1.1/media/upload.json'
        sign = self.__api.gen_sig(sig_data, ur, "POST")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.__api.gen_header(sig_data)
        heads = {'Authorization': head}
        ak = requests.post(ur, headers=heads, params=pars)
        print(ak.status_code, ak.json().keys())
        if ak.status_code > 399:
            print(ak.text)
        self.__processing_info = ak.json().get('processing_info', None)
        self.check_status()

    def check_status(self):
        if self.__processing_info is None:
            return
        state = self.__processing_info['state']
        print('processing_status: ', state, '\nmedia_id: ', self.media_id)
        if state == u'failed':
            sys.exit(0)
        if state == u'succeeded':
            return
        cas = self.__processing_info['check_after_secs']
        time.sleep(cas)
        print('STATUS')

        self.__api.gen_nonce()
        sig_data = {"oauth_nonce": self.__api.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.__api.get_time(),
                    "oauth_consumer_key": self.__api.cons_k,
                    "oauth_token": self.__api.tok_k,
                    "oauth_version": "1.0"
        }
        pars = {"command": "STATUS",
                "media_id": self.__media_id
        }
        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://upload.twitter.com/1.1/media/upload.json'
        sign = self.__api.gen_sig(sig_data, ur, "GET")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.__api.gen_header(sig_data)
        heads = {'Authorization': head}
        ak = requests.get(ur, headers=heads, params=pars)
        self.__processing_info = ak.json().get('processing_info', None)
        self.check_status()

    def post(self, phrase):
        self.__api.gen_nonce()
        sig_data = {"oauth_nonce": self.__api.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.__api.get_time(),
                    "oauth_consumer_key": self.__api.cons_k,
                    "oauth_token": self.__api.tok_k,
                    "oauth_version": "1.0"
        }
        pars = {"status": phrase,
                "media_ids": self.__media_id
        }
        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://api.twitter.com/1.1/statuses/update.json'
        sign = self.__api.gen_sig(sig_data, ur, "POST")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.__api.gen_header(sig_data)
        heads = {'Authorization': head}
        ak = requests.post(ur, headers=heads, params=pars)
        print(ak)
        return ak
