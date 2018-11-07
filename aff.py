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
            "help": self._help,
        }

    def oneWordCmd(self, key):
        if key in self.cmd: # developer command
            ret = self.cmd.get(key)()
        elif key in self.items: # select item
            ret = self._select_by_col(Record.name, key)
        elif key in self.locations: # select location
            ret = self._select_by_col(Record.loc, key)
        else:
            ret = self._usage("你輸入的\"{}\"都沒找到捏".format(key))
        return ret

    def validateWords(self, words):
        ret = None
        location = words[0]
        item = words[1]
        if location in self.cmd or location in self.items:
            ret = self._usage("地點\"{}\"與項目重複囉！可以換個字ㄇ".format(location))
        if item in self.cmd or item in self.locations:
            ret = self._usage("項目\"{}\"與地點重複囉！可以換個字ㄇ".format(item))
        try: int(words[2])
        except Exception:
            ret = self._usage("添加項目的第三欄必須為整數！")
        return ret

    def processText(self, text):
        text = text.lower()
        words = text.split(" ")
        size = len(words)
        if size == 1:
            return self.oneWordCmd(words[0])
        elif size in (3, 4):
            errmsg = self.validateWords(words)
            return errmsg or self.add(words)
        else:
            return self._usage("給太多字啦～")

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

    def _select_by_col(self, col, value, limit=5):
        results = Record.query.with_entities(Record).filter(col==value).order_by(Record.time.desc()).slice(0, limit)
        if col is Record.name:
            return "\n".join(map(lambda r: "[{}] {} ({}/{}) [id:{}]".format(r.time.strftime("%Y-%m-%d %H:%M"), r.loc, r.price, r.unit, r.id), results))
        elif col is Record.loc:
            return "\n".join(map(lambda r: "[{}] {} ({}/{}) [id:{}]".format(r.time.strftime("%Y-%m-%d %H:%M"), r.name, r.price, r.unit, r.id), results))
    
    def _usage(self, msg=None):
        ret = msg + "\n" if msg else ""
        ret += "(可以輸入 help 查看詳細使用說明)"
        return ret

    def _help(self, msg=None):
       #        123456789A123456789B12345678 手機畫面寬度量尺
        ret = "┌－－－－－使用說明－－－－－┐" + "\n"
        ret += "### 添加項目" + "\n"
        ret += "┌－語法－－－－－－－－┐" + "\n"
        ret += "|地點 項目 單價（單位）>" + "\n"
        ret += "└－－－－－－－－－－－┘" + "\n"
        ret += "┌－範例－－－－┐" + "\n"
        ret += "|全聯 奇異果 8 >" + "\n"
        ret += "└－－－－－－－┘" + "\n"
        ret += "┌－或－－－－－－－┐" + "\n"
        ret += "|全聯 奇異果 8 個  >" + "\n"
        ret += "└－－－－－－－－－┘" + "\n"
        ret += "單位預設為：個" + "\n"
        ret += "\n"
        ret += "### 找出特定地點最近五筆" + "\n"
        ret += "┌－語法－┐" + "\n"
        ret += "|地點    >" + "\n"
        ret += "└－－－－┘" + "\n"
        ret += "地點必須為曾經添加過的內容唷！" + "\n"
        ret += "\n"
        ret += "### 找出特定項目最近五筆" + "\n"
        ret += "┌－語法－┐" + "\n"
        ret += "|項目    >" + "\n"
        ret += "└－－－－┘" + "\n"
        ret += "項目必須為曾經添加過的內容唷！" + "\n"
        ret += "\n"
        ret += "### 忘記輸入過那些地點？" + "\n"
        ret += "┌－輸入－－┐" + "\n"
        ret += "|location  >" + "\n"
        ret += "└－－－－－┘" + "\n"
        ret += "\n"
        ret += "### 忘記輸入過那些項目？" + "\n"
        ret += "┌－輸入－－┐" + "\n"
        ret += "|item      >" + "\n"
        ret += "└－－－－－┘" + "\n"
        ret += "└－－－－－－－－－－－－－－┘" + "\n"
       #        123456789A123456789B12345678 手機畫面寬度量尺
        return ret
