import urllib
import http.client
import os


#Push config
user_key = os.environ.get('USER_KEY')
token = os.environ.get('TOKEN')
title = "IC Tennis"


#Push sending notification
def pushover(title, message, user_key):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "title": title,
                     "token": token,
                     "user": user_key,
                     "message": message,
                     "html": 1,
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()

# message = "Hello there"
#
# pushover(title, message, user_key)
