from env import env
import network
import machine
import requests
import ujson
import uasyncio as asyncio
import aiohttp


POLL_INTERVAL_SECONDS = 1
CURRENT_BW = (0,0)

#network stuff
wlan = network.WLAN()
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(env['ssid'], env['wifi_pw'])
    while not wlan.isconnected():
        machine.idle()
print('network config:', wlan.ipconfig('addr4'))

def get_details(key):
    global headers
    url="https://192.168.1.1/proxy/network/integration/v1/sites"
    headers = {'X-API-KEY': env['api_key'], 'Accept':'application/json'}
    r = requests.get(url, headers=headers)
    site = ujson.loads(r.text)['data']
    siteId = site[0]['id']

    url=f"https://192.168.1.1/proxy/network/integration/v1/sites/{siteId}/devices"
    r = requests.get(url, headers=headers)
    devices_raw =  ujson.loads(r.text)['data']
    devices = {device['name']:device for device in devices_raw}
    deviceId= devices['UDM Pro']['id']
    return siteId, deviceId

async def get_uplink_bw(siteId, deviceId):
    global CURRENT_BW
    global headers
    url=f'https://192.168.1.1/proxy/network/integration/v1/sites/{siteId}/devices/{deviceId}/statistics/latest'
    
    async with aiohttp.ClientSession() as session:
        while True:
            async with session.get(url, headers=headers) as response:
                stats = await response.json()
                tx = stats['uplink']['txRateBps']
                rx = stats['uplink']['rxRateBps']
                CURRENT_BW = tx,rx
                print(f"tx: {tx}   rx:{rx}")
                await asyncio.sleep(POLL_INTERVAL_SECONDS)
                

