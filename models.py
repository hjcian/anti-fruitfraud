from manage import db, app

class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    loc = db.Column(db.String(32), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    unit = db.Column(db.String(16), unique=False, nullable=False)

    def __repr__(self):
        return "<Record: {} {} {} {}>".format(self.time, self.loc, self.price, self.unit)