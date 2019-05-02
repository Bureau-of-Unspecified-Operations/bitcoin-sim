from basic_view import ViewDrawer
import pygame
import jygame
from blockchain_viewmodel import BlockchainViewmodel
from queue import *
from block_utils import BlockUtils
from threading import Thread



def main():
    q = Queue()
    bcVM = BlockchainViewmodel(BlockUtils.generateChain("Jacob", 5))
    vm = ViewDrawer(500,500, q)
    t = Thread(target = vm.run)
    t.start()
    q.put(bcVM)
