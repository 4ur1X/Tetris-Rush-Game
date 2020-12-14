#------------------------------------------------------------------------------------------------------------------------------------------------------------------

#                                                        (:  TETRIS RUSH GAME (Processing & Python)  :)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------

import random     # importing random module

# dimensions of grid
WIDTH = 200
HEIGHT = 430    

checklist = [0,1,2,3,4,5,6,7,8,9] # top-most row (to check if all columns in that row have been occupied for game over)

ind = 0           # stores index value of currently visited cell

C, R = 10, 20     # number of columns and rows

S = WIDTH/C       # size of each cell in grid

filled = set()    # set for storing the index of grid cells that have been occupied or filled by blocks

game_speed = 0
score_counter = 0 # keeps track of score
game_over = False

# coordinates of starting cell for block
x = random.randrange(0, 200, 20)   # storing random starting x coordinate for the blocks with step value = 20 as each block is 20x20
y = -S       # initial 'y' of block

colors = [0] * (C)*(R+1)      # list storing the colors of each grid cell, updating letter in the program

# 2D list storing specific colors as mentioned in pdf
clr = [[225, 51, 52],   # RED
       [12, 150, 228],  # BLUE
       [30, 183, 66],   # GREEN
       [246, 187, 0],   # YELLOW
       [76, 0, 153],    # PURPLE
       [255, 255, 255], # WHITE
       [0, 0, 0]]       # BLACK

random_block_color = random.randint(0, len(clr)-1)       # choosing a random list of color from the 'clr' 2D list
col = color(clr[random_block_color][0],clr[random_block_color][1],clr[random_block_color][2])    # storing randomly chosen color

#------------------------------------------------------------------------------------------------------------------------------------------------------------------

# a class for controlling overall game functionalities
class Game:
    
    def __init__(self):
        self.checklist = [0,1,2,3,4,5,6,7,8,9]   # top-most row (to check if all columns in that row have been filled for game over)
        
    def score(self):
        global score_counter
        textSize(15)
        text("SCORE: "+str(score_counter),125,16)
        textSize(16)
        text("T E T R I S  R U S H",27,422)
        
    # method to make and update grid    
    def Grid(self):
        for i in range(C*R):     
            fill(colors[i] if i in filled else 210)     
            rect((i%C)*S, (i//C)*S, S, S)
                
    # method to detect game over and finish it
    def game_over_end(self):
        global game_over, filled, score_counter
        check =  all(item in filled for item in self.checklist)  # checking if all columns on top-most row has been filled (by comparing checklist and filled lists)
        if check == True:           # if all columns filled
            game_over = True
            fill(255,0,0)
            ellipse(100, 197, 180, 180)
            fill(255,255,255)
            textSize(26)
            text("GAME OVER", 26, 190)
            textSize(20)
            text("Score: "+str(score_counter), 60, 221)
            textSize(15)
            text("Click to Restart!", 45, 250)
            noLoop()
            loop()
            
            # when mouse button clicked, it restarts the game from starting
            if mousePressed and (mouseButton == LEFT):
                loop()
                redraw()
            
                # resetting variables
                global game_speed, colors, y, x, filled
                game_speed = 0                     # resetting game speed
                score_counter = 0
                filled.clear()                     # resetting settled down blocks
                colors2 = [] + colors              # copying original 'colors' list
                del colors2[:]                     # resetting original 'colors' list
                x = random.randrange(0, 200, 20)   # storing random starting x coordinate for the blocks
                y = -S                             # resetting 'y' position
                game_over = False
             
    # method for restarting game when mouse clicked   
    def clicked(self):
        global game_speed, filled, colors, y, x
        game_speed = 0           # resetting game speed
        score_counter = 0
        filled.clear()           # resetting settled down blocks
        colors2 = [] + colors    # copying original 'colors' list
        del colors2[:]           # resetting 'colors' list
        x = random.randrange(0, 200, 20)   # storing random starting 'x' coordinate for the blocks with step value = 20 as each block is 20x20 
        y = -S                   # resetting 'y' position
        setup()
        draw()  

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

# class for block related operations
class Block:
    
    def __init__(self):
        self.index_cell_below = 0      # initializing variable that stores index of cell present below
        self.remove_blocks = set()         # set for storing removed blocks (stack of 4)
        self.patterns = (set(range(1,4)), set(range(C, C*4, C)))  # stores sets of distances i.e. patterns
        self.dir = (-C, C)   # direction for checking adjacent ones vertical
        
    # method to check 4 consecutive blocks vertically and remove them    
    def stack(self, ind, v):           
        global colors
        v.append(ind)
        
        for d in self.dir:
        
            if 0<=ind+d<C*R and ind+d not in v:
                if colors[ind+d] == col:
                    self.stack(ind+d, v)    
        return v

    # method for controlling and moving blocks down   
    def block_moves(self):
        global y, col, x, filled, game_speed, score_counter, ind
        if(frameCount%(max(1, int(8 - game_speed)))==0 or frameCount==1):
            ind = (x//S)+(y//S)*C                     # storing coordinates of currently visited cell
            self.index_cell_below = ind+C             # index of cell present below
            if self.index_cell_below not in filled and self.index_cell_below<C*R:   # if NO occupied cell below
                if y < HEIGHT-S:                      # if empty cell below is within grid
                    y+=S                              # incrementing 'y' position 
                    
            else:                                     # else (there is an occupied cell below)                                
                s = self.stack(ind, [])               # looking for cells with similar colors around
                self.remove_blocks = set()
                if len(s)>1:                          # if stack of same colors is found
                    for n in range(len(s)):           # checking if patterns can be found in it
                        i1 = s[n]
                        d = set(abs(i2-i1) for i2 in s[n:] if i1!=i2)
                        for p in self.patterns:
                            if p.issubset(d):
                                for x in p:
                                    self.remove_blocks.update([i1] + [x+i1])     # storing index of their cells in 'remove_blocks' set
                
                # after removing the 4 blocks
                if self.remove_blocks:                                                
                    filled -= self.remove_blocks      # removing the same color stacked blocks from 'filled'
                    game_speed = 0                # resetting the speed
                    score_counter+=1              # incrementing the score
                    for i in self.remove_blocks: 
                        colors[i] = 210           # making them appear default color again 
                        
                else:                             # NO pattern to remove
                    filled.add(ind)               # putting index of current cell in 'filled' set
                    colors[ind] = col             # storing current color to 'colors' list
                    
                x = random.randrange(0, 200, 20)  # storing random starting 'x' coordinate for the blocks with step value = 20 as each block is 20x20
                random_block_color = random.randint(0, len(clr)-1)    # choosing a random list of color from the 'clr' 2D list
                col = color(clr[random_block_color][0],clr[random_block_color][1],clr[random_block_color][2])   # storing randomly chosen color
                game.Grid()                       # updating and printing the grid
                y = -S                            # resetting 'y' position
                game_speed+=0.25

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

block = Block()
game = Game()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------

def setup():
    size(WIDTH, HEIGHT)
    stroke(180)
    strokeWeight(1.3)
    game.Grid()   # function that creates a grid showing both 'filled' and 'empty' cells

def draw():
    global y, col, x, filled, game_speed, score_counter

    game.Grid()     # displaying the grid
    
    fill(col)       # color block
    rect(x,y,S,S)   # making the square block

    
    # calling the methods
    block.block_moves()
    game.game_over_end()
    fill(0,0,0)     # font color for score display i.e. black
    game.score()    # function to display and update score
    
# long press of key makes the block move as long as it's pressed
def keyPressed():
    global x, y
    if keyCode == RIGHT: 
        x+=S       # move RIGHT
    elif keyCode == LEFT: 
        x-=S       # move LEFT
    
    # to ensure that 'x' and 'y' coordinates stay within the limits of the grid  
    x = constrain(x, 0, WIDTH-S)
    y = constrain(y, 0, HEIGHT-S)

# to restart when mouse is clicked anytime during the game
def mouseClicked():
    check =  all(item in filled for item in checklist)  # checking if all columns on top-most row have been filled (by comparing 'checklist' and 'filled' lists)
    if check == True:
        game.clicked()
    
 #-------------------------------------------------------------------- END OF PROGRAM------------------------------------------------------------------------------   
