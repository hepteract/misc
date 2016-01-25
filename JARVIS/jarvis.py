import pushbullet

HEADERS = {"Content-Type" : "application/json", "Access-Token" : "NKuQXPLxhOBBeAkgLk1S81RWzCSEhad9"}

class JARVIS(pushbullet.UserHandler):
    def __init__(self, email = "elijah@shivergaming.com"):
        self.email = email
        self.title = "JARVIS"
        self.header = HEADERS
