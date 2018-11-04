from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta

db = SQLAlchemy()

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    loc = db.Column(db.String(32), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    unit = db.Column(db.String(16), unique=False, nullable=False)

    def __repr__(self):
        return "<Record: {} {} {} {}>".format(self.time, self.loc, self.price, self.unit)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    db.init_app(app)
    return app, db

class AntiFruitFruad(object):
    def __init__(self, db):
        self.db = db
        self.db.create_all()

    def showText(self, text):
        print("Show: {}".format(text))

    def processText(self, text):
        self._displayRecord()
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
        ret = "{} done".format(text)
        self._displayRecord()
        return ret

    def _displayRecord(self):
        print(Record.query.all())