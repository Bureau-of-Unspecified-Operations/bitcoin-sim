from collections import namedtuple

class BlockUtils(object):

    def genisisBlock(name, time):
        return BlockUtils.Block(name, None, 1, hash(time))

    # assert: len(names) = len(times) = height
    def generateChain(names, times):
        top = BlockUtils.Block(names[0], None, 1, hash(times[0]))
        for i in range(1, len(names)):
            top = BlockUtils.Block(names[i], top, i + 1, hash(times[i]))
        return BlockUtils.Chain(top, [])

    def generateDummyChain(height):
        return BlockUtils.generateChain([x for x in range(0, height)], [x for x in range(0, height)])


    # grows a fork onto existing chain from start block, using names and times
    def growForkOnChain(chain, start, names, times):
        top = start
        height = top.height + 1
        for i in range(len(names)):
            top = BlockUtils.Block(names[i], top, height, hash(times[i]))
            height = height + 1
            
        secondary = chain.secondary.copy()
        if start in secondary:
            secondary.remove(start)
             
        if top.height > chain.top.height:
            secondary.append(chain.top)
            newTop = top
        else:
            secondary.append(top)
            newTop = chain.top

        return BlockUtils.Chain(newTop, secondary)

    # yucky code duplicatio here and above
    def addForkToChain(chain, newBlock):
        foundBlock = BlockUtils.findBlock(chain, newBlock):
        secondary = chain.secondary.copy
            
        if foundBlock == None:
            print("newBlock is an orphan")
            return chain
        else:
            if foundBlock in secondary:
                secondary.remove(foundBlock)
                
            if newBlock.height > chain.top.height:
                secondary.append(chain.top)
                newTop = newBlock
            else:
                secondary.append(newBlock)
                newTop = chain.top
        return BlockUtils.Chain(newTop, secondary)


    # yeah recursion!
    def addNewBlocks(chain, blocks):
        if len(blocks) == 0: return chain
        else:
            block = blocks.pop(0)
            return BlockUtils.addNewBLocks(BlockUtils.addForkToChain(chain, block), blocks)
        

    def mineNewBlock(chain, name, time):
        return BlockUtils.addForkToChain(chain, chain.top, [name], [time])

    # runs a BFS search for the trg block, starting at all top/secondaries of the chain
    # return None if trg not in chain
    def findBlock(chain, trg):
        queue = chain.seconday.copy()
        queue.append(chain.top)
        visited = set()
        
        while(len(queue) != 0):
            block = queue.pop(0)
            if block.uid in visited:
                continue
            if trg.uid == block.uid:
                return block
            visited.add(block.uid)
            queue.append(block.prev)
            
        return None


    ############################
    ## VALIDATION CODE
    ############################
    # returns bool, and the genisis block
    def hasGenisis(block, maxDepth):
        visited = set()
        cnt = 0
        while(block.prev != None and cnt < maxDepth):
            if block in visited: return False
            visited.add(block)
            block = block.prev
            cnt = cnt + 1
            if cnt >= maxDepth: return False
        return block.height == 1, block

    def haveSameGenisis(blocks):
        b, oldGen = BlockUtils.hasGenisis(blocks.pop(0))
        if b == False: return False
        
        while(len(blocks) > 0):
            b, curGen = BlockUtils.hasGenisis(blocks.pop(0))
            if b == False or curGen.uid != oldGen.uid: return False
        return True

    def isValidChain(chain):
        ''' 1. no cycles
            2. all blocks have correct height
            3. all blocks connect to genisis
            4. all blocks connect to the same genisis block
            5. all blocks have unique uid (maybe?)
        '''
        pass
    
    '''def printChain(chain):
        gen = chain.top
        while(gen.prev != None):
            gen = gen.prev
        '''

    
    

    # miner -> is name passed by init
    # prev -> last block in the chain
    # height -> height of this block in the chain
    # id -> hash of time when block was mined
    Block = namedtuple("Block", ["miner", "prev", "height", "uid"])

    # top -> tallest block in the chain
    # seconday -> list of all tops of forks
    Chain = namedtuple("Chain", ["top", "secondary"])

    
    Peer = namedtuple("Peer", ["ip", "port", "name"])
