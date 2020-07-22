import asyncio
import random
from prog.db import DBRequest, Database


class Variable:
    def __init__(self, val, tm, sm=True):
        self.value = float(val)
        self.time_st = float(tm)
        self.time_cur = float(tm)
        self.sm = sm


class VariablesClass:
    variables = {}

    @classmethod
    def tick(cls, time_last):
        wm = {}
        time_w8 = 0.3
        for a in cls.variables:
            if not cls.variables[a].sm:
                wm[a] = float(cls.variables[a].value)
                continue
            cls.variables[a].time_cur -= time_last
            if cls.variables[a].time_cur <= 0:
                cls.variables[a].time_cur = cls.variables[a].time_st
                cls.variables[a].value += -1 + 2 * random.random()
                wm[a] = float(cls.variables[a].value)
            if time_w8 > cls.variables[a].time_cur:
                time_w8 = cls.variables[a].time_cur
        return wm, time_w8


class WriterApi:
    _write = False
    _loop = None

    @classmethod
    async def _im_loop(cls):
        wt = 0
        while cls._write:
            rm, wt = VariablesClass.tick(wt)
            if rm:
                DBRequest.set_fields(rm)
            await asyncio.sleep(wt)

    @classmethod
    def start_loop(cls):
        if cls._loop is not None:
            return
        cls._write = True
        cls._loop = asyncio.get_event_loop()
        if cls._loop.is_running():
            cls._loop.create_task(cls._im_loop())
        else:
            cls._loop.run_until_complete(cls._im_loop())

    @classmethod
    def stop_loop(cls):
        cls._write = False
        cls._loop = None


if __name__ == "__main__":
    Database.set_db('influx', 'prr')
    DBRequest.set_mes('msn')
    VariablesClass.variables["e"] = Variable(23, 0.2)
    VariablesClass.variables["r"] = Variable(12, 0.4)
    VariablesClass.variables["q"] = Variable(11, 0.1)
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    WriterApi.start_loop()



