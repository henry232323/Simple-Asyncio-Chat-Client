import asyncio
import json
import argparse
        
class ChatServerProtocol(asyncio.Protocol):
    def __init__(self, connections):
        self.connections = connections
        self.peername = ""
        
    def connection_made(self, transport):
        self.connections += [transport]
        self.peername = transport.get_extra_info('sockname')
        print('Connection from {}:{}'.format(*self.peername))
        self.transport = transport
        msg = "{}:{} connected".format(*self.peername)
        message = self.make_msg(msg, "[Server]", "servermsg")
        for connection in self.connections:
            connection.write(message)

    def connection_lost(self, exc):
        if isinstance(exc, ConnectionResetError):
            self.connections.remove(self.transport)
        else:
            print(exc)
        err = "{}:{} disconnected".format(*self.peername)
        message = self.make_msg(err, "[Server]", "servermsg")
        print(err)
        for connection in self.connections:
            connection.write(message)

    def data_received(self, data):
        message = json.loads(data.decode())
        if message['author'] and message['content']:
            if message["event"] == "message":
                content = "{author}: {content}".format(**message)
            elif message["event"] == "servermsg":
                content = "{author} {content}".format(**message)
            else:
                content = "{author}: {content}".format(**message)
                
            print(content)
            for connection in self.connections:
                connection.write(data)

        else:
            msg = self.make_msg("Sorry! You sent a message without a name or data, it has not been sent.",
                           "[Server]", "servermsg")
            self.transport.write(json.dumps(msg))

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
    parser = argparse.ArgumentParser(description="Server settings")
    parser.add_argument("--addr", default="127.0.0.1", type=str)
    parser.add_argument("--port", default=50000, type=int)
    args = vars(parser.parse_args())
                
    connections = []
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: ChatServerProtocol(connections), args["addr"], args["port"])
    server = loop.run_until_complete(coro)

    print('Serving on {}:{}'.format(*server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
