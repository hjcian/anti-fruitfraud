from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
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
    db.init_app(app)
    return app

class AntiFruitFruad(object):
    def __init__(self):
        pass

    def showText(self, text):
        print("Show: {}".format(text))