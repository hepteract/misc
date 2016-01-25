# Legacy lib, don't use

import json
import requests

HEADERS = {"Content-Type" : "application/json", "Access-Token" : "NKuQXPLxhOBBeAkgLk1S81RWzCSEhad9"}
PUSH_URL = "https://api.pushbullet.com/v2/pushes"

class PushManager(object):
    def send_push(self, body, email = "elijah@shivergaming.com"):
        return requests.post(PUSH_URL, self.create_payload(body, email), headers = HEADERS)

    def create_payload(self, body, email):
        payload = {"email" : email, "type" : "note", "title" : "JARVIS", "body" : body}
        return json.dumps(payload)

jarvis = PushManager()
