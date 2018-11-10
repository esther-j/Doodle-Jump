
import random
from tkinter import * 
class Platforms(object):
    
    def __init__(self, cx, cy):
        self.width = 100
        self.height = 30
        self.cx = cx
        self.cy = cy
    
    def draw(self, canvas):
        canvas.create_rectangle(self.cx - self.width/2, self.cy - self.height/2,
                                self.cx + self.width/2, self.cy + self.height/2,
                                fill = "green")
    
    
class Doodle(object):
    def __init__(self, speedY, speedX, acc, cx, cy, r):
        self.speedY = speedY
        self.speedX = speedX
        self.acc = acc
        self.cx = cx
        self.cy = cy
        self.r = r
        
    def distance(self, blockList):
        hitBlockFlag = 0
        for block in blockList:
            if not abs(self.cx-block.cx) > block.width/8*3:
                hitBlockFlag += 1
        if hitBlockFlag != 1:
            return False
        return True
        
    def draw(self, canvas):
        canvas.create_oval(self.cx-self.r, self.cy-self.r, \
                self.cx+self.r, self.cx+self.r, fill="yellow")
        
            
        
#### Graphics Functions ####

from tkinter import *

def init(data):
    data.doodle = Doodle(-30, 0, -5, data.width/2, data.height-50, 3)
    data.score = 0
    data.timeCalled = 0
    data.scroll = 0
    data.widthPlatform = 8
    data.heightPlatform = 3
    data.numPlatforms = 6
    data.space = data.height // data.numPlatforms
    data.platforms = []
    for platformNum in range(data.numPlatforms):
        data.platforms.append(createPlatform(data, platformNum))
        
        
def createPlatform(data, platformNum):
    cx = random.randint(data.widthPlatform // 2, data.width - data.widthPlatform // 2)
    cy = platformNum * data.space
    return Platforms(cx, cy)        
    
def keyPressed(event, data):
    if event.keysym == "Right":
        data.doodle.speedX += 3
    if event.keysym == "Left":
        data.doodle.speedX -= 3

def timerFired(data):
    data.doodle.speedY += data.doodle.acc
    data.doodle.cy -= data.doodle.speedY
    if data.doodle.distance(data.platforms):
        data.doodle.speedY = -30
    data.scroll += 3
    for platform in data.platforms:
        platform.cy += 3
        if platform.cy > data.height + platform.height/2:
            data.platforms.remove(platform)
            data.platforms.append(createPlatform(data, 0))


def redrawAll(canvas, data):
    for platform in data.platforms:
        platform.draw(canvas)
    data.doodle.draw(canvas)
    
    
        







#################################################################
# use the run function as-is
#################################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)