import pygame
import random
import math

class Platforms(object):
    
    # Initialize values of class
    def __init__(self, cx, cy):
        self.width = 100
        self.height = 10
        self.cx = cx
        self.cy = cy
    
    # Draw individual platforms
    def draw(self, screen):
        pygame.draw.rect(screen, (50,205,50), (int(self.cx - self.width/2), int(self.cy - self.height/2),
                                self.width, self.height), 0)
                                
# Doodle character class    
class Doodle(object):
    
    # Initialize values of class
    def __init__(self, speedY, speedX, grav, cx, cy, r):
        self.speedY = speedY
        self.speedX = speedX
        self.grav = grav
        self.cx = cx
        self.cy = cy
        self.r = r
        self.jumpSpeed = -25
        self.shiftx = 0

    def getmove(self):
        return (self.jumpSpeed, self.grav)
    
    # Function to check if doodle has landed on a platform    
    def distance(self, blockList):
        for block in set(blockList):
            if abs(self.cx-block.cx) < block.width/9*4:
                
                # Since iterating through platforms take time, modify the 
                # checking bounds for platforms on top and bottom
                
                if self.cy <= block.cy-block.height/2-self.r \
                and self.cy >= block.cy - block.height/2-3.2*self.r:
                    if type(block) == Platforms:
                        self.jumpSpeed = -25
                    else:
                        self.jumpSpeed = -50
                    return True

        return False
    
    # Draw the doodle character    
    def drawEyes(self, screen):
        shift = int(self.shiftx)
        eyeSpace = int(self.r // (1.5 + abs(shift)*.5))
        eyeHeight = int(self.r // 10)
        er = int(self.r // 4.2)
        x1 = int(self.cx - eyeSpace/2 - er + self.r*shift*.2)
        x2 = int(self.cx + eyeSpace/2 + er + self.r*shift*.2)
        y1 = int(self.cy - eyeHeight - er)
        y2 = int(self.cy - eyeHeight - er)
        pygame.draw.circle(screen, (255, 255, 255), (x1, y1), er, 0)
        pygame.draw.circle(screen, (255, 255, 255), (x2, y2), er, 0)
        pr = er // 2
        ps = shift*.5*(pr-er)        
        #x1-pr-ps, y1-pr, x1+pr-ps, y1+pr
        pygame.draw.circle(screen, (0,0,0), (x1, y1), pr, 0)
        pygame.draw.circle(screen, (0,0,0), (x2, y2), pr, 0)
    
    def drawMouth(self, screen):
        shift = self.shiftx
        mr = self.r // 5
        my = self.r // 5
        ms = int(self.r*shift*.2)
        #self.cx-mr+ms, self.cy-mr-my, self.cx+mr+ms, self.cy+mr-my, \
                                #start = (mouthA-180)/2,
        if self.speedY <= 15:
            pygame.draw.arc(screen, (0,0,0),(self.cx-mr+ms, self.cy-mr-my, 2*mr, 2*mr), \
                                -math.pi//6, -math.pi//6*5, 2)
        else:
            #(screen, (self.cx-mr*.6+ms, self.cy-mr/8-my, self.cx+mr*.6+ms, self.cy+mr-my, \
            pygame.draw.ellipse(screen, (0,0,0), (self.cx, self.cy, 1.2*mr, mr/8*9), 0)
    
    def checkShift(self):
        if -5 <= self.speedX <= 5:
            self.shiftx = 0
        elif self.speedX > 5:
            self.shiftx = 1
        else:
            self.shiftx = -1

    
    def draw(self, screen):
        r = self.r
        # Draw Body
        pygame.draw.circle(screen, (50,205,50), (int(self.cx), int(self.cy)), r, 0)
        self.drawEyes(screen)
        self.drawMouth(screen)
        
class PowerUp(Platforms):
    
    def draw(self, screen):
        super().draw(screen)
        pygame.draw.circle(screen, (240,128,128), (int(self.cx), int(self.cy)), self.height, 0)

class Pygame(object):  

     
    def init(self):
        
        self.timeOnPlatform = 6
        self.doodle = Doodle(0, 0, 1.95, self.width/2, self.height/2, 20)
        self.score = 0
        self.timeCalled = 0
        self.scroll = 0
        self.widthPlatform = 8
        self.heightPlatform = 3
        self.numPlatforms = 8
        self.space = self.height // self.numPlatforms
        self.platforms = []
        self.playing = True
        for platformNum in range(self.numPlatforms-1):
            self.platforms.append(self.createPlatform(platformNum))
        self.platforms.append(self.firstPlatform())
        
    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass


        
    # Make sure the first platform isn't too skewed from the center        
    def firstPlatform(self):
        cx = random.randint(self.width/2-100, self.width/2+100)
        cy = self.space*7
        return Platforms(cx, cy)
    
    # Generate rest of platforms
    def createPlatform(self, platformNum):
        cx = random.randint(self.widthPlatform//2, 300 - self.widthPlatform // 2)
        cy = platformNum * self.space
        platformType = random.choice([Platforms, Platforms, PowerUp])
        return platformType(cx, cy)
    
                    
    def redrawAll(self, screen):
        for platform in self.platforms:
            platform.draw(screen)
        self.doodle.draw(screen)
        basicfont = pygame.font.SysFont(None, 48)
        text = basicfont.render('Score: '+str(self.score), True, (255, 0, 0), (255, 255, 255))
        screen.blit(text, (100, 100))
    
            
            
                    
    def timerFired(self, dt):
        if self.timeOnPlatform < 6:
            self.timeOnPlatform += 1
            
        if self.playing:
            # Check whether doodle lands on a platform
            if self.doodle.distance(self.platforms) and self.doodle.speedY > 0:
                self.timeOnPlatform = 0
                self.doodle.speedY = self.doodle.jumpSpeed
                self.score += 1    # Update self score once doodle lands on platform
                
            # Doodle drops due to constance gravity
            self.doodle.speedY += self.doodle.grav
            self.doodle.cy += self.doodle.speedY
            self.doodle.cx += self.doodle.speedX
            self.scroll += 3
            
            # Wrap around
            if self.doodle.cx < 0:
                self.doodle.cx = self.width
            elif self.doodle.cx > self.width:
                self.doodle.cx = 0
            
            # Check whether player has lost:
            if self.doodle.cy+self.doodle.r > self.height:
                self.playing = False
            
            # Scroll down screen and generate platforms
            for platform in self.platforms:
                if self.timeOnPlatform < 6:
                    platform.cy += 25
                else:
                    platform.cy += 3
                if platform.cy > self.height + platform.height/2:
                    self.platforms.remove(platform)
                    self.platforms.insert(0, self.createPlatform(0))
                    
                    
    def __init__(self, width=600, height=400, fps=50, title="112 Pygame Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

                    
            
                    
    def run(self):
            
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)
    
        # stores all the keys currently being held down
        self._keys = dict()
    
        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                        event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                        event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            pygame.display.flip()
    
        pygame.quit()


def main():
    game = Pygame()
    game.run()

if __name__ == '__main__':
    main()