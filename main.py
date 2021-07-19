import asyncio
import json
import logging
from utils.driver import AnalogOutput
import websockets
import os
import time
#Env
SERVER_PORT = os.getenv('SERVER_PORT', 6789)
SERVER_URL = os.getenv('SERVER_URL', "localhost")

#Setup logging
logging.basicConfig()

#Body response

CONNECTED_RESPONSE = {
  "status": "ok",
  "response": "Connection established"
}

driver = AnalogOutput(0)
stop = False
async def init_connection(websocket, path):
    try:
        await websocket.send(json.dumps(CONNECTED_RESPONSE))
        async for message in websocket:
            data = json.loads(message)
            if data['option'] == 'getRealtimeInfo':
              global stop
              while not stop:
                response_body = {
                  'value' : driver.getDeviceValue(),
                  'type' : 'realtime_data'

                }
                await websocket.send(json.dumps(response_body))
                print(driver.getDeviceValue())
                time.sleep(1)
            elif data['option'] == 'stopRealtimeInfo':
              stop = True

    except:
      print("Error starting server")

#Start server
start_server = websockets.serve(init_connection, SERVER_URL, SERVER_PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()