import asyncio, json, argparse
import tkinter as tk
from sys import stdout

class Client(asyncio.Protocol):
    def __init__(self, loop, user, **kwargs):
        self.user = user
        if not hasattr(self, "output"):
            self.output = stdout.write
        self.is_open = False
        self.loop = loop
        self.last_message = ""
        
    def connection_made(self, transport):
        self.sockname = transport.get_extra_info("sockname")
        self.transport = transport
        self.transport.write(self.user.encode())
        self.is_open = True
        
    def connection_lost(self, exc):
        self.is_open = False
        self.loop.stop()

    def data_received(self, data):
        if data:
            message = json.loads(data.decode())
            self.process_message(message)

    def process_message(self, message):
        try:
            if message["event"] == "message":
                content = "{timestamp} | {author}: {content}".format(**message)
            elif message["event"] == "servermsg":
                content = "{timestamp} | {author} {content}".format(**message)
            else:
                content = "{timestamp} | {author}: {content}".format(**message)
            
            self.output(content.strip() + '\n')
        except KeyError:
            print("Malformed message, skipping")

    def send(self, data): 
        self.transport.write(data.encode())


        

        
