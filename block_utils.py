from collections import namedtuple
from datetime import datetime
from functools import reduce
import json

class BlockUtils(object):

    # miner -> is name passed by init
    # prev -> last block in the chain
    # height -> height of this block in the chain
    # id -> hash of time when block was mined
    Block = namedtuple("Block", ["miner", "prev", "height", "uid"])

    # top -> tallest block in the chain
    # seconday -> list of all tops of forks
    Chain = namedtuple("Chain", ["top", "orphans"])

    # DEF OF GEN BLOCK (no test)
    def genisisBlock():
        return BlockUtils.Block("GENISIS", None, 1, -1)

    # generate a block of hight = height, by miner = name
    def generateBlock(name, height):
        if height < 1: return None
        if height == 1:
            return BlockUtils.genisisBlock()
        else:
            return BlockUtils.Block(name, BlockUtils.generateBlock(name, height - 1),
                                    height, hash(datetime.now()))
    def generateChain(name, height):
        top = BlockUtils.generateBlock(name, height)
        return None if top == None else BlockUtils.Chain(top, [])

    # requires: cnt >= 1
    def growBlock(start, name, cnt):
        prevBlock = start
        curBlock = start
        while(cnt >= 1):
            curBlock = BlockUtils.Block(name, prevBlock, prevBlock.height + 1,
                                        hash(datetime.now()))
            prevBlock = curBlock
            cnt = cnt - 1
        return curBlock

    # type: Chain * Block -> Chain
    # requires: valid chain
    # ensures: ->chain is valid
    #         if the new forkTop has a previous orphan as it's ancestor, remove from orphan list
    def addForkToChain(chain, forkTop):
        if not BlockUtils.isValidBlock(forkTop):
            print("invalid forkTop")
            return chain

        newOrphans = chain.orphans.copy()
        newTop = chain.top
        for top in chain.orphans:
            if BlockUtils.isAncestorOf(top, forkTop):
                newOrphans.remove(top)
        if forkTop.height > chain.top.height:
            newTop = forkTop
            if not BlockUtils.isAncestorOf(chain.top, forkTop): newOrphans.append(chain.top)
        else:
            newOrphans.append(forkTop)
        return BlockUtils.Chain(newTop, newOrphans)

    # requires: isValidChain(chain) == true
    def addNewBlocks(chain, blocks):
        if len(blocks) == 0: return chain
        else:
            block = blocks.pop(0)
            return BlockUtils.addNewBLocks(BlockUtils.addForkToChain(chain, block), blocks)
        
    # NEEDED
    # Type: Chain * str -> Chain
    def mineNewBlock(chain, name):
        print("mining new")
        
        return BlockUtils.addForkToChain(chain, BlockUtils.Block(name, chain.top,
                                                                 chain.top.height + 1,
                                                                 hash(datetime.now()))
                                         )

    # checks if the trg block exists along the src's history
    # TESTED
    def isAncestorOf(trg, src):
        # check for genisis block
        if trg.uid == -1:
            return True
        curBlock = src
        while(curBlock.prev != None):
            if curBlock.uid == trg.uid:
                return True
            curBlock = curBlock.prev
        return False

    # runs a BFS search for the trg block, starting at all top/secondaries of the chain
    # return None if trg not in chain
    def findBlockOnChain(chain, trg):
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

    ###########################
    # TRANSMITTING BLOCKS
    ###########################

    def blockToDict(block):
        if block.height == 1:
            return block._asdict()
        else:
            prev = BlockUtils.blockToDict(block.prev)
            newDict = block._asdict()
            newDict["prev"] = prev
            return newDict

    def blockToJson(block):
        return json.dumps(BlockUtils.blockToDict(block))

    def dictToBlock(d):
        if d["prev"] == None:
            return BlockUtils.genisisBlock()
        else:
            prev = BlockUtils.dictToBlock(d["prev"])
            newBlock = BlockUtils.Block(d["miner"], prev, d["height"], d["uid"])
            return newBlock


    def jsonToBlock(data):
        return BlockUtils.dictToBlock(json.loads(data))
        


    ############################
    ## VALIDATION CODE
    ############################

    def hasGenisis(block):
        visited = set()
        while(block.prev != None):
            if block.uid in visited: return False
            visited.add(block.uid)
            block = block.prev
        return block.miner == "GENISIS" and block.height == 1 and block.uid == -1

    def hasValidHeights(block):
        cur = block
        visited = set()
        while(cur.prev != None):
            if cur.uid in visited: return False
            visited.add(cur.uid)
            if cur.prev.height != cur.height - 1 or cur.height < 2:
                return False
            cur = cur.prev
        return cur.height == 1

    def isValidBlock(block):
        return BlockUtils.hasGenisis(block) and BlockUtils.hasValidHeights(block)
        

    def isValidChain(chain):
        if chain.top.height < sum(map(lambda block: block.height, chain.orphans)):
            return False
        blocks = chain.orphans.copy()
        blocks.append(chain.top)
        return reduce(lambda b1,b2: b1 and b2 ,
                      map(lambda block: BlockUtils.isValidBlock(block), blocks),
                      True)
        ''' 1. no cycles (checked by hasGen)
            2. all blocks have correct height
            3. all blocks connect to genisis (checked by hasGen())
            4. all blocks connect to the same genisis block (only one Gen)
            5. all blocks have unique uid 
            6. top is in fact the tallest (or equal)
        '''
        pass
 

