import asyncio
from collections import namedtuple
import datetime

async def handle_echo(reader, writer):
    MAXBYTES = 100
    data = await reader.read(MAXBYTES)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print("Send: %r" % message)
    writer.write(data)
    await writer.drain()

    print("Close the client socket")
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()


class Miner(object):
    def __init__(self, port, name, bootstrap, difficulty):
        self.name = name
        self.port = port
        self.peers = bootstrap
        self.difficulty = difficulty
        self.chain = BlockUtils.Chain(BlockUtils.genisisBlock(), [])
    
    def mineLoop(self):
        while(true):
            # simulate mining by rolling dice till 0
            if (random.randint(0, difficulty) == 0):
                self.chain = BlockUtils.mineNewBlock(self.chain, self.name, datetime.datetime.now())
                self.broadcastNewBlock()
            self.checkForNewBlocks()


    # gets all newBlocks that have been broadcasted, adds them to the chain.
    # updates the top if any of them are taller than previous top
    def checkForNewBlocks():
        blocks = GET FROM QUEUE
        self.chain = BlockUtils.addNewBlocks(self.chain, blocks)
    

    # hmmm, TODO currenlty we only send top block, so if you have secondaries they don't have, they won't update. Does that matter??
    def broadcastNewBlock(self):
        self.loop.run_until_complete(self.broadcast(self.chain.top, self.loop, self.peers))
        
    def broadcast(self, block, loop, peers):
        for peer in peers:
            reader, writer = asyncio.open_connection(peer.addr, peer.port, loop=loop)
            write.write(BlockUtils.blockToData(block))
            response = await reader.read(100)
            print(reponse.decode())
            writer.close()
            
        
        
        
