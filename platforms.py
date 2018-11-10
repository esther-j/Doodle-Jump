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
    
def createPlatform(data, platformNum):
    cx = random.randint(data.widthPlatform // 2, data.width - data.widthPlatform // 2)
    cy = platformNum * data.space
    return Platforms(cx, cy)
        
def init(data):
    data.scroll = 0
    data.widthPlatform = 8
    data.heightPlatform = 3
    data.numPlatforms = 6
    data.space = data.height // data.numPlatforms
    data.platforms = []
    for platformNum in range(data.numPlatforms):
        data.platforms.append(createPlatform(data, platformNum))
    
    
def redrawAll(canvas, data):
    for platform in data.platforms:
        platform.draw(canvas)
    
def mousePressed(data, event):
    pass
    
def keyPressed(data, event):
    pass

def timerFired(data):
    data.scroll += 3
    for platform in data.platforms:
        platform.cy += 3
        if platform.cy > data.height + platform.height/2:
            data.platforms.remove(platform)
            data.platforms.append(createPlatform(data, 0))

        

def run(width=500, height=500):
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
run()