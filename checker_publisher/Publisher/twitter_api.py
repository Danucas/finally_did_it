#!/usr/bin/python3
"""search api auth module"""
from hashlib import sha1
import hmac, random, codecs, time, requests
from urllib.parse import quote
import base64
import os
import json

class Tapi:

    def __init__(self, cons_k, cons_s, tok_k, tok_s):
        self.__cons_k = cons_k
        self.__cons_s = cons_s
        self.__tok_k = tok_k
        self.__tok_s = tok_s
        # callback = "http://127.0.0.1:8080"
        # callback = bytes([ord(x) for x in callback])
        # callback = quote(callback, safe="")
        # self.__callback = callback

    @property
    def cons_k(self):
        return self.__cons_k

    @property
    def cons_s(self):
        return self.__cons_s

    @property
    def tok_k(self):
        return self.__tok_k

    @property
    def tok_s(self):
        return self.__tok_s

    def gen_sig(self, dic, url="", method=""):
        keys = [st for st in dic.keys()]
        keys = sorted(keys)
        out_s = ""
        for attr in keys:
            key = quote(bytes([ord(x) for x in attr]), safe="")
            out_s += key + "="
            out_s += quote(bytes([ord(x) for x in dic[attr]]), safe="")
            out_s += "&"
        out_s = quote(bytes([ord(x) for x in out_s[:-1]]), safe="")
        url = quote(bytes([ord(x) for x in url]), safe="")
        par_str = "&".join([method, url, out_s])
        par_str = bytes([ord(x) for x in par_str])
        sig_key = quote(bytes([ord(x) for x in self.__cons_s]), safe="") + "&"
        sig_key += quote(bytes([ord(x) for x in self.__tok_s]), safe="")
        sig_key = bytes([ord(x) for x in sig_key])
        hashed = hmac.new(sig_key, par_str, sha1)
        hashed = codecs.encode(hashed.digest(), "base64").rstrip(bytes([10]))
        hashed = quote(hashed, safe="")
        return hashed

    @property
    def nonce(self):
        return self.__nonce

    def gen_nonce(self):
        nonce = lambda length: list(filter(lambda s: chr(s).isalpha(), base64.b64encode(os.urandom(length * 2))))[:length]
        nonce = codecs.encode(bytes(nonce(32)), "base64").rstrip(bytes([10]))
        nonce = ''.join([chr(x) for x in nonce])[:-1]
        self.__nonce = nonce
        return self.__nonce

    def get_time(self):
        self.__time = str(int(time.time()))
        return self.__time

    def gen_header(self, sig_data):
        keys = [st for st in sig_data.keys()]
        keys = sorted(keys)
        header_str = "OAuth "
        for par in keys:
            header_str += par
            header_str += '="'
            header_str += sig_data[par]
            header_str += '", '
        header_str = header_str[:-2]
        return header_str


    def get_user(self, par):
        self.gen_nonce()
        sig_data = {"oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.cons_k,
                    "oauth_token": self.tok_k,
                    "oauth_version": "1.0"
        }
        pars = par
        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://api.twitter.com/1.1/users/lookup.json'
        sign = self.gen_sig(sig_data, ur, "GET")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.gen_header(sig_data)
        heads = {'Authorization': head, 'content-type': 'application/json'}
        ak = requests.get(ur, headers=heads, params=pars)
        print(ak.status_code)
        return ak

    def follow_user(self, id=""):
        self.gen_nonce()
        sig_data = {"oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.cons_k,
                    "oauth_token": self.tok_k,
                    "oauth_version": "1.0"
        }
        pars = {"user_id": id, "follow": "true"}

        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://api.twitter.com/1.1/friendships/create.json'
        sign = self.gen_sig(sig_data, ur, "POST")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.gen_header(sig_data)
        heads = {'Authorization': head, 'content-type': 'application/json'}
        ak = requests.post(ur, headers=heads, params=pars)
        print(ak.status_code)
        return ak

    def get_followers(self, id="", cursor=None):
        self.gen_nonce()
        sig_data = {#"include_entities": "true",
                    "oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.__cons_k,
                    "oauth_token": self.__tok_k,
                    "oauth_version": "1.0"
                    }

        pars = {"user_id": id, "count": "100", "skip_status": "false"}
        if cursor != None:
            pars["cursor"] = cursor

        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://api.twitter.com/1.1/followers/list.json'
        sign = self.gen_sig(sig_data, ur, "GET")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.gen_header(sig_data)
        heads = {'Authorization': head}
        ak = requests.get(ur, headers=heads, params=pars)
        print(ak.status_code)
        return ak


    def search_tweets(self, query=""):
        self.gen_nonce()
        sig_data = {"oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.__cons_k,
                    "oauth_token": self.__tok_k,
                    "oauth_version": "1.0"
                    }

        pars = {"q": query}

        for par in pars.keys():
            sig_data[par] = pars[par]

        ur = 'https://api.twitter.com/1.1/search/tweets.json'
        sign = self.gen_sig(sig_data, ur, "GET")
        sig_data["oauth_signature"] = sign

        for par in pars.keys():
            del sig_data[par]

        head = self.gen_header(sig_data)
        heads = {'Authorization': head}
        ak = requests.get(ur, headers=heads, params=pars)
        print(ak.status_code)
        return ak


    def search_users(self, query=""):
        self.gen_nonce()
        sig_data = {"include_entities": "true",
                    "oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.__cons_k,
                    "oauth_token": self.__tok_k,
                    "oauth_version": "1.0",
                    "q": query,
                    "page": "5"
                    }
        ur = 'https://api.twitter.com/1.1/users/search.json'
        sign = self.gen_sig(sig_data, ur, "GET")
        sig_data["oauth_signature"] = sign
        del sig_data["q"]
        del sig_data["page"]
        del sig_data["include_entities"]
        head = self.gen_header(sig_data)
        heads = {'Authorization': head}
        #print("\n", heads, "\n")
        ur += "?include_entities=true"
        #print("\nurl: ", ur)
        ak = requests.get(ur, headers=heads, params={'q': query, 'page': '5'})
        print(ak.status_code)
        return ak

    def update(self, message=""):
        self.gen_nonce()
        sig_data = {"include_entities": "true",
                    "oauth_nonce": self.nonce,
                    "oauth_signature_method": "HMAC-SHA1",
                    "oauth_timestamp": self.get_time(),
                    "oauth_consumer_key": self.__cons_k,
                    "oauth_token": self.__tok_k,
                    "oauth_version": "1.0",
                    "status": "test"
                    }
        ur = 'https://api.twitter.com/1.1/statuses/update.json'
        sign = self.gen_sig(sig_data, ur, "POST")
        sig_data["oauth_signature"] = sign
        del sig_data["status"]
        head = self.gen_header(sig_data)
        heads = {'Authorization': head}
        print("\n", heads, "\n")
        ur += "?include_entities=true"
        print("\nurl: ", ur)
        ak = requests.post(ur, headers=heads, params={'status': 'test'})
        print(ak.status_code)
        return ak
