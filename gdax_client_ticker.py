import json
import asyncio
import functools
import signal
import websockets

# address of websockets feed for GDAX
address = "wss://ws-feed.gdax.com"

# JSON text to subscribe to ticker of BTC-USD
sub = json.dumps({
        "type": "subscribe",
        "channels": [{ "name": "ticker", "product_ids": ["BTC-USD"] }]
    })

# JSON text to subscribe from ticker of BTC-USD
unsub = json.dumps({
        "type": "unsubscribe",
        "channels": [{ "name": "ticker", "product_ids": ["BTC-USD"] }]
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
    if jmsg['type'] == 'ticker' and all (key in jmsg for key in ('price','side')):
        print(
            "#({},{}) @ {} : Price = {}, Volume = {}, Side = {:4}, Bid = {}, Ask = {}".format(
                jmsg['sequence'], jmsg['trade_id'], jmsg['time'], jmsg['price'],
                jmsg['last_size'], jmsg['side'], jmsg['best_bid'], jmsg['best_ask']))

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
