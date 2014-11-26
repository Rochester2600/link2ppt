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

    def _xauth(self):
        # try to authenticate with instapaper
        logging.debug("xauth")
        header = {'x_auth_username': self.email, 'x_auth_password': self.password} ##TODO do I need the xauth client type here?
        return header

    def _oauth(self):
        if not self.osecret and self.otoken:
            oauth = OAuth1(self.ckey, self.csecret)
        elif self.osecret and self.otoken:
            oauth = OAuth1(self.ckey, self.csecret, self.otoken, self.osecret)
        else:
            raise(Exception)
        return oauth

    def login(self):
        data = self._xauth()
        auth = self._oauth()
        r = requests.post(
            "https://www.instapaper.com/api/1.1/oauth/access_token",
            data=body,
            auth=auth
            )
        resp = str(r.text)
        oauth_tokens = resp.split("&")
        self.osecret = oauth_tokens[0].split("=")[1]
        self.otoken = oauth_tokens[1].split("=")[1]


    def getlinks(self, folder="archive"):
        '''Returns a list of links from the
        from the instapaper archive'''
        url = __ENDPOINT__ + "bookmarks/list"
        data = {
            "limit": 500,
            "folder_id": folder
        }
        r= _request(url, data=data, auth=self._oauth)
        logging.debug(r.text)


    def _request(self, url, data=None, auth=None):
        r = requests.post(url, data=data, auth=auth) ##TODO clean up
        return r

    def getfolders(self):
        folderurl = __BASE__ + "/api/" + __API_VERSION__ + "/folders/list"

    def _list(self, limit, folder_id, have, highlights):
        logging.debug("_list")

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

    with open(args.creds) as f:
        creds = f.readlines()

    ipaper = Instalink(creds)
    ipaper.login()
    ipaper.getlinks()

# init main
if __name__ == '__main__':
    main()
