from flask import Flask, request, abort
from datetime import datetime, timezone, timedelta
from models import Record

class AntiFruitFruad(object):
    def __init__(self, db):
        self.db = db
        self.db.create_all()
        self.locations = set(map(lambda r: r.loc, Record.query.with_entities(Record.loc)))
        self.items = set(map(lambda r: r.name, Record.query.with_entities(Record.name)))
        self.cmd = {
            "show": self._displayRecord,
            "clear": self._clear,
            "item": lambda: "\n".join(self.items),
            "location": lambda: "\n".join(self.locations),
            "test": self._test,
        }

    def processText(self, text):
        text = text.lower()
        self.showText(text)
        words = text.split(" ")
        size = len(words)
        if size == 1:
            ret = "Not found {} in developer command and item list".format(words[0])
            if words[0] in self.cmd: # developer command
                ret = self.cmd.get(words[0], self._usage)()
            elif words[0] in self.items: # find item
                ret = self._select_by_name(words[0])
            return ret
        elif size in (3, 4):
            return self.add(words)
        else:
            return self._usage()

    def _usage(self):
        return "Show usage"

    def add(self, actions):
        r = Record(
            time=datetime.utcnow() + timedelta(hours=8),
            loc=actions[0],
            name=actions[1], 
            price=actions[2], 
            unit=actions[3] if len(actions) > 3 else "{}".format("個")
            )
        self.db.session.add(r)
        self.db.session.commit()
        self.locations.add(actions[0])
        self.items.add(actions[1])
        return "[OK] {} {}({}/{})/{} [id:{}]".format(r.time.strftime("%Y-%m-%d %H:%M"), r.name, r.price, r.unit, r.loc, r.id, )

    def _displayRecord(self):
        return "[develop]\n{}".format(Record.query.all())

    def _clear(self):
        self.db.session.query(Record).delete()
        self.db.session.commit()
        return "[develop] clear all records"

    def _test(self):
        return "[develop]\n123456789A123456789B123456789C123456789D123456789E"

    def _select_by_name(self, name):
        results = Record.query.with_entities(Record).filter(Record.name==name).order_by(Record.time.desc()).slice(0, 5)
        return "\n".join(map(lambda r: "[{}] {} ({}/{}) [id:{}]".format(r.time.strftime("%Y-%m-%d %H:%M"), r.loc, r.price, r.unit, r.id), results))

    def showText(self, text):
        print("Received: {}".format(text))
