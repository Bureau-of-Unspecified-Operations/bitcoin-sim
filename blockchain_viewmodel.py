import pygame
import jygame
import Colors

class Block(jygame.DrawableTextRect):
        def __init__(self, uid, height, miner, cx, cy):
            margin = 10
            rColor = Colors.ORANGE
            tColor = Colors.BLACK
            fSize = 12
            text = "Height: " + str(height) + "\n" + "UID: " + str(uid) + "\n" + "Mined by: " + miner
            super().__init__(text, cx, cy, margin, rColor, tColor, fSize)

class BlockchainViewmodel(object):
    
    def __init__(self, chain):
        self.chain = chain
        self.marginB = 10
        self.marginR = 10
        self.height = 50
        self.width = 50
        self.vertGap = 10
        self.horzGap = 10
        

    def draw(self, screen):
        print("drawing blockchain")
        blocks = list()
        d = dict()
        forks = self.chain.orphans.copy()
        forks.append(self.chain.top)
        for i,block in enumerate(forks):
            cur = block
            while(cur.prev != None):
                n = cur.height - 1
                y = self.marginB + cur.height * self.height + n * self.vertGap
                x = self.marginR + (i+1) * self.width + (i-1) * self.horzGap + self.width / 2
                
                pygame.draw.rect(screen, Colors.ORANGE, (x,y,self.width,self.height))
                print("drew rect")
        print("done drawing blockchain")
