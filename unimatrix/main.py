from env import env
import api, display
import asyncio
import time
import math, random
import machine

machine.freq(200000000)

POLL_INTERVAL = 1 # per second
FPS = 4
TRAIL_LENGTH = 5
TRAIL_COLOR = (64,255,0)
DOT_COLOR = (192,255,96)

siteId, deviceId = api.get_details(env['api_key'])

async def main():
    last_spawn = time.ticks_ms()
    last_poll = time.ticks_ms()
    dots = []
    spawn_rate = 30 # dots per second
    get_bw = asyncio.create_task(api.get_uplink_bw(siteId, deviceId))
    
    while True:

        now = time.ticks_ms()
        
        #update spawn rate
        tx, rx = api.CURRENT_BW            
        rx_percent = max(min(100, rx//375000),1)            
        spawn_rate = rx_percent

        #spawn dots
        while time.ticks_diff(now, last_spawn) > 1/spawn_rate:
            dots.append((random.randrange(16),0))
            last_spawn = time.ticks_add(last_spawn, 1000//spawn_rate)
            
        
        # update dot coords and clear any that have reached the bottom
        for i,(x,y) in enumerate(dots):
            dots[i] = x,y+1
        
        dots = [(x,y) for (x,y) in dots if y < 24]
        display.draw(dots)
        print(f"{spawn_rate} dots per second")
        await asyncio.sleep(1/FPS)

if __name__ == "__main__":
    asyncio.run(main())