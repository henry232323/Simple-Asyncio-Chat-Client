# Simple-Asyncio-Chat-Client
A simple asyncio chat server and client made in Python using tkinter GUI or PyQt5 (or STDOUT for command line)
STDOUT / No GUI mode can be a little buggy (i.e if a message is received while typing etc.,)

###Usage:
####Server
 - python server.py --addr [\*\*address] --port [\*\*port]
####Tkinter Client
 - python client.py --user [\*\*username] --addr [\*\*address] --port [\*\*port] --nogui [\*\*bool]
####PyQt5 Client
 - python qtclient.py --user [\*\*username\ --addr [\*\*address] --port [\*\*port]

###Defaults
 - Username defaults to "User" (Unless using Qt, then will ask)
 - Address defaults to 127.0.0.1 (localhost)
 - Port defaults to 50000
 - Nogui defaults to False
