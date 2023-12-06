### MODULES ####################################################################
from cmu_graphics import*

from vectors import*

from PIL import Image
import random, os, pathlib
################################################################################

'''
Crystal class is for material crystals that spawn on screen that a player can
collect when they hit the crystal to increase their material limit. This is
what makes the game an "infinite" game.
'''

def crystalSpawn(app):
    randomY = random.randrange(50, app.height-150)
    newCrystal = Crystal(app.width + 50, randomY, app.crayon.ability)
    app.crystals.append(newCrystal)

class Crystal():
    def __init__(self, x, y, ability):
        self.r = 50

        self.x = x
        self.y = y
        self.dx = -3
        self.dy = 0
        self.ddx = 0
        self.ddy = 0 # no gravity so it moves linearly

        self.changeColor(ability) # uses method to change image

    def draw(self):
        drawImage(self.image, self.x, self.y, align="center", rotateAngle=30)

    def changeColor(self, ability):
        # changes color of the crayon and ability based on parameter
        self.ability = ability
        if ability == "slippery":
            tempImage = Image.open("assets/crystal_blue.png")
            tempImage = tempImage.resize((40, 80))
            self.image = CMUImage(tempImage)
        elif ability == "speedy":
            tempImage = Image.open("assets/crystal_green.png")
            tempImage = tempImage.resize((40, 80))
            self.image = CMUImage(tempImage)
        elif ability == "springy":
            tempImage = Image.open("assets/crystal_purple.png")
            tempImage = tempImage.resize((40, 80))
            self.image = CMUImage(tempImage)

    def step(self):
        # normal physics
        self.x += self.dx
        self.y += self.dy
        self.dx += self.ddx
        self.dy += self.ddy

    def despawn(self, app, crystalIndex, playerPoint):
        # remove if go off screen for too long
        if self.x < -30:
            app.crystals.pop(crystalIndex)

        # increase material limit if hit by Player
        crystalPoint = (self.x, self.y)
        if Vector.distance(playerPoint, crystalPoint) <= (self.r * 1.5):
            app.crystals.pop(crystalIndex)
            app.materialLimit += 250