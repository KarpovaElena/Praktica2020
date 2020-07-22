from aiohttp import web
import prog.endpoints as ep
from prog.db import Database, DBRequest

Database.set_db('influx', 'prr')
DBRequest.set_mes('msn')
ep.MQTT.addr = 'mosq'
ep.JWT.secr = "qweijslfniEfnsnefsdfpsefqaweqweqrfzdf"

app = web.Application()

app.router.add_get('/start', ep.start_server)
app.router.add_get('/stop', ep.stop_server)
app.router.add_get('/add', ep.add_var)
app.router.add_get('/list_var', ep.list_var)
app.router.add_get('/mq', ep.add_mosquitto)
app.router.add_post('/auth', ep.auth)

web.run_app(app, host='0.0.0.0', port=8010)
