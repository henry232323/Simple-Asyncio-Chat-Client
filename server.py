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
        message = make_msg(msg, "[Server]")
        for connection in self.connections:
            connection.write(message)

    def connection_lost(self, exc):
        if isinstance(exc, ConnectionResetError):
            self.connections.remove(self.transport)
        else:
            print(exc)
        err = "{}:{} disconnected".format(*self.peername)
        message = make_msg(err, "[Server]")
        print(err)
        for connection in self.connections:
            connection.write(message)

    def data_received(self, data):
        message = json.loads(data.decode())
        if message['message'] and message['name']:
            content = "{name}: {message}".format(**message)
            print(content)
            for connection in self.connections:
                connection.write(data)

        else:
            msg = make_msg("Sorry! You sent a message without a name or data, it has not been sent.",
                           "[Server]")
            self.transport.write(json.dumps(msg))

def make_msg(message, author):
        msg = dict()
        msg["message"] = message
        msg["name"] = author
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
