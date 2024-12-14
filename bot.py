import asyncio
import requests
import webcolors
from settings import *
from websockets.asyncio.client import connect

async def main():
    def payload(color):
        payload = {
            "model": MODEL,
            "cmd": {
                "value": {
                    "name": "Color",
                    "r": color.red,
                    "g": color.green,
                    "b": color.blue
                },
                "name": "color"
            },
            "device": MACADDRESS
        }
        return payload
    url = "https://developer-api.govee.com/v1/devices/control"
    colors = webcolors.names()

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Govee-API-Key": GOVEEAPIKEY
    }
    async with connect("ws://irc-ws.chat.twitch.tv:80") as websocket:
        await websocket.send(f"PASS oauth:{ACCESSTOKEN}")
        await websocket.send(f"NICK {NICK}")
        await websocket.send(f"JOIN #{CHANNELNAME}")
        while True: 
            response = await websocket.recv() 
            if "PING" in response: 
                await websocket.send("PONG")
                continue
            match = next((color for color in colors if color in response.lower()), False)
            if not match:
                continue
            response = requests.put(url, json=payload(webcolors.name_to_rgb(match)), headers=headers)
            print(f"Changing color to {match}")

asyncio.run(main())
