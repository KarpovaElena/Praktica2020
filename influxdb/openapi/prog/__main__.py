from aiohttp import web
import prog.endpoints as ep
from prog.db import Database, DBRequest

Database.set_db('influx', 'prr')
DBRequest.set_mes('msn')

app = web.Application()

app.router.add_get('/start', ep.start_server)
app.router.add_get('/stop', ep.stop_server)
app.router.add_get('/add', ep.add_var)
app.router.add_get('/list_var', ep.list_var)

web.run_app(app, host='0.0.0.0', port=8010)
