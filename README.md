# Simple-Asyncio-Chat-Client
A simple Asyncio chat / relay server and client (Async Protocol / Callback) using a STDOUT / tKinter UI through Async create_connection and running the input/GUI in an executor, or using the Quamash PyQt5 loop and running the create_connection as a coroutine.
STDOUT / No GUI mode can be a little buggy (i.e if a message is received while typing etc.,)

##Usage:

 - ###Server
  - python server.py --addr [\*\*address] --port [\*\*port]
 
 - ###Tkinter Client
  - python client.py --user [\*\*username] --addr [\*\*address] --port [\*\*port] --nogui [\*\*bool]
 
 - ###PyQt5 Client
  - python qtclient.py --user [\*\*username] --addr [\*\*address] --port [\*\*port]

##Defaults
 - Username defaults to "User" (Unless using Qt, then will ask)
 - Address defaults to 127.0.0.1 (localhost)
 - Port defaults to 50000
 - Nogui defaults to False
