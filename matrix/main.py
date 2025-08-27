from env import env
import api, display
import uasyncio as asyncio
import time
import math, random
import machine

machine.freq(200000000)

POLL_INTERVAL = 1 # per second
FPS = 4.5
SPAWN_MULTIPLIER = 50

siteId, deviceId = api.get_details(env['api_key'])

dots = []

async def spawn_dots():
    global spawn_rate
    global dots
    while True:
        dots.append((random.randrange(16), 0))
        await asyncio.sleep(1/spawn_rate)


async def update_dots():
    global dots
    global spawn_rate
    while True:
        tx, rx = api.CURRENT_BW            
        rx_percent = max(min(1, rx/37500000),0.01)
        spawn_rate = rx_percent * SPAWN_MULTIPLIER        
        
        # update dot coords and clear any that have reached the bottom
        for i,(x,y) in enumerate(dots):
            dots[i] = x,y+1

        dots = [(x,y) for (x,y) in dots if y < 24]
        display.draw(dots)
        await asyncio.sleep(1/FPS)
    
async def main():
    asyncio.create_task(api.get_uplink_bw(siteId, deviceId))
    asyncio.create_task(update_dots())
    await asyncio.create_task(spawn_dots())
    
if __name__ == "__main__":
    asyncio.run(main())
