import random
from tkinter import * 

# Platform class
class Platforms(object):
    
    # Initialize values of class
    def __init__(self, cx, cy):
        self.width = 100
        self.height = 10
        self.cx = cx
        self.cy = cy
    
    # Draw individual platforms
    def draw(self, canvas):
        canvas.create_rectangle(self.cx - self.width/2, self.cy - self.height/2,
                                self.cx + self.width/2, self.cy + self.height/2,
                                fill = "green")
    
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
    
    # Function to check if doodle has landed on a platform    
    def distance(self, blockList):
        for block in set(blockList):
            if abs(self.cx-block.cx) < block.width/9*4:
                
                # Since iterating through platforms take time, modify the 
                # checking bounds for platforms on top and bottom
                
                if self.cy <= block.cy-block.height/2-self.r \
                and self.cy >= block.cy - block.height/2-3.2*self.r:
                    return True

        return False
    
    # Draw the doodle character    
    def draw(self, canvas):
        canvas.create_oval(self.cx-self.r, self.cy-self.r, \
                self.cx+self.r, self.cy+self.r, fill="yellow")
        
            
        
#### Graphics Functions ####

from tkinter import *

####################################
# init and various functions
####################################


# Initialize graphics data
def init(data):
    # Begin at start screen mode
    data.mode = "startScreen"
    
    data.timeOnPlatform = 6
    data.doodle = Doodle(0, 0, 1.95, data.width/2, data.height/2, 10)
    data.score = 0
    data.timeCalled = 0
    data.scroll = 0
    data.widthPlatform = 8
    data.heightPlatform = 3
    data.numPlatforms = 8
    data.space = data.height // data.numPlatforms
    data.platforms = []
    for platformNum in range(data.numPlatforms-1):
        data.platforms.append(createPlatform(data, platformNum))
    data.platforms.append(firstPlatform(data))
    data.timerCalled = 0
    
    data.playing = True
    
# Make sure the first platform isn't too skewed from the center        
def firstPlatform(data):
    cx = random.randint(data.width/2-100, data.width/2+100)
    cy = data.space*7
    return Platforms(cx, cy)
 
# Generate rest of platforms
def createPlatform(data, platformNum):
    cx = random.randint(data.widthPlatform // 2, \
            data.width - data.widthPlatform // 2)
    cy = platformNum * data.space
    return Platforms(cx, cy)        

    
####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    if data.mode == "startScreen": 
        startScreenMousePressed(event, data)
    elif data.mode == "playGame":   
        playGameMousePressed(event, data)
    elif data.mode == "help":       
        helpScreenMousePressed(event, data)
    elif data.mode == "pauseScreen":
        pauseScreenMousePressed(event, data)

def keyPressed(event, data):
    if data.mode == "startScreen": 
        startScreenKeyPressed(event, data)
    elif data.mode == "playGame":   
        playGameKeyPressed(event, data)
    elif data.mode == "help":       
        helpScreenKeyPressed(event, data)
    elif data.mode == "pauseScreen":
        pauseScreenKeyPressed(event, data)


def redrawAll(canvas, data):
    if data.mode == "startScreen": 
        startScreenRedrawAll(canvas, data)
    elif data.mode == "playGame":   
        playGameRedrawAll(canvas, data)
    elif data.mode == "help":       
        helpScreenRedrawAll(canvas, data)
    elif data.mode == "pauseScreen":
        pauseScreenRedrawAll
        
def timerFired(data):
    if data.mode == "playGame":   
        playGameTimerFired(data)
        

####################################
# startScreen Mode
####################################    

def startScreenKeyPressed(event, data):
    if event.keysym == 's':
        data.mode = 'playGame'
    if event.keysym == 'h':
        data.mode = 'help'
        
def startScreenRedrawAll(canvas, data):
    for platform in data.platforms:
        platform.draw(canvas)
        
    # Determine font size according to window size                        
    fontSizeSmall = int(data.width/35)
    fontSizeBig = int(data.width/18)
        
    canvas.create_text(data.width/2, data.height*0.3,\
        text = "DOODLE KINECT", font = "Arial "+str(fontSizeBig)+" bold", \
        fill = 'black')
    
    canvas.create_text(data.width/2, data.height*0.4,\
        text = "Press 's' to start the game! \n Press 'h' for instructions", \
                       font = "Arial "+str(fontSizeSmall))

def startScreenMousePressed(event, data):
    pass
        


####################################
# playScreen mode
####################################    

# Keypressed Controller   
def playGameKeyPressed(event, data):
    if event.keysym == "Right":
        data.doodle.speedX += 5
        # Doodle stops acceclaring in x-direction once reached max value
        if data.doodle.speedX >= 20:
            data.doodle.speedX = 20
    if event.keysym == "Left":
        data.doodle.speedX -= 5
        if data.doodle.speedX <= -20:
            data.doodle.speedX = -20
    elif event.keysym == "r":
        data.mode = 'startScreen'

# Timer Fired Controller
def playGameTimerFired(data):
    if data.timeOnPlatform < 6:
        data.timeOnPlatform += 1
    if data.playing:
        data.timerCalled += 1
        # Check whether doodle lands on a platform
        if data.doodle.distance(data.platforms):
            data.timeOnPlatform = 0
            data.doodle.speedY = -25
            data.score += 1    # Update data score once doodle lands on platform
            
        # Doodle drops due to constance gravity
        data.doodle.speedY += data.doodle.grav
        data.doodle.cy += data.doodle.speedY
        data.doodle.cx += data.doodle.speedX
        data.scroll += 3
        
        # Wrap around
        if data.doodle.cx < 0:
            print("checking")
            data.doodle.cx = data.width
        elif data.doodle.cx > data.width:
            print("checking again")
            data.doodle.cx = 0
        
        # Check whether player has lost:
        if data.doodle.cy+data.doodle.r > data.height:
            data.playing = False
        
        # Scroll down screen and generate platforms
        for platform in data.platforms:
            if data.timeOnPlatform < 6:
                platform.cy += 20
            else:
                platform.cy += 3
            if platform.cy > data.height + platform.height/2:
                data.platforms.remove(platform)
                data.platforms.insert(0, createPlatform(data, 0))
            

# Redraw Viewer
def playGameRedrawAll(canvas, data):
    for platform in data.platforms:
        platform.draw(canvas)
    data.doodle.draw(canvas)
    canvas.create_text(50, 25, text = "Score: "+str(data.score), \
                    font = "Ariel 12 bold")
    if not data.playing:
        canvas.create_text(data.width/2, data.height/2, text = "You Lose!!!\nPress 'r' to restart the game", 
        font = "Arial "+str(int(data.width/35))+" bold", fill = 'black')
    
####################################
# helpScreen mode
####################################    

def helpScreenKeyPressed(event, data):
    if event.keysym == "r":
        data.mode = 'startScreen'

def helpScreenMousePressed(event, data):
    pass

def helpScreenRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/2, 
    text = "Use Left/Right keys to move the ball and stop it from falling!\nPress 'r' to go back to startScreen", font = "Ariel 15 bold")


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
