import random
from tkinter import * 

# Platform class
class Platforms(object):
    speedY = 0
    
    # Initialize values of class
    def __init__(self, cx, cy):
        self.width = 100
        self.height = 10
        self.cx = cx
        self.cy = cy
        self.color = "orange"
    
    # Draw individual platforms
    def draw(self, canvas):
        canvas.create_rectangle(self.cx - self.width/2, self.cy - self.height/2,
                                self.cx + self.width/2, self.cy + self.height/2,
                                fill = self.color)
        
class PowerUp(Platforms):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.color = "blue"

class MovingPlatforms(Platforms):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.color = "pink"
        self.speed = random.randint(3, 7)
        
class BreakingPlatforms(Platforms):
    def __init__(self, cx, cy):
        super().__init__(cx, cy)
        self.color = "Red"   
         
# Doodle character class    
class Doodle(object):
#     
    # Initialize values of class
    def __init__(self, speedY, speedX, grav, cx, cy, r):
        self.speedY = speedY
        self.speedX = speedX
        self.grav = grav
        self.cx = cx
        self.cy = cy
        self.r = r
        self.jumpSpeed = -35
        self.shiftx = 0

    def getmove(self):
        return (self.jumpSpeed, self.grav)
    
    # Function to check if doodle has landed on a platform    
    def distance(self, blockList):
        for block in set(blockList):
            surfaceY = block.cy-block.height/2-self.r
            if self.cy <= surfaceY and self.cy + self.speedY >= surfaceY and \
                abs(self.cx-block.cx) < block.width/2:
                if type(block) == Platforms or type(block) == MovingPlatforms:
                    self.jumpSpeed = -35
                elif type(block) == PowerUp:
                    self.jumpSpeed = -55
                return surfaceY
        return None
    
    # Draw the doodle character    
    def drawEyes(self, canvas):
        shift = self.shiftx
        eyeSpace = self.r // (1.5 + abs(shift)*.5)
        eyeHeight = self.r // 10
        if self.speedY <= 20:
            er = self.r // 4.2
        else:
            er = self.r //3.8
        x1 = self.cx - eyeSpace/2 - er + self.r*shift*.2
        x2 = self.cx + eyeSpace/2 + er + self.r*shift*.2
        y1 = self.cy - eyeHeight - er
        y2 = self.cy - eyeHeight - er
        canvas.create_oval(x1-er, y1-er, x1+er, y1+er, fill = 'white')
        canvas.create_oval(x2-er, y2-er, x2+er, y2+er, fill = 'white')
        pr = er // 2
        ps = shift*.5*(pr-er)
        canvas.create_oval(x1-pr-ps, y1-pr, x1+pr-ps, y1+pr, fill = 'black')
        canvas.create_oval(x2-pr-ps, y2-pr, x2+pr-ps, y2+pr, fill = 'black')
    
    def drawMouth(self, canvas):
        shift = self.shiftx
        mr = self.r // 5
        my = self.r // 5
        ms = self.r*shift*.2
        if self.speedY <= 15:
            mouthA = 120
            canvas.create_arc(self.cx-mr+ms, self.cy-mr-my, self.cx+mr+ms, self.cy+mr-my, \
                                start = (mouthA-180)/2, extent = -mouthA, \
                                style = 'arc', width = 2)
        else:
            canvas.create_oval(self.cx-mr*.6+ms, self.cy-mr/8-my, self.cx+mr*.6+ms, self.cy+mr-my, \
                                fill = 'black')
    
    def checkShift(self):
        if -5 <= self.speedX <= 5:
            self.shiftx = 0
        elif self.speedX > 5:
            self.shiftx = 1
        else:
            self.shiftx = -1

    
    def draw(self, canvas):
        r = self.r
        # Draw Body
        canvas.create_oval(self.cx-r, self.cy-r, self.cx+r, self.cy+r, fill = 'green')
        self.drawEyes(canvas)
        self.drawMouth(canvas)
        
class Background:
    def __init__(self, jumpy):
        self.r = 200
        self.g = 255
        self.b = 200
        self.change = 1
        height, accel = jumpy.getmove()
        self.degree = int(23 // (-height / accel))
        self.color = '#c8ffc8'
    
    # Switch the color that's changing and how
    def newChange(self):
        newC = random.randint(0,2)
        sign = -1**random.randint(0,1)
        if self.change != newC or sign == -1:
            self.change = newC
            self.degree *= sign
        else:
            self.newChange()
    
    def update(self):
        change = self.change
        degree = self.degree
        test = [self.r, self.g, self.b][change] + degree
        if test > 255 or test < 200:
            self.newChange()
            self.update()
        elif change == 0:
            self.r += degree
        elif change == 1:
            self.g += degree
        else:
            self.b += degree
        self.color = '#' + hex(self.r)[2:] + hex(self.g)[2:] + hex(self.b)[2:] 
            
    
    def draw(self, data, canvas):
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill=self.color, width=0)
                                
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
    data.doodle = Doodle(0, 0, 1.95, data.width/2, data.height/2, 20)
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
    data.bg = Background(data.doodle)
    data.playing = True
    
# Make sure the first platform isn't too skewed from the center        
def firstPlatform(data):
    cx = random.randint(data.width/2-100, data.width/2+100)
    cy = data.space*7
    return Platforms(cx, cy)
 
# Generate rest of platforms
def createPlatform(data, platformNum):
    cx = random.randint(data.widthPlatform//2, \
            data.width - data.widthPlatform//2)
    cy = platformNum * data.space
    platformType = random.choice([Platforms, Platforms, Platforms, PowerUp, MovingPlatforms])
    return platformType(cx, cy)      

    
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
    elif data.mode == 'endGame':
        endGameMousePressed(event, data)

def keyPressed(event, data):
    if data.mode == "startScreen": 
        startScreenKeyPressed(event, data)
    elif data.mode == "playGame":   
        playGameKeyPressed(event, data)
    elif data.mode == "help":       
        helpScreenKeyPressed(event, data)
    elif data.mode == "pauseScreen":
        pauseScreenKeyPressed(event, data)
    elif data.mode == 'endGame':
        endGameKeyPressed(event, data)


def redrawAll(canvas, data):
    if data.mode == "startScreen": 
        startScreenRedrawAll(canvas, data)
    elif data.mode == "playGame":   
        playGameRedrawAll(canvas, data)
    elif data.mode == "help":       
        helpScreenRedrawAll(canvas, data)
    elif data.mode == "pauseScreen":
        pauseScreenRedrawAll(canvas, data)
    elif data.mode == 'endGame':
        endGameRedrawAll(canvas, data)
        
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
    elif event.keysym == "Left":
        data.doodle.speedX -= 5
        if data.doodle.speedX <= -20:
            data.doodle.speedX = -20
    data.doodle.checkShift()

def playGameMousePressed(event, data):
    pass

# Timer Fired Controller
def playGameTimerFired(data):

    if data.timeOnPlatform < 6:
        data.timeOnPlatform += 1
    if data.playing:
        hit = False
        data.timerCalled += 1
        # Check whether doodle lands on a platform
        # Doodle drops due to constance gravity
        data.doodle.speedY += data.doodle.grav
        data.doodle.cx += data.doodle.speedX
        data.scroll += 3
        
        if data.doodle.speedY > 0:
            height = data.doodle.distance(data.platforms)
            if height:
                data.timeOnPlatform = -1
                data.doodle.speedY = data.doodle.jumpSpeed
                data.doodle.cy = height
                data.bg.newChange()
                hit = True
        else:
            data.bg.update()
            
        # Wrap around
        if data.doodle.cx < 0:
            data.doodle.cx = data.width
        elif data.doodle.cx > data.width:
            data.doodle.cx = 0
        
        # Check whether player has lost:
        if data.doodle.cy+data.doodle.r > data.height:
            #data.playing = False
            data.mode = 'endGame'
        
        # Scroll down screen and generate platforms
        if data.doodle.cy <= data.height / 3:
            Platforms.speedY += 2
        elif Platforms.speedY > 0:
            Platforms.speedY -= 3
            if Platforms.speedY < 0:
                Platforms.speedY = 0
        
        for platform in data.platforms:
            platform.cy += Platforms.speedY * (5/4)
            if platform.cy > data.height + platform.height/2:
                data.platforms.remove(platform)
                data.platforms.insert(0, createPlatform(data, 0))
                data.score += 1
        
        if not hit:    
            data.doodle.cy += data.doodle.speedY * (3/5) + Platforms.speedY * (5/4)

# Redraw Viewer
def playGameRedrawAll(canvas, data):
    data.bg.draw(data, canvas)
    for platform in data.platforms:
        platform.draw(canvas)
        if type(platform) == MovingPlatforms:
            platform.cx += platform.speed
            if platform.cx + platform.width / 2 > data.width or \
            platform.cx - platform.width/2 <= 0:
                platform.speed *= -1
    data.doodle.draw(canvas)
    canvas.create_text(10, 10, text = "Score: "+str(data.score), \
                    anchor = NW, font = "Ariel 20 bold")
    if not data.playing:
        data.mode = 'pauseScreen'
    
    
####################################
# endGame mode
####################################  
    
def endGameMousePressed(event, data):
    pass    
    
def endGameKeyPressed(event, data):
    if event.keysym == "r":
        data.mode = 'startScreen'
        data.doodle = Doodle(0, 0, 1.95, data.width/2, data.height/2, 20)
        data.timeOnPlatform = 6
        data.score = 0
        data.scroll = 0
        data.platforms = []
        for platformNum in range(data.numPlatforms-1):
            data.platforms.append(createPlatform(data, platformNum))
        data.platforms.append(firstPlatform(data))
        data.timerCalled = 0
        data.playing = True
    data.doodle.checkShift()    
    
def endGameRedrawAll(canvas, data):
    canvas.create_text(data.width/2, data.height/2, 
                        text = "You Lose!!!\nFinal Score: " + str(data.score) + \
                        "\nPress 'r' to restart the game", 
                        font = "Arial "+str(int(data.width/15))+" bold", 
                        fill = 'black')
    
    
    
####################################
# helpScreen mode
####################################    

def helpScreenKeyPressed(event, data):
    if event.keysym == "r":
        data.mode = 'startScreen'

def helpScreenMousePressed(event, data):
    pass

def helpScreenRedrawAll(canvas, data):
    samplePlatform = Platforms(data.width/6, data.height/3)
    samplePowerUp = PowerUp(data.width/6, samplePlatform.cy + samplePlatform.height * 2)
    sampleMoving = MovingPlatforms(data.width/6, samplePowerUp.cy + samplePowerUp.height * 2)
    canvas.create_text(data.width/2, data.height/2, 
    text = "Use Left/Right keys to move the ball and stop it from falling!\nPress 'r' to go back to startScreen", font = "Ariel 15 bold")
    samplePlatform.draw(canvas)
    canvas.create_text(samplePlatform.cx + samplePlatform.width/2, samplePlatform.cy,
    text = "     Normal Platform: Jumps in normal height", font = "Ariel 15 bold", anchor = W)
    samplePowerUp.draw(canvas)
    canvas.create_text(samplePowerUp.cx + samplePowerUp.width/2, samplePowerUp.cy,
    text = "     Power Up: Jumps higher than normal platform", 
    font = "Ariel 15 bold", anchor = W)
    sampleMoving.draw(canvas)
    canvas.create_text(sampleMoving.cx + sampleMoving.width/2, sampleMoving.cy,
    text = "     Moving Platform: Moves in left/right direction", 
    font = "Ariel 15 bold", anchor = W)


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
