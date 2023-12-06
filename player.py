### MODULES ####################################################################
from cmu_graphics import*

from vectors import*

from PIL import Image
import os, pathlib
################################################################################

'''
Player class is used for Kirby and consists of every position, velocity, and
acceleration constant in R2. It also self.scribbleIndex to determine if and
which scribble in the game's list the player is rolling along, self.lineIndex to
determine which line of that scribble it's on, AND self.friction and gravity
to accumulate appropriately over time along the scribble.
'''

class Player:
    def __init__(self, x, y):
        self.r = 40
        # set image to kirby and default direction to forward
        tempImage = Image.open("assets/kirby_skateboard.png")
        tempImage = tempImage.resize((80, 80))
        tempImage = tempImage.transpose(Image.FLIP_LEFT_RIGHT)
        self.image = CMUImage(tempImage)
        self.forward = True

        self.x = x
        self.y = y
        self.dx = 2
        self.dy = 0
        self.ddx = 0
        self.ddy = 0.15

        # scribble related fields
        self.scribbleIndex = None
        self.lineIndex = None

        # health for getting hit by waddle doos
        self.health = 3
    
    def draw(self):
        drawImage(self.image, self.x, self.y, align="center")

    # every step the player moves in a variable behavior
    def step(self, app):
        # flip the image if going backwards
        if self.dx < 0 and self.forward:
            tempImage = Image.open("assets/kirby_skateboard.png")
            tempImage = tempImage.resize((80, 80))
            self.image = CMUImage(tempImage)
            self.forward = not self.forward
        elif self.dx >= 0 and not self.forward:
            tempImage = Image.open("assets/kirby_skateboard.png")
            tempImage = tempImage.resize((80, 80))
            tempImage = tempImage.transpose(Image.FLIP_LEFT_RIGHT)
            self.image = CMUImage(tempImage)
            self.forward = not self.forward

        # if the player is rolling along a line
        if self.scribbleIndex != None:
            scribble = app.scribbles[self.scribbleIndex]
            scribbleStart = scribble.points[0][0]
            scribbleEnd = scribble.points[-1][0]
            # if it's a slippery Line
            if scribble.ability == "slippery":
                # change direction based on dx and line drawn direction
                if self.dx >= 0 and scribbleEnd >= scribbleStart:
                    self.rollingMotionForward()
                elif self.dx >= 0 and scribbleEnd < scribbleStart:
                    self.rollingMotionBackward()
                elif self.dx < 0 and scribbleEnd > scribbleStart:
                    self.rollingMotionBackward()
                else:
                    self.rollingMotionForward()

            # if it's a speedy line
            elif scribble.ability == "speedy":
                if scribbleStart < scribbleEnd and not self.forward:
                    tempImage = Image.open("assets/kirby_skateboard.png")
                    tempImage = tempImage.resize((80, 80))
                    tempImage = tempImage.transpose(Image.FLIP_LEFT_RIGHT)
                    self.image = CMUImage(tempImage)
                    self.forward = not self.forward
                elif scribbleStart >= scribbleEnd and self.forward:
                    tempImage = Image.open("assets/kirby_skateboard.png")
                    tempImage = tempImage.resize((80, 80))
                    self.image = CMUImage(tempImage)
                    self.forward = not self.forward
                self.rollingMotionForward(frictionConstant=0.9)

            # if it's a springy line
            elif scribble.ability == "springy":
                self.bounceMotion()

        # else then it's normal Newtonian motion
        else:
            self.x += self.dx
            self.y += self.dy
            self.dx += self.ddx
            self.dy += self.ddy

        self.borderBounce(app)

    def rollingMotionForward(self, frictionConstant=0.2):
        scribble = app.scribbles[self.scribbleIndex]
        i = self.lineIndex

        # if player is in the middle of the scribble
        if 0 < i < len(scribble.points):
            currentX, currentY = scribble.points[i][0], scribble.points[i][1]
            previousX, previousY = scribble.points[i-1][0], scribble.points[i-1][1]

            # create a vector from current line segment
            previousPoint = (previousX, previousY)
            currentPoint = (currentX, currentY)
            v = Vector.fromPoints(previousPoint, currentPoint)

            # scale vector by friction constant
            v = Vector.scale(v, frictionConstant)
            x, y = v

            # increment player along segment vector until it reaches next point
            # if next point is going to be reached, shift center to next segment
            if self.x + x > currentX or self.y + y > currentY:
                self.lineIndex += 1
                self.x = currentX
                self.y = currentY
            else:
                self.x += x
                self.y += y

        # if player is all out of scribble to roll on
        if i == len(scribble.points):
            # reset all scribble related fields
            self.lineIndex = 0
            self.scribbleIndex = None

            # disable scribble and gray it out
            scribble.active = False
            
            # average last 5 segment vectors or first if out of range
            if i < 5:
                exitStart = scribble.points[0]
            else:
                exitStart = scribble.points[i-5]
            exitEnd = scribble.points[i-1]
            exitVector = Vector.fromPoints(exitStart, exitEnd)

            # unitize then scale vector by exit constant
            exitVector = Vector.unitize(exitVector)
            if frictionConstant > 0.2:
                exitVector = Vector.scale(exitVector, 20)
            else:
                exitVector = Vector.scale(exitVector, 10)

            # make exit velocity the exit vector
            self.dx, self.dy = exitVector

    def rollingMotionBackward(self):
        scribble = app.scribbles[self.scribbleIndex]
        i = self.lineIndex

        # if player is in the middle of the scribble
        if 0 < i < len(scribble.points):
            previousX, previousY = scribble.points[i][0], scribble.points[i][1]
            currentX, currentY = scribble.points[i-1][0], scribble.points[i-1][1]

            # create a vector from current line segment
            previousPoint = (previousX, previousY)
            currentPoint = (currentX, currentY)
            v = Vector.fromPoints(previousPoint, currentPoint)

            # scale vector by friction constant
            v = Vector.scale(v, 0.4)
            x, y = v

            # increment player along segment vector until it reaches next point
            # if next point is going to be reached, shift center to next segment
            if self.x + x < currentX or self.y + y < currentY:
                self.lineIndex -= 1
                self.x = currentX
                self.y = currentY
            else:
                self.x += x
                self.y += y

        # if player is all out of scribble to roll on
        if i == 0:
            # reset all scribble related fields
            self.lineIndex = 0
            self.scribbleIndex = None

            # disable scribble and gray it out
            scribble.active = False
            
            # average last 5 segment vectors or first if out of range
            if len(scribble.points) <= 5:
                exitStart = scribble.points[len(scribble.points)-1]
            else:
                exitStart = scribble.points[5]
            exitEnd = scribble.points[0]
            exitVector = Vector.fromPoints(exitStart, exitEnd)

            # unitize then scale vector by exit constant
            exitVector = Vector.unitize(exitVector)
            exitVector = Vector.scale(exitVector, 10)

            # make exit velocity the exit vector
            self.dx, self.dy = exitVector

    def bounceMotion(self):
        scribble = app.scribbles[self.scribbleIndex]
        i = self.lineIndex

        # create exit vector from original and new coordinate
        exitStart = (self.originalX, self.originalY)
        exitEnd = (self.x, self.y)
        exitVector = Vector.fromPoints(exitStart, exitEnd)

        # unitize then invert vector by exit constant
        exitVector = Vector.unitize(exitVector)
        exitVector = Vector.scale(exitVector, -10)

        # reset all scribble related fields
        self.lineIndex = 0
        self.scribbleIndex = None

        # disable scribble and gray it out
        scribble.active = False

        # make exit velocity the exit vector
        self.dx, self.dy = exitVector

    def borderBounce(self, app):
        # bounces ball off all walls of canvas in very bug free way
        if (self.x - self.r) < 0:
            if self.dx < 0:
                self.x = self.r
                self.dx *= -0.8
        elif (self.x + self.r) >= app.width:
            if self.dx > 0:
                self.x = app.width - self.r
                self.dx *= -0.8

        if (self.y - self.r) < 0:
            if self.dy < 0:
                self.y = self.r
                self.dy *= -0.8
        elif (self.y + self.r) > app.height:
            if self.dy > 0:
                self.y = app.height - self.r
                self.dy *= -0.8