from aiohttp import web
from prog.publisher import WriterApi, VariablesClass, Variable


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


async def list_var(request):
    return web.json_response({"lst": [{a: VariablesClass.variables[a].value} for a
                              in VariablesClass.variables], "cnt": len(VariablesClass.variables)})
