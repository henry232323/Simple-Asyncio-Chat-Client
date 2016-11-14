import asyncio
import json        
        
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
        content = "{name}: {message}".format(**message)
        print(content)
        for connection in self.connections:
            connection.write(data)
            
connections = []
loop = asyncio.get_event_loop()
coro = loop.create_server(lambda: ChatServerProtocol(connections), "localhost", 50000)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
