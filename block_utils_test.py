import unittest
from block_utils import BlockUtils as BU
import datetime
from collections import namedtuple

# Yo! I just realized I can't make blocks chains that loop :)
class TestBlock(unittest.TestCase):

    def setUp(self):
        fGen = BU.Block("me", None, 2, hash(1))
        self.fakeGenisis = BU.Block("me", BU.Block("me", fGen, 2, hash(2)), 3, hash(3))        

    def testBlockTuple(self):
        time = hash(datetime.datetime.now())
        block = BU.Block("name", None, 1, time)
        self.assertEqual(block.miner, "name")

    def testGenerate(self):
        chain = BU.generateChain(["a"] * 5, [x for x in range(1,6)])
        block = chain.top
        cnt = 5
        while(block.prev != None):
            self.assertEqual(block.height, cnt)
            self.assertEqual(block.uid, hash(cnt))
            cnt = cnt - 1
            block = block.prev

    def testAddFork(self):
        chain = BU.generateDummyChain(5)
        start = chain.top.prev.prev
        genisis = start.prev.prev
        fChain = BU.growForkOnChain(chain, start, ["a"] * 3, ["a"] * 3)
        nub = fChain.top.prev.prev
        self.assertEqual(fChain.top.height, 6)
        self.assertEqual(len(fChain.secondary), 1)
        self.assertEqual(fChain.secondary[0].height, 5)
        fChain = BU.growForkOnChain(fChain, nub, ["a"], ["a"])
        self.assertEqual(fChain.top.height, 6)
        self.assertEqual(len(fChain.secondary), 2)
        fChain = BU.growForkOnChain(fChain, genisis, ["A"] * 8, ["A"] * 8)
        self.assertEqual(fChain.top.height, 9)
        self.assertEqual(len(fChain.secondary), 3)
        fChain = BU.growForkOnChain(fChain, chain.top, ["A"] * 5, ['A'] * 5)
        self.assertEqual(fChain.top.height, 10)
        # check deletes secondaries tht have been added to
        self.assertEqual(len(fChain.secondary), 3)
        #no dangling
        for block in fChain.secondary:
            b, gen = BU.hasGenisis(block)
            self.assertEqual(b, True)

    def testHasGenisis(self):
        b, gen = BU.hasGenisis(self.fakeGenisis)
        self.assertEqual(b, False)
        b, gen = BU.hasGenisis(BU.genisisBlock("me", 1))
        self.assertEqual(b, True)
        b, gen = BU.hasGenisis(BU.generateDummyChain(10).top)
        self.assertEqual(b, True)

        
if __name__ == '__main__':
    unittest.main()
