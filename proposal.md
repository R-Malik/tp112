# Project Proposal

### TP3 Update

After MVP, I added the "AI" tracking enemies called Waddle Doos, 3 health hearts for Kirby, and material crystals Kirby can collect to increase your material limit. Now the game is officially an "infinite" game of sorts. There's also a file read/write system for persisting high scores over app termination. All of this is better communicated in the UI.

### TP2 Update

With TP2 done, I've thought about adding more win/lose conditions to the game. Specifically, I'm thinking of adding enemies you want to avoid rather than kill called Waddle Doos. Hitting one will decrement Kirby's health bar until it's game over. They will also have some "AI" to target Kirby for added algorithmic complexity.

### TP1 Update

When coding up TP1, I've thought about turning Kirby into a skater so that he can grind rails instead of just ride on top of scribbles. This means he can bounce off the edges of the screen onto rails above him. I'll decide whether he should rotate or be shifted above or below the rail later. I'm also thinking of having scribbles disappear with some magical animation after they are used. Right now, the working title will be **Kirby and the Crystal Crayon**. Sprites for Kirby, the crystal crayon, and more will be added later.

OOP is on the rise. I've put all the vector functions in their own class, Vector, to kind of use it like a custom module.

### Project Description

Kirby and the Canvas Quest will be a drawing-based, platformer/physics game. Basically, you strategically draw lines or paths using different materials and have Kirby roll across them to smash into Waddle Dees in order to reach King Dedede and save the kingdom. You can draw paths before and after you get Kirby rolling, and every level will have progressively more obstacles thrown onto the canvas. The three materials you can draw with will be slippery (make Kirby slide across), springy (make Kirby bounce), and speedy (make Kirby faster).

### Similar Projects

Originally, I had a vague idea of having some drawing game where the stuff you draw interacted with a character using real physics. After ideating with Mike, I decided to base this game off some Kirby games and Line Rider. Specifically, Kirby: Canvas Curse and Kirby and the Rainbow Curse inspired the characters (Kirby and King Dedede) and inspired putting enemies (Waddle Dees) in the game for Kirby to destroy. Line Rider, which actually has been done as a 112 project before, inspired more of the open-ended nature of the game. There will be enemies, added obstacles, and powerups in the form of different material physics, but the Canvas will still be mostly a blank slate for Kirby to solve puzzles and optimize Waddle Dee destruction. Unlike Line Rider, there is a win condition, which is getting past all the levels. This project will hopefully strike a balance between the Kirby classics and Line Rider.

### Algorithmic Plan

I think the trickiest part of the project will be the physics. That can be subdivided into horizontal/vertical velocity and acceleration, collision, and special materials. 

For horizontal/vertical velocity and acceleration, I was thinking of storing those as fields in the class called Player and have a method that updates them based on a parameter, time since last update, and the self.dx and self.ddx values. 

For collision, I was thinking of having a class called `LineGroup` and have fields for a list of joined lines (which have a start x,y and end x,y). The `LineGroup` would also have a self.borderwidth and self.material for the different materials and their properties. `LineGroup` will also have a method that changes Kirby’s acceleration if Kirby is in contact with it. All these “updater” methods will be called on all objects every step in cmu graphics.

For special materials, `LineGroup` will have self.elasticity properties and self.speed fields that magnify the effect of Kirby’s changes in x, y acceleration. Elasticity will be 0 for all materials except “springy” and self.speed will be 0 for all materials except “speedy.”

### Structural Plan

There will likely be three files for MVP of this project, and then more as I add story frames, game instructions, victory screens etc. 

One file will be for the `Player` and `Enemy` classes and their respective methods. The `Player` class will notably have image, x, y, dx, dy, ddx, ddy, and rotateAngle fields—and updatePosition method. The `Enemy` class will be very similar to `Player` depending on whether a Waddle Dee is statically flying or interacting with the platforms and bouncing. 

Another file will be for the `LineGroup` class and its respective methods. It will notably have lines list, material, elasticity, speedness, and stickiness fields—and a method like isTouchingPlayer that takes a Player and changes its acceleration accordingly depending on the severity of the collision and material type.

Another file will be for all the cmu graphics functions, onAppStart, redrawAll, onStep, onMousePress, onKeyPress, etc. It’s going to be important later to make redrawAll clean, so I’ll have methods like drawYourself for the classes themselves.

### Timeline Plan

By TP1, I hope to have the basics down: physics and drawing. I’ll start with a simple ball as a Player class rolling on a straight line (LineGroup) with normal gravity and collision physics. Then, I’ll make the lines drawable by me, add elasticity, rotation for the Player, and work up from there.

By TP2, I hope to have a roughly playable game and will start working on streamlining the user experience and adding finer details like dampening to the physics. I’ll also start making some levels and incorporating enemies as puzzles. A final boss fight might be a possibility.

By TP3, I hope to have a really polished game with a story sequence, visible controls, music, and victory screens. I’ll also have a few of my friends play it and give me feedback.

### Version Control Plan

Code will be backed up with git on local repository and routinely pushed to GitHub. Code will be committed and pushed daily and after finishing features. Above is an image of some example files for the project in VSC and the files pushed a few seconds later on the new GitHub repository: `R-Malik/tp112`

### Module List

No external modules will be used.

