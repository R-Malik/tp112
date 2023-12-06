### MODULES ####################################################################
from cmu_graphics import*

from player import*
from scribbles import*
from enemy import*
from crystal import*

from PIL import Image
import os, pathlib
################################################################################

'''
main.py contains all the standard cmu_graphics functions and handlers. It
also has relevant helper functions in close proximity to the type of handler or
function they assist.
'''

### START/STOP/RESET ###########################################################
def onAppStart(app):
    app.width, app.height = 900, 600
    app.stepsPerSecond = 150
    reset(app)
    app.paused = True
    storeImages(app) # increases efficiency of loading images

def reset(app):
    app.kirby = Player(100, 100)
    app.crayon = Crayon(0, 0, "slippery")
    app.scribbles = []
    app.enemies = []
    app.crystals = []

    app.pointTally = 0 # number of Waddle Dees killed
    app.materialLimit = 10000 # arbitrary material starting amount

    app.isDrawing = False
    app.currentScribbleIndex = 0
    app.ability = "slippery"

    app.stepCount = 50
    app.spawnLimit = 250 # arbitrary number to mod stepCount by

    app.paused = False
    app.gameOver = False
    app.refreshScores = True

    refreshHighScores(app)

def storeImages(app):
    # health heart icon image
    heartImage = Image.open("assets/heart.png")
    heartImage = heartImage.resize((40, 40))
    app.heartImage = CMUImage(heartImage)

    # waddle dee image for score tally
    scoreImage = Image.open("assets/waddle_dee_wings.png")
    scoreImage = scoreImage.resize((80, 80))
    app.scoreImage = CMUImage(scoreImage)

    # waddle dee image for enemy
    deeImage = Image.open("assets/waddle_dee_wings.png")
    deeImage = deeImage.resize((100, 100))
    app.deeImage = CMUImage(deeImage)

    # waddle doo image for forward direction
    dooForwardsImage = Image.open("assets/waddle_doo.png")
    dooForwardsImage = dooForwardsImage.resize((80, 60))
    dooForwardsImage = dooForwardsImage.transpose(Image.FLIP_LEFT_RIGHT)
    app.dooForwardsImage = CMUImage(dooForwardsImage)

    # waddle doo image for backwards direction
    dooBackwardsImage = Image.open("assets/waddle_doo.png")
    dooBackwardsImage = dooBackwardsImage.resize((90, 70))
    app.dooBackwardsImage = CMUImage(dooBackwardsImage)

def refreshHighScores(app):
    # read and convert text file to sorted high scores list
    with open("highscores.txt", "r") as file:
        scoresString = file.read()
    scoreList = []
    for score in scoresString.splitlines():
        scoreList.append(int(score))
    # add new high score if it's greater than the minimum
    if app.pointTally > min(scoreList):
        scoreList.pop()
        scoreList.append(app.pointTally)
    scoreList.sort(reverse=True)
    app.highScores = scoreList
    # write to text file afterward
    scoresString = ""
    for score in app.highScores:
        scoresString += str(score)+"\n"
    with open("highscores.txt", "w") as file:
        file.write(scoresString)
################################################################################

### KEYBOARD HANDLERS ##########################################################
def onKeyPress(app, key):
    if key == "r":
        reset(app)
    if key == "1":
        app.isDrawing = False
        app.ability = "slippery"
        app.crayon.changeColor("slippery")
    elif key == "2":
        app.isDrawing = False
        app.ability = "speedy"
        app.crayon.changeColor("speedy")
    elif key == "3":
        app.isDrawing = False
        app.ability = "springy"
        app.crayon.changeColor("springy")
################################################################################

### MOUSE HANDLERS #############################################################
def onMouseMove(app, mouseX, mouseY):
    app.crayon.x = mouseX
    app.crayon.y = mouseY

    # hover over pause/help button
    pauseButtonHovering = False
    pausePosX, pausePosY = (25, 25)
    pauseSizeX, pauseSizeY = (120, 50)
    if pausePosX <= mouseX <= pausePosX + pauseSizeX:
        if pausePosY <= mouseY <= pausePosY + pauseSizeY:
            pauseButtonHovering = True
    app.crayon.opacity = 0 if pauseButtonHovering else 100

def onMousePress(app, mouseX, mouseY):
    # appends new scribble to app list of scribbles
    app.isDrawing = True
    app.scribbles.append(Scribble(app.ability))

    # click the pause/help button
    pausePosX, pausePosY = (25, 25)
    pauseSizeX, pauseSizeY = (120, 50)
    if pausePosX <= mouseX <= pausePosX + pauseSizeX:
        if pausePosY <= mouseY <= pausePosY + pauseSizeY:
            app.paused = not app.paused

def onMouseDrag(app, mouseX, mouseY):
    if not app.paused and not app.gameOver:
        app.crayon.x = mouseX
        app.crayon.y = mouseY
        if app.isDrawing:
            # adds a point to the current scribble every frame
            if app.currentScribbleIndex < len(app.scribbles):
                app.scribbles[app.currentScribbleIndex].addPoint(mouseX, mouseY, app)

def onMouseRelease(app, mouseX, mouseY):
    # stop drawing and increment scribble index
    app.isDrawing = False
    app.currentScribbleIndex += 1
################################################################################

### EVENT LOOP #################################################################
def onStep(app):
    if app.materialLimit <= 0:
        app.materialLimit = 0
        app.crayon.opacity = 0
        app.gameOver = True
        if app.refreshScores:
            refreshHighScores(app)
            app.refreshScores = False
    if app.kirby.health <= 0:
        app.crayon.opacity = 0
        app.gameOver = True
        if app.refreshScores:
            refreshHighScores(app)
            app.refreshScores = False
    if not app.paused and not app.gameOver:
        app.kirby.step(app)

        # sidescroll and checkroll all scribbles in loop
        i = 0
        while i < len(app.scribbles):
            app.scribbles[i].checkRoll(app.kirby, i)
            app.scribbles[i].sidescroll(app.scribbles, i, 2)
            i += 1
       
        i = 0
        # step and appropriately despawn enemies in loop
        waddleDeeCount, waddleDooCount = 0, 0
        while i < len(app.enemies):
            playerPoint = (app.kirby.x, app.kirby.y)
            if app.enemies[i].destructive:
                waddleDooCount += 1
            else:
                waddleDeeCount += 1
            app.enemies[i].step(playerPoint, app.stepCount)
            app.enemies[i].despawn(app, i, playerPoint)
            i += 1

        i = 0
        # step and appropriately despawn crystals in loop
        while i < len(app.crystals):
            playerPoint = (app.kirby.x, app.kirby.y)
            app.crystals[i].step()
            app.crystals[i].despawn(app, i, playerPoint)
            i += 1

        # spawn enemies on different timer
        if app.stepCount % app.spawnLimit == 0:
            if waddleDeeCount < 3:
                enemySpawn(app, destructive=False)
            if waddleDooCount < 1:
                enemySpawn(app, destructive=True)
            if len(app.crystals) < 1:
                crystalSpawn(app)

        app.stepCount += 1
################################################################################

### DRAWING ####################################################################
def redrawAll(app):
    for scribble in app.scribbles:
        scribble.draw()
    app.kirby.draw()
    for enemy in app.enemies:
        if enemy.destructive:
            if enemy.forward:
                enemy.draw(app.dooForwardsImage)
            else:
                enemy.draw(app.dooBackwardsImage) # flipped
        else:
            enemy.draw(app.deeImage)
    for crystal in app.crystals:
        crystal.draw()

    app.crayon.draw()

    # helper functions for other interface elements
    drawToolbar(app)
    if app.gameOver:
        drawGameOverScreen(app)
    if app.paused:
        drawHelpScreen(app)

def drawToolbar(app):
    # pause/help button
    x, y = 25, 25
    drawRect(x, y, 120, 50, fill="pink", border="black", borderWidth=3)
    if app.paused:
        drawLabel("PLAY", x+60, y+25, size=24, font="Comic Sans MS Bold")
    else:
        drawLabel("MENU", x+60, y+25, size=24, font="Comic Sans MS Bold")

    # health hearts
    x, y = 140, 25
    for i in range(1, 4):
        if i <= app.kirby.health:
            drawImage(app.heartImage, x+50*i, y+25, align="center")
        else:
            drawImage(app.heartImage, x+50*i, y+25, opacity=25, align="center")

    # waddle dee kill total
    x, y = app.width - 125, 25
    drawRect(x, y, 100, 50, fill="orange", border="black", borderWidth=3)
    drawImage(app.scoreImage, x, y+25, align="center")
    drawLabel(f"{app.pointTally}", x+60, y+25, size=24, font="Comic Sans MS Bold")

    # crayon material total
    x, y = app.width - 305, 25
    color = Scribble.colorFromAbility(app.ability)
    drawRect(x, y, 120, 50, fill=color, border="black", borderWidth=3)
    drawImage(app.crayon.image, x, y+25, align="center", rotateAngle=30)
    roundedTotal = math.floor(app.materialLimit/50) * 10
    drawLabel(f"{roundedTotal}", x+65, y+25, size=24, font="Comic Sans MS Bold")

def drawHelpScreen(app):
    # draw border box
    x, y = app.width/2, 120
    drawRect(x, y, 700, 360, fill="lightSalmon", border="black", borderWidth=3, align="top")

    helpInstructions = [
    "Click and drag with your mouse/trackpad to draw",
    "Press '1, 2, 3' to switch between the crayon ability", "",
    "Bump into Waddle Dees (orange) and you gain points",
    "Run into Waddle Doos (red) and you lose a heart",
    "Run out of crayon material or lose all 3 hearts and you die", "",
    "Press 'R' anytime to restart"]

    # draw the instructions
    drawLabel("INSTRUCTIONS", x, y+50, size=36, font="Comic Sans MS Bold")
    for i in range(len(helpInstructions)):
        drawLabel(helpInstructions[i], x, y+100+(i*30), size=20, font="Comic Sans MS Bold")

def drawGameOverScreen(app):
    # draw border box for game over message
    x, y = app.width/2, 120
    drawRect(x, y, 400, 180, fill="mediumTurquoise", border="black", borderWidth=3, align="top")

    # draw the instructions and end score
    drawLabel("GAME OVER", x, y+50, size=36, font="Comic Sans MS Bold")
    drawLabel("PRESS 'R' TO RESTART", x, y+100, size=20, font="Comic Sans MS Bold")
    drawLabel(f"YOUR SCORE: {app.pointTally}", x, y+130, size=20, font="Comic Sans MS Bold")

    # draw border box for high scores
    x, y = app.width/2, y+200
    drawRect(x, y, 400, 215, fill="hotPink", border="black", borderWidth=3, align="top")

    # draw the high scores
    drawLabel(f"HIGHSCORES", x, y+35, size=20, font="Comic Sans MS Bold")
    for i in range(len(app.highScores)):
        score = str(app.highScores[i])
        zeroFactor = 5 - len(score)
        score = "0"*zeroFactor + score
        drawLabel(score, x, y+70+25*i, size=20, font="Comic Sans MS Bold")
################################################################################

runApp()