### MODULES ####################################################################
from cmu_graphics import*
from vectors import*

from PIL import Image
import random, os, pathlib
################################################################################

'''
Enemy class is for Waddle Dees and Waddle Doos in the game. Waddle Doos track
the player with basic math ("AI targeting") and damage the player when they hit.
Waddle Dees move in a flying motion and follow normal parabolic physics, and
when the player hits them, the Waddle Dee dies and increases the points tally.
Both spawn with the same function just with a different parameter value.
'''

def enemySpawn(app, destructive):
    # spawns off screen
    randomY = random.randrange(50, app.height-150)
    newEnemy = Enemy(app.width + 50, randomY, destructive)
    app.enemies.append(newEnemy)

class Enemy:
    def __init__(self, x, y, destructive):
        self.r = 50
        self.destructive = destructive
        self.forward = False

        self.x = x
        self.y = y
        self.startingHeight = y # for Waddle Dee flying motion

        # if destructive enemy then it's a Waddle Doo
        if destructive:
            self.dx = 0
            self.dy = 0
            self.ddx = 0
            self.ddy = 0
        # if it's not then it's a Waddle Dee
        else:
            self.dx = -2
            self.dy = 0
            self.ddx = 0
            self.ddy = 0.1

    def draw(self, cmuImage):
        drawImage(cmuImage, self.x, self.y, align="center")

    def step(self, playerPoint, stepCount):
        # Waddle Doos move towards the player
        if self.destructive:
            # flip the image if going backwards
            if self.dx < 0 and self.forward:
                self.forward = not self.forward
            elif self.dx >=0 and not self.forward:
                self.forward = not self.forward

            # only change vector every 10 steps to make the enemy easier to avoid
            if stepCount % 50 == 0:
                v = Vector.fromPoints((self.x, self.y), playerPoint)
                v = Vector.unitize(v)
                v = Vector.scale(v, 3)
                self.dx = v[0]
                self.dy = v[1]

            self.x += self.dx
            self.y += self.dy
            self.dx += self.ddx
            self.dy += self.ddy
        # Waddle Dees move in a flying motion with normal physics
        else:
            self.x += self.dx
            self.y += self.dy
            self.dx += self.ddx
            self.dy += self.ddy
            
            # gives the flying motion with dampening
            if abs(self.y - self.startingHeight) > 150:
                self.dy += -2

    def despawn(self, app, enemyIndex, playerPoint):
        # die if go off screen for too long
        if self.x < -30:
            app.enemies.pop(enemyIndex)

        if self.destructive:
            # Waddle Doos hurt player if hit player
            enemyPoint = (self.x, self.y)
            if Vector.distance(playerPoint, enemyPoint) <= (self.r * 1.25):
                app.kirby.health -= 1
                app.enemies.pop(enemyIndex)
        else:
            # Waddle Dees die if hit by Player
            enemyPoint = (self.x, self.y)
            if Vector.distance(playerPoint, enemyPoint) <= (self.r * 1.25):
                app.enemies.pop(enemyIndex)
                app.pointTally += 1