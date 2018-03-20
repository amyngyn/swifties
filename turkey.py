import json
import random
import re
import requests
import time


DOMAIN = 'http://127.0.0.1:5000'
TOKEN_REGEX = re.compile("var id = \"([^']*)\"")


def send_request(method, endpoint, headers=None, data=None):
    url = "%s%s" % (DOMAIN, endpoint)
    print ("--- Sending %s to %s" % (method.upper(), url))
    watch_begin = requests.request(method, url, headers=headers, data=data)
    return watch_begin


if __name__ == "__main__":
    for i in xrange(100):
        print("-------------------------------")
        # 1. Get a unique ID from the Swifties server
        js_response = send_request("GET", "/static/counters.js", None, None)
        token = TOKEN_REGEX.search(js_response.text).group(1)
        print("--- Got ID: %s" % token)

        # 2. Send a request to the start endpoint
        headers = {'Content-Type': 'application/json'}
        token_data = '{"id": "%s"}' % token
        send_request("POST", "/start", headers, token_data)

        # 3. Send a request to the count endpoint
        watch_response = send_request("POST", "/count", headers, token_data)
        watch_json = json.loads(watch_response.text)
        if watch_json["success"]:
            print "Success!"
        else:
            print "Failed??"
