import asyncio
import signal
from nats.aio.client import Client as cli

from .chat_constants import Config


class Publisher:
    def __init__(self):
        self._nt = cli()
        self._loop = asyncio.get_event_loop()

    async def start_publisher(self, name):
        await self._nt.connect(Config.nats_address, loop=self._loop)
        while True:
            wrt = input()
            if wrt == "//stop":
                break
            await self._nt.publish(Config.room_name, (name + ": " + wrt).encode())
            await asyncio.sleep(0.2)
        await self._nt.close()


if __name__ == "__main__":
    inpt = input("Your name: ")
    asyncio.get_event_loop().run_until_complete(Publisher().start_publisher(inpt))