#!/usr/bin/python
# Title: InstaLink
# Description: Collect links and highlights from Instapaper.
# Usage:
#   import instalink
#   ilink = instalink.instalink()
#   ilink.login()
#   ilink.getlinks(daterange)
import argparse
import requests
import logging
import time
from requests_oauthlib import OAuth1

__BASE__ = "https://www.instapaper.com"
__API_VERSION__ = "1.1"
__ENDPOINT__ = __BASE__ + "/api/" + __API_VERSION__ + "/"

class Instalink:
    def __init__(self, creds):
        self.ckey = creds[0]
        self.csecret = creds[1]
        self.email = creds[2]
        self.password = creds[3]
        self.osecret = None
        self.otoken = None
        logging.basicConfig(level=logging.DEBUG)

    def _xauth(self):
        # try to authenticate with instapaper
        logging.debug("xauth")
        header = {'x_auth_username': self.email, 'x_auth_password': self.password} ##TODO do I need the xauth client type here?
        return header

    def _oauth(self):
        if not self.osecret and not self.otoken:
            oauth = OAuth1(self.ckey, self.csecret)
        elif self.osecret and self.otoken:
            oauth = OAuth1(self.ckey, self.csecret, self.otoken, self.osecret)
        else:
            raise(Exception)
        return oauth

    def login(self):
        data = self._xauth()
        auth = self._oauth()
        r = self._request(
            "https://www.instapaper.com/api/1.1/oauth/access_token",
            data=data,
            auth=auth
            )
        ## TODO add status code check
        resp = str(r.text)
        oauth_tokens = resp.split("&")
        self.osecret = oauth_tokens[0].split("=")[1]
        self.otoken = oauth_tokens[1].split("=")[1]


    def getlinks(self, folder="archive"):
        '''Returns a list of links from the
        from the instapaper archive'''
        url = __ENDPOINT__ + "bookmarks/list"
        data = {
            "limit": 50, ##TODO
            "folder_id": folder
        }
        r= self._request(url, data=data, auth=self._oauth())
        logging.debug(r.text)
        for b in r.json()["bookmarks"]:
            print("TITLE:")
            print(b["title"])
            print("TIME:")
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(b["time"])))
            print("HIGHLIGHTS")
            print(self.get_highlights(b["bookmark_id"]))
        for h in r.json()["highlights"]:
            print("HIGHLIGHTS:")
            print(h)

    def get_highlights(self, bookmark_id):
        url = __ENDPOINT__ + "bookmarks/" + str(bookmark_id) + "/highlights"
        ## I don't know why but this only works by using a GET request
        r = request.get(url, auth=self._oauth())
        logging.debug(r.json())
        return r.json()

    def get_text(self, bookmark_id):
        url = __ENDPOINT__ + "bookmarks/get_text"
        data = {"bookmark_id": bookmark_id}
        r = self._request(url, data=data, auth=self._oauth())
        logging.debug(r.json())


    def _request(self, url, data, auth):
        r = requests.post(url, data=data, auth=auth) ##TODO clean up
        return r

    def getfolders(self):
        folderurl = __BASE__ + "/api/" + __API_VERSION__ + "/folders/list"
        ## TODO

    def gettext(self, bookmark_id):
        '''Return the text from the bookmarks'''
        logging.debug("gettext")


def main():
    parser = argparse.ArgumentParser(
        description='Instapaper link grabber')
    parser.add_argument('-f',
        dest='creds',
        help="File with consumer key, consumer secret, email, and password in that order on separate lines")

    args = parser.parse_args()

    creds = open(args.creds,'r').read().splitlines()

    ipaper = Instalink(creds)
    ipaper.login()
    ipaper.getlinks()

# init main
if __name__ == '__main__':
    main()
