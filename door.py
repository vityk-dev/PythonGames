import pygame

class Door:
   
    def __init__(self,x,y,req_key):
        self.rect = pygame.Rect(x,y,20,20)
        self.req_key = req_key
        self.opened = False
        
    def checkOp(self, inventory):
        for item in inventory:
            if item.name == self.req_key:
                self.opened = True
                return True
        return False
        
    def try_doors(self, inventory):
        if not self.opened and self.checkOp(inventory):
            self.opened = True
    def draw(self,screen):
        if not self.opened:
            pygame.draw.rect(screen, (101,67,33), self.rect)