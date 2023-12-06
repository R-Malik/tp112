### MODULES ####################################################################
from cmu_graphics import*

from vectors import*

from PIL import Image
import math, os, pathlib
################################################################################

'''
Crayon class stores the position of Kirby's Crystal Crayon and can draw itself 
every time the mouse is moved across the canvas.
'''

class Crayon():
    def __init__(self, x, y, ability):
        self.x = x
        self.y = y
        self.ability = ability

        self.changeColor(ability) # uses method to change image
        self.opacity = 100 # to hide crayon when hovering over buttons

    def draw(self):
        drawImage(self.image, self.x, self.y, align="center", rotateAngle=30, opacity=self.opacity)

    def changeColor(self, ability):
        # changes color of the crayon and ability based on parameter
        self.ability = ability
        if ability == "slippery":
            tempImage = Image.open("assets/crayon_blue.png")
            tempImage = tempImage.resize((30, 60))
            self.image = CMUImage(tempImage)
        elif ability == "speedy":
            tempImage = Image.open("assets/crayon_green.png")
            tempImage = tempImage.resize((30, 60))
            self.image = CMUImage(tempImage)
        elif ability == "springy":
            tempImage = Image.open("assets/crayon_purple.png")
            tempImage = tempImage.resize((30, 60))
            self.image = CMUImage(tempImage)

'''
Anything drawn on the canvas is a Scribble. A new instance of Scribble is
created whenever the user releases the mouse, clicks and draws a new line, then
releases it again. That way Scribbles can be drawn as a continuous connection
of points. A new point is added to the self.points field ever step.
'''

class Scribble():
    def __init__(self, ability):
        self.points = []
        self.active = True
        self.ability = ability

    def addPoint(self, x1, y1, app):
        # appends point to self.points and updates material used
        self.points.append((x1, y1))
        if len(self.points) >= 2:
            x0, y0 = self.points[-2]
            v = Vector.fromPoints((x0, y0), (x1, y1))
            material = Vector.magnitude(v)
            app.materialLimit -= int(math.floor(material))

    def draw(self):
        i = 0
        while i < len(self.points):
            if i > 0:
                # set color based on scribble ability or whether it's active
                if not self.active:
                    color = "lightGray"
                else:
                    color = self.colorFromAbility(self.ability)

                # draw line from current and previous point if in range
                x, y = self.points[i][0], self.points[i][1]
                previousX, previousY = self.points[i-1][0], self.points[i-1][1]
                drawLine(previousX, previousY, x, y, fill=color, lineWidth=10)
            i += 1

    # returns the right color for the right special line type
    @staticmethod
    def colorFromAbility(ability):
        if ability == "slippery":
            return "powderBlue"
        elif ability == "speedy":
            return "paleGreen"
        elif ability == "springy":
            return "orchid"

    '''
    This is a sidescrolling game, and the self.sidescroll method allows the line
    to be shifted by a variable amount each step. To improve performance,
    individual points of scribbles are deleted after leaving the viewport for
    100 pixels. Empty scribble classes are never deleted to preserve index.
    '''

    def sidescroll(self, scribbles, scribbleIndex, shiftFactor):
        # loop through points to shift or delete
        i = 0
        while i < len(self.points):
            x, y = self.points[i][0], self.points[i][1]
            self.points[i] = (x-shiftFactor, y)

            # removes point from self.points once safely off screen
            if x < -100:
                self.points.pop(i)
            i += 1

    '''
    self.checkRoll method takes the center of the player and loops through all
    the lines part of the scribble to find the the segment closest to the player
    center. Then the player's fields are changed to indicate it's rolling on the
    curve starting from that closest point on that segment until it exits.
    '''

    def checkRoll(self, player, scribbleIndex):
        # checks that scribble has never been interacted with by player
        # checks whether player is already rolling on a scribble
        if self.active and player.scribbleIndex != scribbleIndex:
            point = (player.x, player.y)

            # loop through all segments using points
            i = 0
            while i < len(self.points):
                if i > 0:
                    x, y = self.points[i][0], self.points[i][1]
                    previousX, previousY = self.points[i-1][0], self.points[i-1][1]
                    start = (previousX, previousY)
                    end = (x, y)

                    # gets shortest distance and closest point using helper
                    dist, rollPoint = distanceFromPointToSegment(point, start, end)

                    # only interact with line if shortest distance is <= radius
                    if dist <= player.r:
                        # checks if the player continues on current trajectory
                        # it will get closer to the path and is not moving away
                        nextX, nextY = player.x + player.dx, player.y + player.dy
                        nextPoint = (nextX, nextY)
                        nextDist = Vector.distance(nextPoint, rollPoint)
                        if nextDist < dist:
                            # sets player position to closest point for springy
                            if self.ability == "springy":
                                player.originalX, player.originalY = player.x, player.y
                                player.x, player.y = rollPoint
                            
                            # gets player rolling on scribble at current line
                            # starts friction off
                            player.scribbleIndex = scribbleIndex
                            player.lineIndex = i
                i += 1