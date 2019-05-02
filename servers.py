import asyncio
from block_utils import BlockUtils
from queue import *
import concurrent.futures
import sys
from threading import Thread

# will run event loop forever, put in own thread
class InboxServer(object):
    MAXLEN = 1000000

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
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        print("setting up server")
        coro = asyncio.start_server(self.listenForBlocks, self.ip, self.port)
        self.server = self.loop.run_until_complete(coro)
        print("running server")
        sys.stdout.flush()
        self.loop.run_forever()

    def shutDown(self):
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())
        self.loop.close()



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

class BootstrapServer(object):
    def boot(peers, loop):
        for peer in peers:
            reader, writer = await asyncio.open_connection(peer.ip, peer.port, loop = loop)
            s = "START"
            writer.write(s.encode())
            writer.close()
        print("all peers bootstrapped!")

    def go(peers):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(BootstrapServer.boot(peers, loop)

def main():
    server = InboxServer(Queue(), "127.0.0.1", 8888)
    t = Thread(target = server.startServer)
    t.start()

