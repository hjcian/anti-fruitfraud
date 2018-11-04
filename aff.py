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
            return "{}".format(Record.query.all())
        else:
            return "Action not found ({})".format(" ".join(self.cmd))

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

    def _usage(self):
        return "Show usage"

    def debug(self, actions):
        if len(actions):
            a = actions[0]
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
                unit=actions[3] if len(actions) > 3 else "個"
                )
            self.db.session.add(r)
            self.db.session.commit()
            return "[success][id:{}] add item {} ({}/{}) at {} when {}".format(
                r.id, 
                r.name, 
                r.price, 
                r.unit, 
                r.loc, 
                r.time.strftime("%Y-%m-%d %H:%M"))
        else:
            return self._usage()

    def processText(self, text):
        text = text.lower()
        self.showText(text)
        cmd, *actions = text.split(" ")
        commands = {
            "debug": self.debug,
            "add": self.add,
        }
        ret = commands.get(cmd)(actions)
        return ret

    def _displayRecord(self):
        return "[develop]\n{}".format(Record.query.all())

    def _clear(self):
        self.db.session.query(Record).delete()
        self.db.session.commit()
        return "[develop] clear all records"

    def _test(self):
        return "[develop]\n123456789A123456789B123456789C123456789D123456789E"

    def showText(self, text):
        print("Show: {}".format(text))

