#!/usr/bin/python2.7

import sendmail
import random
import email

class Singleton(object):
    self = None
    def __new__(cls, *args, **kwargs):
        if cls.self is None:
            cls.self = object.__new__(cls, *args, **kwargs)
        return cls.self

class InstantFactory(object):
    def __init__(self, cls, src):
        self.cls = cls
        self.src = src
        self.exp = []

    def __getitem__(self, name):
        return self.cls( *self.src[name] )

    def __setitem__(self, name, value):
        if type(value) is self.cls and hasattr(self.cls, "__zip__"):
            self.src[name] = value.__zip__()
        else:
            raise TypeError, "Invalid value for setitem"

    def __delitem__(self, name):
        #del self.src[name]
        self.exp.append(name)

    def __getattr__(self, name):
        return getattr(self.src, name)

    def __len__(self):
        return len(self.src)

    def keys(self):
        return [item for item in self.src.keys() if item not in self.exp]

def clean_names(names):
    ret = {}
    for person in names:
        name = " ".join((person[1], person[3]))
        ret[name] = (name, person[0], person[4], person[5], person[6])
    return ret

class Soul(object):
    def __init__(self, name, gender, zodiac, occupation, bloodtype):
        self.name = name
        self.sex = gender
        self.sign = zodiac
        self.job = occupation
        self.blood = bloodtype

    def __str__(self):
        return "     ".join((self.name, self.sex, self.sign, self.job, self.blood))

class Reaper(Singleton):
    def __init__(self, filename = "raw.csv"):
        with open(filename) as f:
            raw = f.read()
        self.souls = InstantFactory(Soul,\
            clean_names( [item.split(",") for item in raw.split("\n")[1:-1]] ))

    def get_new_soul(self):
        name = random.choice(self.souls.keys())
        soul = self.souls[name]
        del self.souls[name]
        return soul

class Spirifer(object):
    def __init__(self, num = 20, name = "Grim Reaper"):
        self.souls = []
        self.reap = Reaper()
        self.add_souls(num)
        self.name = name        

    def add_souls(self, num = 20):
        for i in xrange(num):
            self.souls.append(self.reap.get_new_soul())

    def update(self):
        if len(self.souls) == 0:
            self.add_souls()
        return self.souls.pop()

class Game(object):
    def __init__(self, num = 5, client = "dummya1473@gmail.com"):
        self.sellers = [Spirifer(11) for i in xrange(num)]
        for person in self.sellers:
            person.name = person.souls.pop().name
        self.client = client

    def new_seller(self):
        seller = random.choice(self.sellers)
        soul = seller.update()
        sendmail.send(self.client, "".join(("I have an offer.\n\n$", str(random.randrange(1, 10) * 100), " for ", soul.name, "'s soul. Details follow.\n\n", str(soul))), "".join((soul.name, "'s soul")), seller.name)

    def update(self):
        for msg in sendmail.recv():
            body = list(msg.walk())[1].get_payload().split("\r\n")[0]
            new = email.message_from_string(msg.as_string().replace(body, "Thank you for your business."))
            new["From"] = msg["To"]
            new["To"] = self.client
            new["Subject"] = "Re: " + msg["Subject"]
            
            sendmail.send(self.client, new.as_string(), raw = True)
            print msg["Subject"].replace("Re: ", ""), "sold."
