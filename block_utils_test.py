import unittest
from block_utils import BlockUtils as BU
import datetime
from collections import namedtuple

# Yo! I just realized I can't make blocks chains that loop :)
class TestBlock(unittest.TestCase):

    def setUp(self):
        pass


    def testBlockTuple(self):
        time = hash(datetime.datetime.now())
        block = BU.Block("name", None, 1, time)
        self.assertEqual(block.miner, "name")


    def testGenerateBlock(self):
        self.assertEqual(BU.generateBlock("me", 6).height, 6)
        self.assertEqual(BU.generateBlock("me", 0), None)
        self.assertEqual(BU.generateBlock("me",1), BU.genisisBlock())
        self.assertEqual(BU.isValidBlock(BU.generateBlock("me", 50)), True)

    def testGenerateChain(self):
        self.assertEqual(BU.isValidChain(BU.generateChain("me", 34)), True)
        self.assertEqual(BU.generateChain("me", -5), None)

    def testGrowBlock(self):
        base = BU.generateBlock("me", 15)
        self.assertEqual(base.height, 15)
        top = BU.growBlock(base, "he", 23)
        self.assertEqual(top.height, 15 + 23)
        self.assertEqual(BU.isValidBlock(top), True)
        self.assertEqual(BU.growBlock(base, "he", 0).uid, base.uid)

    '''def testGrowFork(self):
        chain = BU.generateDummyChain(5)
        start = chain.top.prev.prev
        genisis = start.prev.prev
        fChain = BU.growForkOnChain(chain, start, ["a"] * 3, ["a"] * 3)
        nub = fChain.top.prev.prev
        self.assertEqual(fChain.top.height, 6)
        self.assertEqual(len(fChain.orphans), 1)
        self.assertEqual(fChain.orphans[0].height, 5)
        fChain = BU.growForkOnChain(fChain, nub, ["a"], ["a"])
        self.assertEqual(fChain.top.height, 6)
        self.assertEqual(len(fChain.orphans), 2)
        fChain = BU.growForkOnChain(fChain, genisis, ["A"] * 8, ["A"] * 8)
        self.assertEqual(fChain.top.height, 9)
        self.assertEqual(len(fChain.orphans), 3)
        fChain = BU.growForkOnChain(fChain, chain.top, ["A"] * 5, ['A'] * 5)
        self.assertEqual(fChain.top.height, 10)
        # check deletes secondaries tht have been added to
        self.assertEqual(len(fChain.orphans), 3)
        #no dangling
        for block in fChain.orphans:
            b = BU.hasGenisis(block)
            self.assertEqual(b, True)
    '''

    def testHasGenisis(self):
        pass
    
    def testIsAncestor(self):
        b10 = BU.generateBlock("b10", 10)
        foreign = BU.generateBlock("foreign", 5)
        cur = foreign
        while(cur.prev != None):
            self.assertEqual(BU.isAncestorOf(cur, b10), False)
            cur = cur.prev
        cur = b10
        while(cur.prev != None):
            self.assertEqual(BU.isAncestorOf(cur, b10), True)
            cur = cur.prev
        self.assertEqual(BU.isAncestorOf(BU.genisisBlock(), b10), True)

    def testMineNewBlock(self):
        chain = BU.generateChain("me", 5)
        newChain = BU.mineNewBlock(chain, "me")
        self.assertEqual(BU.isValidChain(newChain), True)
        self.assertEqual(len(newChain.orphans), 0)

    def testAddForkToChain(self):
        chain = BU.generateChain("me", 5)
        b3 = chain.top.prev.prev
        fork = BU.growBlock(b3, "me", 3)
        fChain = BU.addForkToChain(chain, fork)
        self.assertEqual(fChain.top.height, 6)
        self.assertEqual(BU.isValidChain(fChain), True)
        self.assertEqual(len(fChain.orphans), 1)
        fChain = BU.addForkToChain(fChain, BU.growBlock(fChain.orphans[0], "me", 2))
        self.assertEqual(BU.isValidChain(fChain), True)
        self.assertEqual(len(fChain.orphans), 1)

        
    def testBlockToFromData(self):
        block = BU.genisisBlock()
        nBlock = BU.jsonToBlock(BU.blockToJson(block))
        self.assertEqual(nBlock.miner, block.miner)
        self.assertEqual(nBlock.prev, block.prev)
        self.assertEqual(nBlock.height, block.height)
        self.assertEqual(nBlock.uid, block.uid)

        block = BU.generateBlock("me", 5)
        nBlock = BU.jsonToBlock(BU.blockToJson(block))
        self.assertEqual(nBlock.miner, block.miner)
        self.assertEqual(nBlock.prev, block.prev)
        self.assertEqual(nBlock.height, block.height)
        self.assertEqual(nBlock.uid, block.uid)

    def testBlockToDict(self):
        block = BU.generateBlock("me", 3)
        d = BU.blockToDict(block)
        self.assertEqual(d["height"], 3)
        

        
if __name__ == '__main__':
    unittest.main()
