from flask import Flask, request, abort
from datetime import datetime, timezone, timedelta
from models import Record


class AntiFruitFruad(object):
    def __init__(self, db):
        self.db = db
        self.db.create_all()

    def showText(self, text):
        print("Show: {}".format(text))

    def processText(self, text):
        self.showText(text)
        self._displayRecord()
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
        self._displayRecord()
        ret = "{} done".format(text)
        return ret

    def _displayRecord(self):
        print(Record.query.all())