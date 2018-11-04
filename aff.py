from flask import Flask, request, abort
from datetime import datetime, timezone, timedelta
from models import Record


class BaseMode(object):
    def __init__(self, command):
        self.cmd = command

    def reply(self):
        return "Command not found ({})".format(self.cmd)

class DebugMode(BaseMode):
    def reply(self):
        s = self.cmd[0]
        if s == "show":
            return Record.query.all()

class AddMode(BaseMode):
    def reply(self):
        pass

def processText(text):
    key, *rest = text.split(" ")
    return {
        "debug": DebugMode(rest)
    }.get(key, BaseMode(text)).reply()

class AntiFruitFruad(object):
    def __init__(self, db):
        self.db = db
        self.db.create_all()

    def showText(self, text):
        print("Show: {}".format(text))

    def processText(self, text):
        self.showText(text)
        dt = datetime.utcnow()
        tzutc_8 = timezone(timedelta(hours=8))
        local_dt = dt.astimezone(tzutc_8)
        r = Record(
            time=local_dt,
            loc=text, 
            price=123, 
            unit="斤")
        self.db.session.add(r)
        self.db.session.commit()
        # ret = "{} done".format(text)
        ret = processText(text)
        return ret

    def _displayRecord(self):
        print(Record.query.all())