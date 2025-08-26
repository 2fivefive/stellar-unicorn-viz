from env import env
import api, display
import uasyncio as asyncio
import time
import math, random
import machine

machine.freq(200000000)

POLL_INTERVAL = 1 # per second
FPS = 8
TRAIL_LENGTH = 5
TRAIL_COLOR = (64,255,0)
DOT_COLOR = (192,255,96)
SPAWN_MULTIPLIER = 50

siteId, deviceId = api.get_details(env['api_key'])

# globals
dots = []

async def spawn_dots():
    global spawn_rate
    global dots
    while True:
        dots.append((random.randrange(16), 0))
        await asyncio.sleep(1/spawn_rate)
    
    
async def main():
    global dots, spawn_rate
    last_spawn = time.ticks_ms()
    last_poll = time.ticks_ms()

    get_bw = asyncio.create_task(api.get_uplink_bw(siteId, deviceId))
    asyncio.create_task(spawn_dots())
    
    while True:
        #update spawn rate
        tx, rx = api.CURRENT_BW            
        rx_percent = max(min(1, rx/37500000),0.01)
        spawn_rate = rx_percent * SPAWN_MULTIPLIER        
        
        # update dot coords and clear any that have reached the bottom
        for i,(x,y) in enumerate(dots):
            dots[i] = x,y+1
        
        dots = [(x,y) for (x,y) in dots if y < 24]
        display.draw(dots)
        #print(rx, rx_percent, spawn_rate)
        await asyncio.sleep(1/FPS)

if __name__ == "__main__":
    asyncio.run(main())