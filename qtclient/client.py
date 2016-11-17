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
        self.is_open = True
        
    def connection_lost(self, exc):
        self.is_open = False
        self.loop.stop()

    def data_received(self, data):
        if data:
            message = json.loads(data.decode())
            self.process_message(message)

    def process_message(self, message):
        if message["event"] == "message":
            content = "{author}: {content}".format(**message)
        elif message["event"] == "servermsg":
            content = "{author} {content}".format(**message)
        else:
            content = "{author}: {content}".format(**message)
            
        self.output(content.strip() + '\n')

    def send(self, data): 
        self.transport.write(self.make_msg(data, self.user, "message"))

    def make_msg(self, message, author, *event):
            msg = dict()
            msg["content"] = message
            msg["author"] = author
            if event:
                msg["event"] = event[0]
            else:
                msg["event"] = "message"
            return json.dumps(msg).encode()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client settings")
    parser.add_argument("--user", type=str)
    parser.add_argument("--addr", default="127.0.0.1", type=str)
    parser.add_argument("--port", default=50000, type=int)
    args = vars(parser.parse_args())

    loop = asyncio.get_event_loop()
    userClient = Client(loop, args["user"])
    coro = loop.create_connection(lambda: userClient, args["addr"], args["port"])
    server = loop.run_until_complete(coro)


    loop.run_forever()
    loop.close()


        

        
