from flask import Flask, request, abort
from datetime import datetime, timezone, timedelta
from models import Record

class AntiFruitFruad(object):
    def __init__(self, db):
        self.db = db
        self.db.create_all()
        # self.locations = set()
        # self.items = set()
        self.locations = set(map(lambda r: r.loc, Record.query.with_entities(Record.loc)))
        self.items = set(map(lambda r: r.name, Record.query.with_entities(Record.name)))


    def _usage(self):
        return "Show usage"

    def debug(self, actions):
        if len(actions):
            a = actions[0].strip()
            action = {
                "show": self._displayRecord,
                "clear": self._clear,
                "test": self._test,
            }
            ret = action.get(a, self._usage())()
            return ret
        else:
            return self._usage()

    def add(self, actions):
        if len(actions) >= 3:
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
            return "{} {}({}/{})/{} [id:{}]".format(r.time.strftime("%Y-%m-%d %H:%M"), r.name, r.price, r.unit, r.loc, r.id, )
        else:
            return self._usage()

    def show(self, actions):
        if len(actions):
            a = actions[0].strip()
            action = {
                "name": self._select_name,
            }
            ret = action.get(a, self._usage())()
            return ret
        else:
            return self._usage()

    def processText(self, text):
        # self._init()
        text = text.lower()
        self.showText(text)
        key, *actions = text.split(" ")
        key = key.strip()
        if key in self.items:
            # directly search item
            ret = self._select_by_name(key)
            return ret
        else:
            commands = {
                "debug": self.debug,
                "add": self.add,
                "show": self.show,
            }
            ret = commands.get(key)(actions)
            return ret

    def _displayRecord(self):
        return "[develop]\n{}".format(Record.query.all())

    def _clear(self):
        self.db.session.query(Record).delete()
        self.db.session.commit()
        return "[develop] clear all records"

    def _test(self):
        return "[develop]\n123456789A123456789B123456789C123456789D123456789E"

    def _select_name(self):
        results = Record.query.with_entities(Record.name)
        results = set(map(lambda r: r.name, results))
        return "\n".join(results)

    def _select_by_name(self, name):
        results = Record.query(Record).filter(Record.name==name)
        for i in results:
            print(i)
        return "\n".join(map(lambda r: "{} {} ({}/{})".format(r.loc, r.name, r.price, r.unit), results))

    def showText(self, text):
        print("Received: {}".format(text))

    def _init(self):
        if not self.locations:
            self.locations = set(map(lambda r: r.loc, Record.query.with_entities(Record.loc)))
        if not self.items:
            self.items = set(map(lambda r: r.name, Record.query.with_entities(Record.name)))

