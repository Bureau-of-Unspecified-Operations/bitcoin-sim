import pygame
import asyncio
import jygame
from queue import *
import Colors

# Simple view that displays and evolving ViewModel
# Does not animate, mearly updates when ever the ViewModel
# sense a redraw


class ViewDrawer(object):

    def __init__(self, width, height, queue):
        
        self.width = width
        self.height = height
        self.viewModelQueue = queue
        self.frame = jygame.Frame((0,0), width, height)
        self.loop = asyncio.get_event_loop()
    

    # Only Handles quit    
    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

    # Handle events and draw any incoming ViewModels
    def mainLoop(self):
    print("in mainloop")
        while(True):
            self.handleEvents()
            while(not self.viewModelQueue.empty()):
                print("found something in queue")
                vm = self.viewModelQueue.get()
                vm.draw(self.screen)
                #self.screen.blit(self.frame.screen, (self.frame.x,self.frame.y))
                pygame.display.flip()
                print(self.viewModelQueue.epmty())

    def run(self):
        print("run was called")
        pygame.init()
        infoObj = pygame.display.Info()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.loop.run_until_complete(self.mainLoop())

    def quit(self):
        self.loop.stop()
        pygame.quit()
        
        
