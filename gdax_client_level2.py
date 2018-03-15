import json
import asyncio
import functools
import signal
import websockets

# address of websockets feed for GDAX
address = "wss://ws-feed.gdax.com"

sub = json.dumps({
        "type": "subscribe",
        "channels": [{ "name": "level2", "product_ids": ["BTC-USD"] }]
    })

unsub = json.dumps({
        "type": "unsubscribe",
        "channels": [{ "name": "level2", "product_ids": ["BTC-USD"] }]
    })

# subscribe to data feed
async def subscribe(ws):
    await ws.send(sub)

# unsubscribe from data feed (may not be needed when stream is terminated anyway)
async def unsubscribe():
    await websocket.send(unsub)

# process JSON data and print
async def process_message(msg):
    jmsg = json.loads(msg)
    await print_message(jmsg)

async def print_message(jmsg):
    if jmsg['type'] == 'snapshot':
        print("Got snapshot with {} bids and {} asks".format(len(jmsg['bids']),len(jmsg['asks'])))
    elif jmsg['type'] == 'l2update':
        print("Got update at time {}".format(jmsg['time']))
    else:
        print("Got another message")

async def get_stream():
    try:
        async with websockets.connect(address) as ws:
            await subscribe(ws)
            async for message in ws:
                await process_message(message)
    except:
        pass

loop = asyncio.get_event_loop()

def exit():
    for task in asyncio.Task.all_tasks():
        task.cancel()

loop.add_signal_handler(signal.SIGTERM, exit)
loop.add_signal_handler(signal.SIGINT, exit)
loop.run_until_complete(get_stream())
