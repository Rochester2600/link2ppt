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
from requests_oauthlib import OAuth1

__BASE__ = "https://www.instapaper.com"
__API_VERSION__ = "1.1"

class Instalink:
    def __init__(self, creds):
        self.ckey = creds[0]
        self.csecret = creds[1]
        self.email = creds[2]
        self.password = creds[3]

    def _xauth(self):
        # try to authenticate with instapaper
        print("xauth")
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
        data = _xauth()
        auth = _oauth()
        r = requests.post(
            "https://www.instapaper.com/api/1.1/oauth/access_token",
            data=body,
            auth=auth
            )
        resp = str(r.text)
        oauth_tokens = resp.split("&")
        self.osecret = oauth_tokens[0].split("=")[1]
        self.otoken = oauth_tokens[1].split("=")[1]


    def getlinks(self, folder=None):
        '''Returns a list of links from the
        instagram account. Folder is optional'''
        # requests.post(__BASE__ + "/" + __API_VERSION__ + )
        print("getlinks")
        url = ""
        data = {
            "limit": 500,
            "folder_id": "archive"
        }
        _request(url, data=data, auth=_oauth)

    def _request(self, url, data=None, auth=None):
        requests.post(url, data=data, auth=auth) ##TODO clean up

    def getfolders(self):
        folderurl = __BASE__ + "/api/" + __API_VERSION__ + "/folders/list"

    def _list(self, limit, folder_id, have, highlights):
        print("_list")

    def gettext(self, bookmark_id):
        '''Return the text from the bookmarks'''
        print("gettext")





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

# init main
if __name__ == '__main__':
    main()
