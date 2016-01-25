import json
import requests

PUSH_URL = "https://api.pushbullet.com/v2/pushes"

class PushbulletError(Exception): pass

class UserHandler(object):
    def __init__(self, email, token, default_title = None, last_check = 0):
        self.email = email
        self.title = default_title
        self.header = {"Content-Type" : "application/json", "Access-Token" : token}

        
    def send_push(self, body, title = None):
        if title:
            return requests.post(PUSH_URL, self.create_payload(body, title), headers = self.header)
        elif self.title:
            return requests.post(PUSH_URL, self.create_payload(body, self.title), headers = self.header)
        else:
            raise PushbulletError, "UserHandler cannot send push without a title"

    def create_payload(self, body, title):
        payload = {"email" : self.email, "type" : "note", "title" : title, "body" : body}
        return json.dumps(payload)

    def fetch_messages(self, limit = None, active = True):
        raise PushbulletError, "fetch_messages not yet implemented"
