import json
import asyncio
import functools
import signal
import websockets

address = "wss://ws-feed.gdax.com"

subscribe = json.dumps({
        "type": "subscribe",
        "channels": [{ "name": "ticker", "product_ids": ["BTC-USD"] }]
    })

unsubscribe = json.dumps({
        "type": "unsubscribe",
        "channels": [{ "name": "ticker", "product_ids": ["BTC-USD"] }]
    })

loop = asyncio.get_event_loop()

def exit(signame):
    print("Got signal {} and will exit ...".format(signame))
    loop.stop()

for signame in ('SIGINT', 'SIGTERM'):
    loop.add_signal_handler(getattr(signal, signame), functools.partial(exit, signame))

async def print_message(jsm):
    print("< #({}) @ {} : {}".format(jsm['sequence'],jsm['time'],jsm['price'])) if 'side' in jsm else None

async def process_message(message):
    jsm = json.loads(message)
    await print_message(jsm)

async def connection():
    async with websockets.connect(address) as websocket:
        await websocket.send(subscribe)
        print("> {}".format(subscribe))
        async for message in websocket:
            await process_message(message)
        await websocket.send(unsubscribe)
        print("> {}".format(unsubscribe))

# clean up not yet working
asyncio.get_event_loop().run_until_complete(connection())

