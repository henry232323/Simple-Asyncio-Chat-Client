import asyncio
import json
import argparse
from datetime import datetime
        
class ChatServerProtocol(asyncio.Protocol):
    def __init__(self, connections, users):
        self.connections = connections
        self.users = users
        self.peername = ""
        self.user = None
        
    def connection_made(self, transport):
        self.connections += [transport]
        self.peername = transport.get_extra_info('sockname')
        self.transport = transport

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
        if data:
            if not self.user:
                user = data.decode()
                if not user.isalpha():
                    self.transport.write(self.make_msg("Your name must be alphanumeric!", "[Server]", "servermsg"))
                    self.transport.close()
                else:
                    self.user = data.decode()
                    print('{} connected ({}:{})'.format(self.user, *self.peername))
                    msg = '{} connected ({}:{})'.format(self.user, *self.peername)
                    message = self.make_msg(msg, "[Server]", "servermsg")
                    
                    for connection in self.connections:
                        connection.write(message)
            else:
                message = data.decode()
                print("{}: {}".format(self.user, message))
                msg = self.make_msg(message, self.user)
                for connection in self.connections:
                    connection.write(msg)

        else:
            msg = self.make_msg("Sorry! You sent a message without a name or data, it has not been sent.",
                           "[Server]", "servermsg")
            self.transport.write(msg)

    def make_msg(self, message, author, *event):
            msg = dict()
            msg["content"] = message
            msg["author"] = author
            time = datetime.utcnow()
            msg["timestamp"] = "{hour}:{minute}:{sec}".format(hour=str(time.hour).zfill(2),
                                                              minute=str(time.minute).zfill(2),
                                                              sec=str(time.second).zfill(2))
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
    users = dict()
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: ChatServerProtocol(connections, users), args["addr"], args["port"])
    server = loop.run_until_complete(coro)

    print('Serving on {}:{}'.format(*server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
