import asyncio
import json
import argparse
        
class ChatServerProtocol(asyncio.Protocol):
    def __init__(self, connections):
        self.connections = connections
    
    def connection_made(self, transport):
        self.connections += [transport]
        peername = transport.get_extra_info('sockname')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def connection_lost(self, exc):
        print(exc)
        self.connections.remove(self.transport)
        

    def data_received(self, data):
        message = json.loads(data.decode())
        if message['message'] and message['name']:
            content = "{name}: {message}".format(**message)
            print(content)
            for connection in self.connections:
                connection.write(data)

        else:
            msg = dict()
            msg['message'] = "Sorry! You sent a message without a name or data, it has not been sent."
            msg['name'] = "[Server]"
            self.transport.write(json.dumps(msg).encode())

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
