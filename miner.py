import asyncio
import concurrent.futures
from collections import namedtuple
from block_utils import BlockUtils
import datetime
from queue import *


class Miner(object):
    maxLen = 10000
    def __init__(self, ip, port, name, bootstrap, difficulty):
        self.name = name
        self.port = port
        self.peers = bootstrap
        self.difficulty = difficulty
        self.chain = BlockUtils.Chain(BlockUtils.genisisBlock(), [])
        self.outbox = Queue()
        self.inbox = Queue()
        self.inboxServer = InboxServer(self.inbox, ip, port)
        self.loop = asyncio.get_event_loop()

    def mine(self):
        self.listen()
        while(True):
            pass
        #self.mineLoop()
    
    def mineLoop(self):
        while(true):
            # simulate mining by rolling dice till 0
            if (random.randint(0, difficulty) == 0):
                self.chain = BlockUtils.mineNewBlock(self.chain, self.name)
                self.broadcastNewBlock()
                self.checkForNewBlocks()


    # gets all newBlocks that have been broadcasted, adds them to the chain.
    # updates the top if any of them are taller than previous top
    def checkForNewBlocks():
        blocks = list()
        while(not self.inbox.empty()):
            blocks.append(self.inbox.get())
        self.chain = BlockUtils.addNewBlocks(self.chain, blocks)
    

    # hmmm, TODO currenlty we only send top block, so if you have secondaries they don't have, they won't update. Does that matter??
    def broadcastNewBlock(self):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            self.loop.run_in_executor(pool,
                                      self.broadcast(self.chain.top, self.loop, self.peers))

    # needs a wrapper to work right
    def broadcast(self, block, peers):
        def client():
            loop = asyncio.get_running_loop()
            for peer in peers:
                reader, writer = asyncio.open_connection(peer.ip, peer.port, loop=loop)
                write.write(BlockUtils.blockTojson(block).encode())
                #response = await reader.read(100)
                print("no")
                writer.close()
        return client

    def listen(self):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            self.loop.run_in_executor(pool, self.inboxServer.startServer)


# will run event loop forever, put in own thread
class InboxServer(object):

    # inbox: python queue
    def __init__(self, inbox, ip, port):
        self.inbox = inbox
        self.ip = ip
        self.port = port
        print("made it")

    async def listenForBlocks(self, reader, writer):
        data = await reader.read(Miner.maxLen)
        block = BlockUtils.jsonToBlock(data.decode())
        self.inbox.put(block)
        writer.close()

    def startServer(self):
        loop = asyncio.get_event_loop()
        print("setting up server")
        coro = asyncio.start_server(self.listenForBlocks, self.ip, self.port)
        server = loop.run_until_complete(coro)
        print("running server")
        loop.run_forever()
        
            
        
        
m = Miner("127.0.0.1", 8888, "Jacob", [], 10000)
m.mine()
