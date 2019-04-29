import asyncio
from block_utils import BlockUtils
from queue import *
import concurrent.futures
import sys
from threading import Thread

# will run event loop forever, put in own thread
class InboxServer(object):
    MAXLEN = 1000

    # inbox: python queue
    def __init__(self, inbox, ip, port):
        self.inbox = inbox
        self.ip = ip
        self.port = port
        print("made it")

    async def listenForBlocks(self, reader, writer):
        data = await reader.read(InboxServer.MAXLEN)
        block = BlockUtils.jsonToBlock(data.decode())
        print(block)
        self.inbox.put(block)
        writer.close()

    def startServer(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print("setting up server")
        coro = asyncio.start_server(self.listenForBlocks, self.ip, self.port)
        server = loop.run_until_complete(coro)
        print("running server")
        sys.stdout.flush()
        loop.run_forever()



class TestServer(object):
    async def sendBlock(ip, port, loop, height):
        block = BlockUtils.generateBlock("me", height)
        reader, writer = await asyncio.open_connection(ip, port, loop = loop)
        writer.write(BlockUtils.blockToJson(block).encode())
        print("sent block")
        writer.close()

    def test(ip, port, height):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(TestServer.sendBlock(ip, port, loop, height))


server = InboxServer(Queue(), "127.0.0.1", 8888)
t = Thread(target = server.startServer)
t.start()

