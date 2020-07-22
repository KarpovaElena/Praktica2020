from aiohttp import web
import aio_mqtt
import random
import asyncio
from prog.publisher import WriterApi, VariablesClass, Variable


class MQTT:
    addr = 'localhost'


class AnswerPattern:
    @classmethod
    def _get_answer(cls, a_str):
        return {"response": a_str}

    @classmethod
    def get_success_answer(cls):
        return cls._get_answer("OK")

    @classmethod
    def get_error_answer(cls):
        return cls._get_answer("ERROR")


async def start_server(request):
    WriterApi.start_loop()
    return web.json_response(AnswerPattern.get_success_answer())


async def stop_server(request):
    WriterApi.stop_loop()
    return web.json_response(AnswerPattern.get_success_answer())


async def add_var(request):
    name = request.rel_url.query.get("name", None)
    beg_val = request.rel_url.query.get("begin", None)
    try:
        time_sim = 1 / abs(float(request.rel_url.query.get("fr", 1.0)))
    except Exception:
        return web.json_response(AnswerPattern.get_error_answer())

    if name is None or beg_val is None:
        return web.json_response(AnswerPattern.get_error_answer())

    VariablesClass.variables[name] = Variable(beg_val, time_sim)
    return web.json_response(AnswerPattern.get_success_answer())


async def del_var(request):
    name = request.rel_url.query.get("name", None)
    if name is None:
        return web.json_response(AnswerPattern.get_error_answer())
    if VariablesClass.variables.get(name, None) is not None:
        VariablesClass.variables.pop(name)
        return web.json_response(AnswerPattern.get_success_answer())
    return web.json_response(AnswerPattern.get_error_answer())


async def add_mosquitto(request):
    authed = await auth_token(request)
    if not authed:
        return web.json_response(AnswerPattern.get_error_answer())
    name = request.rel_url.query.get("name", None)
    topic = request.rel_url.query.get("topic", None)
    if name is None or topic is None:
        return web.json_response(AnswerPattern.get_error_answer())
    cli = aio_mqtt.Client(loop=asyncio.get_event_loop())
    await cli.connect(MQTT.addr)
    await cli.subscribe((topic+'/'+name, aio_mqtt.QOSLevel.QOS_1))

    async def handle():
        async for message in cli.delivered_messages(topic+'/'+name):
            VariablesClass.variables[name] = Variable(float(message.payload.decode()), 0.3, False)

    asyncio.get_event_loop().create_task(handle())
    return web.json_response(AnswerPattern.get_success_answer())


async def list_var(request):
    return web.json_response({"lst": [{a: VariablesClass.variables[a].value} for a
                              in VariablesClass.variables], "cnt": len(VariablesClass.variables)})
