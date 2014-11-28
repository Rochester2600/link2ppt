open#!/usr/bin/python
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
        # If we don't have a token pair then just create the request
        if not self.osecret and not self.otoken:
            oauth = OAuth1(self.ckey, self.csecret)
        elif self.osecret and self.otoken:
            oauth = OAuth1(self.ckey, self.csecret, self.otoken, self.osecret)
        else:
            raise(Exception)
        return oauth

    def login(self):
        data = self._xauth() # Get the body of the request
        auth = self._oauth() # get the authorization header
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
            "limit": 50, ## TODO
            "folder_id": folder
        }
        r= self._request(url, data=data, auth=self._oauth())
        logging.debug(r.text)

        return(r.json())

    def handlelinks(self, r):
        ''' take in the json response a reduce it
        down to only the necessary text'''
        links = []
        for b in r["bookmarks"]:
            link = {}
            link["title"] = b["title"]
            link["url"] = b["url"]
            link["starred"] = b["starred"]
            # time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(1347517370))
            link["date"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(b["time"])
            # Get the highlights text if there is any
            highlights = list(
                h["text"] for h in r["highlights"] if h["bookmark_id"] == b["bookmark_id"]
                )
            link["highlights"] = highlights
            logging.debug(link)
            links.append(link)

        return(links)



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
