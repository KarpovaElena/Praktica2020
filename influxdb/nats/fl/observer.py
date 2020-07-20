import asyncio
import signal
from nats.aio.client import Client as cli

from .chat_constants import Config


class Observer:
    def __init__(self):
        self._nt = cli()
        self._loop = asyncio.get_event_loop()
        self._stop = False
        self._sub = None
        self._create_stop_handler()

    def _create_stop_handler(self):
        this = self

        def handler(a, b):
            this._stop_func()
            print("Good Bye")

        signal.signal(signal.SIGINT, handler)

    async def start_observer(self):
        await self._nt.connect(Config.nats_address, loop=self._loop)

        def sub_func(msg):
            print(msg.data.decode())

        self._sub = await self._nt.subscribe(Config.room_name, cb=sub_func)
        while not self._stop:
            await asyncio.sleep(0.2)
        await self._nt.unsubscribe(self._sub)
        await self._nt.close()

    def _stop_func(self):
        self._stop = True


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(Observer().start_observer())
