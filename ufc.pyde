add_library('minim')
import os
import random
import time
from collections import OrderedDict
choice1 = 0 #global variable for player 1 character selection
choice2 = 0 #global variable for player 2 character selection
path=os.getcwd()
hit1=False #global variable for player 1 hitting
hit2=False #global variable for player 2 hitting
cnt1=1 #global variable for number of times player 1 hit
cnt2=1 #global variable for number of times player 2 hit
strike1 = 0 #global variable for total strikes of player 1
strike2= 0 #global variable for total strikes of player 2
message='' #global variable for name typing
game_time=60 #global variable for total game time
game_run=True #global variable for flag for restarting the game
class Fighter: #Class for the fighters 
    def __init__ (self,x,y,r,g,w,h,F,dir):
        self.x=x
        self.y=y
        self.r=r
        self.w=w
        self.h=h
        self.F=F #total frames
        self.vx=0
        self.vy=0
        self.g=g
        self.time = -1
        self.key_handler = {"left":False, "right":False, UP: False, DOWN: False}
        self.f=2 #instantaneous frames
        self.dir=dir
        self.state=0   #variable to decide which frame to display
        self.blackf= loadImage(path+ '/blackframes.png') #load images for all characters with different colors
        self.redf= loadImage(path+ '/redframes.png')
        self.greenf= loadImage(path+ '/greenframes.png')
        self.bluef= loadImage(path+ '/blueframes.png')
    def gravity(self): #method for gravity
        if self.y +self.r < self.g:
            self.vy += 0.5    
            if self.y+self.r+self.vy > self.g:
                self.vy = self.g-self.y-self.r
        else:
            self.vy = 0
        self.g=game.g
        
    def update(self): 
        if self.time > 0:       #decrease time for punching/kicking animation 
            self.time -= 1
        self.gravity()
        if self.key_handler['left']:
            self.vx=-5
            self.dir=-1
        elif self.key_handler['right']:
            self.vx=5
            self.dir=1
        else:
            self.vx=0
        if self.key_handler[UP] and self.y + self.r == self.g:
            self.vy = -10
            self.f=5
        if self.state==0:        #display walking frames
            if self.vx!= 0 and self.vy == 0:
                self.f=(self.f+0.2)%self.F
            else:
                self.f=0
        elif self.state==5:       #display jumping frame
            if self.vy != 0:
                self.f=4
            else:
                self.state= 0
        elif self.state==6:       #display punching frame
            if self.time >=0:
                self.vx=0
                self.f=5
        elif self.state==7:       #display kicking frame
            if self.time >= 0:
                self.vx=0
                self.f=6
        elif self.state==8:       #display blocking frame
            self.f=7
        elif self.state==9:       #display winning frame
            self.f=9
            self.vx = 0
            self.vy = 0
        elif self.state==10:      #display knocked out frame
            self.f=10
            self.vx = 0
            self.vy = 0
        self.x += self.vx 
        self.y += self.vy
         
    def display1(self): #display method of fighter 1
        global choice1,choice2,hit2
        self.update()
        if self.x <=5: #prevent moving off the screen
            self.x = 10
        elif self.x>=1150:
            self.x=1145
        if hit2 == True:   #knockback animation when fighter 1 gets hit
            self.f = 8          
            if game.fighter2.x < game.fighter1.x :   #setting knock back distance according to position 
                self.x += 5
            elif game.fighter2.x > game.fighter1.x:
                self.x -= 5
            hit2= False         #flag set to false to prevent infinite knock back animation
            if hit2 == False:   #displaying back to walking frames
                self.state=0  
        if self.dir >0:       #set frames according to direction and selected character
            if choice1 ==1 :
                image(self.blackf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,self.w*(int(self.f)+1),self.h)
            elif choice1 ==2:
                image(self.greenf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,self.w*(int(self.f)+1),self.h)
            elif choice1 ==3:
                image(self.redf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,self.w*(int(self.f)+1),self.h)
            elif choice1 ==4:
                image(self.bluef,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,self.w*(int(self.f)+1),self.h)
        elif self.dir < 0:
            if choice1 == 1:
                image(self.blackf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,self.w*(int(self.f)),self.h)
            elif choice1 == 2:
                image(self.greenf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,self.w*(int(self.f)),self.h)
            elif choice1 == 3:
                image(self.redf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,self.w*(int(self.f)),self.h)
            elif choice1 == 4:
                image(self.bluef,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,self.w*(int(self.f)),self.h)
 
    def display2(self): #display method of fighter 2
        global choice1, choice2,hit1
        self.update()
        if self.x <=5: #prevents moving off screen
            self.x = 10
        elif self.x>=1150:
            self.x=1145
        if hit1 == True: #knockback animation when hit
            self.f = 8
            if game.fighter2.x > game.fighter1.x :
                self.x += 5
            elif game.fighter2.x < game.fighter1.x:
                self.x -= 5
            hit1= False   
            if hit1 == False:
                self.state=0
        if self.dir >0:
            if choice2 ==1 :
                image(self.greenf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,self.w*(int(self.f)+1),self.h)
            elif choice2 ==2:
                image(self.blackf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,self.w*(int(self.f)+1),self.h)
            elif choice2 ==3:
                image(self.bluef,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,self.w*(int(self.f)+1),self.h)
            elif choice2 ==4:
                image(self.redf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f)*self.w,0,self.w*(int(self.f)+1),self.h)
        elif self.dir < 0:
            if choice2 == 1:
                image(self.greenf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,self.w*(int(self.f)),self.h)
            elif choice2 == 2:
                image(self.blackf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,self.w*(int(self.f)),self.h)
            elif choice2 == 3:
                image(self.bluef,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,self.w*(int(self.f)),self.h)
            elif choice2 == 4:
                image(self.redf,self.x-self.r,self.y-self.r,self.w,self.h,int(self.f+1)*self.w,0,self.w*(int(self.f)),self.h)

def keyPressed(): #keypressed for all the movements and attacks
    if game.stage == 2:    #main fighting phase of game
        global cnt1,cnt2,choice1,choice2,strike1,strike2,hit1,hit2,game_run,game_time
        if key == "a":     #set key handler for fighter actions
            game.fighter1.F=4
            game.fighter1.key_handler["left"] = True  
        elif key == "d":
            game.fighter1.F=4  
            game.fighter1.key_handler["right"] = True  
        elif key == "w":    #jumping
            game.fighter1.state=5
            game.fighter1.key_handler[UP] = True
        elif key == "c":   #punching
            if game.fighter1.time == -1: #timer to prevent punching for unlimited time
                game.fighter1.time = 30
                game.fighter1.state=6
            elif game.fighter1.time > 0:
                game.fighter1.state=6
            else:
                game.fighter1.state = 0
            game.punch.rewind()     #play punching sound everytime fighter punches
            game.punch.play()
        elif key == "v" :          #kicking    
            if game.fighter1.time == -1:   #timer to prevent kicking for unlimited time
                game.fighter1.time = 30
                game.fighter1.state=7
            elif game.fighter1.time > 0:
                game.fighter1.state=7
            else:
                game.fighter1.state = 0           
        elif key == "s":  #blocking
            game.fighter1.state=8
            game.fighter1.key_handler[DOWN] = True  
        elif keyCode == LEFT:
            game.fighter2.F=4  
            game.fighter2.key_handler["left"] = True  
        elif keyCode == RIGHT: 
            game.fighter2.F=4 
            game.fighter2.key_handler["right"] = True  
        elif keyCode == UP:  #jumping
            game.fighter2.state=5
            game.fighter2.key_handler[UP] = True
        elif key == "/":     #punching
            if game.fighter2.time == -1:
                game.fighter2.time = 30
                game.fighter2.state=6
            elif game.fighter2.time > 0:
                game.fighter2.state=6
            else:
                game.fighter2.state = 0  
        elif key == ".":      #kicking
            if game.fighter2.time == -1:
                game.fighter2.time = 30
                game.fighter2.state=7
            elif game.fighter2.time > 0:
                game.fighter2.state=7
            else:
                game.fighter2.state = 0 
        elif keyCode == DOWN:  #blocking
            game.fighter2.state=8
            game.fighter2.key_handler[DOWN] = True
    elif game.stage==5 or game.stage ==6:
        global message
        if keyCode == 8: #delete message when backspace pressed
            message = message[0: len(message)-2]
    elif game.stage == 3: #resetting all the variable of the game when game restarts
        if keyCode == 32:   #spacebar
            game_run=False   #flag for returning to main menu
            if game_run == False:    
                game.stage=1     #reset all global variables to original value
                game_time=60
                choice1=0
                choice2=0
                hit1=False
                hit2=False
                cnt1=1
                cnt2=1
                strike1 = 0
                strike2= 0
                message=''
                game.health1=[]
                game.health2=[]
                for i in range(0,10):   #reset health bars for both fighters
                    game.health1.append(game.health)
                    game.health2.append(game.health)
                game.fighter1.x = 400
                game.fighter2.x = 800
                game.fighter1.state = 0
                game.fighter2.state = 0
                game.fighter1.dir=1
                game.fighter2.dir=-1
                game.name=[]
                game.scores=[]
                game_run=True

def keyTyped(): #keytyped to add the names
    global message
    if game.stage == 5 or game.stage == 6:
        if len(message) <13:     #limit name length to 12 characters
            message += key
        message=message.strip('\n')
        
def keyReleased():  
    if key == "a":  
        game.fighter1.key_handler["left"] = False  
    elif key == "d":  
        game.fighter1.key_handler["right"] = False  
    elif key == "w":   
        game.fighter1.key_handler[UP] = False  
    elif key == "c":  
        game.fighter1.state=0
        game.fighter1.time = -1
    elif key == "v":  
        game.fighter1.state=0 
        game.fighter1.time=-1
    elif key == "s":  
        game.fighter1.state=0
        game.fighter1.key_handler[DOWN] = False 
    elif keyCode == LEFT:  
        game.fighter2.key_handler["left"] = False  
    elif keyCode == RIGHT:  
        game.fighter2.key_handler["right"] = False  
    elif keyCode == UP:  
        game.fighter2.key_handler[UP] = False  
    elif key == "/":  
        game.fighter2.state=0
        game.fighter2.time = -1
    elif key == ".":  
        game.fighter2.state=0
        game.fighter2.time = -1
    elif keyCode == DOWN:  
        game.fighter2.state=0
        game.fighter2.key_handler[DOWN] = False 
    if game.stage==5 or game.stage ==6 or game.stage==7:
        global message, game_time
        if keyCode == 8:   #backspace
            message = message[0: len(message)-1] #delete characters
        if keyCode == 10: #sorting the names according to score in the csv file when enter is pressed and released
            game.leaderboard[message]=int((60-game_time))   #add name and score to leaderboard dictionary
            for i in range(5):           #call method to sort dictionary
                game.sort_dict()
            count_scoreboard=0           #variable set to read top 5 lines in csv file
            game.file=open('leaderboard.csv','r')
            for line in game.file:
                xline = line.strip('').split(',')
                if count_scoreboard < 5:
                    game.name.append(xline[0])   #add name to name list
                    game.scores.append(xline[1]) #add score to score list
                count_scoreboard += 1    #keep track of number of line read
            game.file.close()
            game.stage = 3        #leaderboard stage
            game.crowd.pause()    #stop crowd sound
            
class Game: #class for the whole game
    def __init__(self,w,h,g):
        self.w=w
        self.h=h
        self.g=g
        self.bg1=loadImage(path+'/background.png')    #load backgrounds, fighter images, control images, health bar image, leaderboard image
        self.bg2=loadImage(path+'/wfog.png')
        self.menu=loadImage(path+'/menu.png')
        self.khabib=loadImage(path+'/khabib.png')
        self.mcgregor=loadImage(path+'/mcgregor.png')
        self.dustin=loadImage(path+'/poirier.png')
        self.justin=loadImage(path+'/gaethje.png')
        self.arrows=loadImage(path+'/arrows.png')
        self.d_arrow=loadImage(path+'/downarrow.png')
        self.wasd=loadImage(path+'/wasd.png')
        self.c_key=loadImage(path+'/c.png')
        self.v_key=loadImage(path+'/v.png')
        self.s_key=loadImage(path+'/s.png')
        self.period=loadImage(path+'/period.png')
        self.slash=loadImage(path+'/slash.png')
        self.health=loadImage(path+'/healthsquare.png')
        self.l_image=loadImage(path+'/leaderboard.png')
        self.fighter1 = Fighter(400, 0, 60, 0, 161, 271, 11,1)    #instantiate fighter object from figthter class
        self.fighter2 = Fighter(800, 150, 60, 0, 161,271,11,-1)
        self.stage=1     #set stage as main menu
        self.health1=[]  #list for health bar images
        self.health2=[]
        for i in range(0,10):    #add ten health bar images
            self.health1.append(self.health)
            self.health2.append(self.health)
        self.frames=0    
        self.crowd=minim.loadFile(path+'/crowdnoise.mp3')   #load crowd noise, punch noise, winning commentary
        self.punch=minim.loadFile(path+'/punch.mp3')
        self.itstime=minim.loadFile(path+'/itstime.mp3')
        self.p1=minim.loadFile(path+'/poirier1.mp3')
        self.p2=minim.loadFile(path+'/poirier2.mp3')
        self.p3=minim.loadFile(path+'/poirier3.mp3')
        self.k1=minim.loadFile(path+'/khabib1.mp3')
        self.k2=minim.loadFile(path+'/khabib2.mp3')
        self.k3=minim.loadFile(path+'/khabib3.mp3')
        self.g1=minim.loadFile(path+'/gaethje1.mp3')
        self.g2=minim.loadFile(path+'/gaethje2.mp3')
        self.c1=minim.loadFile(path+'/conormcgregor1.mp3')
        self.c2=minim.loadFile(path+'/conormcgregor2.mp3')
        self.mcgregor_audio=[self.c1,self.c2]      #add winning commentary audio for each fighter as a list
        self.khabib_audio = [self.k1, self.k2, self.k3]
        self.poirier_audio = [self.p1, self.p2, self.p3]
        self.gaethje_audio = [self.g1, self.g2]
        self.leaderboard = {}       #leaderboard dictionary to keep names and scores of players
        self.file=open('leaderboard.csv','a')    
        self.file.close()
        self.file= open('leaderboard.csv','r')
        for line in self.file:           #copy content in csv file to leaderboard dictionary when game runs
            line = line.strip().split(',')
            self.leaderboard[line[0]]=line[1]
        self.file.close()
        self.sorted_board = []     #list to contain 2-tuples of names and scores for sorting
        self.sorted_dict = {}      #dictionary to contain names sorted according to scores
        self.name = []
        self.scores= []
        
    def sort_dict(self): #method to sort dictionary containing name and time
        self.sorted_board = sorted(self.leaderboard.items(), key = lambda x:x[1])  #function from collections library to convert unsorted dictionary to sorted 2-tuples into a list
        if len(self.sorted_board)>5:     #make sure dictionary contains only top 5
            self.sorted_board=self.sorted_board[:5]
        self.sorted_dict = OrderedDict(self.sorted_board)    #function from collection class to convert sorted list into a sorted dictionary
        self.file=open('leaderboard.csv','w')
        for name in self.sorted_dict: 
            self.file.write('{0},{1}\n'.format(name,int(self.sorted_dict[name])))    #write content of dictionary into csv file
        self.file.close()

    def display_leaderboard(self): #method to show the names and times in the leaderboard
        x=0
        y=0
        textSize(40)
        for i in self.name:       
            text(i,475,175+x)
            x+=75
        for j in self.scores:
            stroke(255,255,255)
            text(j,765,175+y)
            y+=75

    def display(self): #display method for the whole game
        global game_time, hit1, hit2, cnt1, cnt2, strike1, strike2, choice1, choice2, message
        if self.stage == 1: #main menu stage with option to start game or check leaderboard
            image(self.menu,0,0,1217,510)
            textSize(50)
            if 270<mouseX<540 and 540<mouseY<585:
                fill(255,0,0)
            else :
                fill(255,255,255)
            text ('Start Game',270,580)
            if 700<mouseX<990 and 540<mouseY<590:
                fill(255,0,0)
            else:
                fill(255,255,255)
            text ('High Scores',700,580)
            fill(255,255,255)
        elif self.stage == 2: #game stage where fighters are diplayed and the 1 minute round starts
            self.frames=(self.frames+1)%60
            if self.frames == 0:
                game_time -=1
            image(self.bg1,0,0)
            self.fighter1.display1()
            self.fighter2.display2()
            fill(255,255,255)
            textSize(24)
            text('Time: '+str(game_time),10,50)
            self.collision()
            text("Player 1: ", 5, 85)
            text("Player 2: ", 980, 85)
            health_length1 = len(self.health1)
            for i in range (health_length1):  #display health bar images on screen
                image(self.health,0+i*25,100, 25, 25)
            health_length2 = len(self.health2)
            for i in range (health_length2):
                image(self.health,1192-i*25,100, 25, 25)
            if hit1== True and cnt1 ==0:
                self.health2.pop()        #remove one health bar image when enough damage inflicted
                hit1=False
            if hit2== True and cnt2==0:
                self.health1.pop()
                hit2=False
            text("Strikes: " + str(strike1), 10, 150)
            text("Strikes: " + str(strike2), 1050, 150)
            if  (health_length1 == 0) or (game_time ==0 and strike2>strike1):  #checking win conditions
                hit1=False   #change collision flags to false to prevent attacking after game ends
                hit2=False
                self.stage = 5 # p2 wins
                if choice2 == 1: #audio specific to fighter chosen plays after win
                    sound = random.choice(self.mcgregor_audio)
                    sound.rewind()
                    sound.play()
                if choice2 == 2:
                    sound = random.choice(self.khabib_audio)
                    sound.rewind()
                    sound.play()
                if choice2 == 3:
                    sound = random.choice(self.gaethje_audio)
                    sound.rewind()
                    sound.play()
                if choice2 == 4:
                    sound = random.choice(self.poirier_audio)
                    sound.rewind()
                    sound.play()
            elif (health_length2 == 0) or (game_time == 0 and strike1>strike2):
                self.stage = 6 # p1 wins
                if choice1 == 1:
                    sound = random.choice(self.khabib_audio)
                    sound.rewind()
                    sound.play()
                if choice1 == 2:
                    sound = random.choice(self.mcgregor_audio)
                    sound.rewind()
                    sound.play()
                if choice1 == 3:
                    sound = random.choice(self.poirier_audio)
                    sound.rewind()
                    sound.play()
                if choice1 == 4:
                    sound = random.choice(self.gaethje_audio)
                    sound.rewind()
                    sound.play()
            elif strike1 == strike2 and game_time == 0:
                self.stage=7 #draw stage
        elif self.stage ==3: #leaderboard stage
            image(self.l_image,350,25,500,500)
            textSize(25)
            text('Time(s)',745,110)
            text('Press Spacebar to Return to Main Menu',360,550)
            self.display_leaderboard()
        elif self.stage ==4: #character selection stage
            image(self.bg2,0,0,1217,610)
            image(self.khabib,0,0,200,200)
            image(self.mcgregor,205,0,200,200)
            image(self.dustin,0,205,200,200)
            image(self.justin,205,205,200,200)
            image(self.khabib,812,0,200,200)
            image(self.mcgregor,1017,0,200,200)
            image(self.dustin,812,205,200,200)
            image(self.justin,1017,205,200,200)
            image(self.wasd,450,10,150,150)
            image(self.arrows,650,10,150,150)
            image(self.s_key,450,180,50,50)
            image(self.c_key,450,240,50,50)
            image(self.v_key,450,310,50,50)
            image(self.d_arrow,750,180,50,50)
            image(self.slash,750,240,50,50)
            image(self.period,750,310,50,50)
            textSize(35)
            text('Block',575,220)
            text('Punch',570,280)
            text('Kick',585,350)
            noFill()
            if (0<mouseX<200 and 0<mouseY<200):
                stroke(255,0,0)
            else:
                stroke(255,255,255)
            if choice1 == 1:
                stroke(255,0,0)
            rect(0,0,200,200,7)
            if (205<mouseX<405 and 0<mouseY<200):
                stroke(255,0,0)
            else:
                stroke(255,255,255)
            if choice1 == 2:
                stroke(255,0,0)
            rect(205,0,200,200,7)
            if (0<mouseX<200 and 205<mouseY<405):
                stroke(255,0,0)
            else:
                stroke(255,255,255)
            if choice1 == 3:
                stroke(255,0,0)
            rect(0,205,200,200,7)
            if (200<mouseX<400 and 200<mouseY<400):
                stroke(255,0,0)
            else:
                stroke(255,255,255)
            if choice1 == 4:
                stroke(255,0,0)
            rect(205,205,200,200,7)
            if (1017<mouseX<1217 and 0<mouseY<200):
                stroke(255,0,0)
            else:
                stroke(255,255,255)
            if choice2 == 1:
                stroke(255,0,0)
            rect(1017,0,200,200,7)
            if (812<mouseX<1012 and 0<mouseY<200):
                stroke(255,0,0)
            else:
                stroke(255,255,255)
            if choice2 == 2:
                stroke(255,0,0)
            rect(812,0,200,200,7)
            if (1017<mouseX<1217 and 205<mouseY<405):
                stroke(255,0,0)
            else:
                stroke(255,255,255)
            if choice2 == 3:
                stroke(255,0,0)
            rect(1017,205,200,200,7)
            if (812<mouseX<1012 and 200<mouseY<400):
                stroke(255,0,0)
            else:
                stroke(255,255,255)
            if choice2 == 4:
                stroke(255,0,0)
            rect(812,205,200,200,7)
        elif self.stage == 5 : #p2 winning stage
            self.crowd.pause()
            image(self.bg1,0,0)
            self.fighter1.state=10  #display knocked out frame for p1
            self.fighter2.state=9   #display victory frame for p2
            self.fighter1.display1()
            self.fighter2.display2()
            text('Player 2 wins! Enter your name:',450,100) 
            text(message, 450, 150)
        elif self.stage == 6: #p1 winning stage
            self.crowd.pause()
            image(self.bg1,0,0)
            self.fighter1.state=9   #display victory frame for p1
            self.fighter2.state=10  #display knocked out frame for p2
            self.fighter1.display1()
            self.fighter2.display2()
            text('Player 1 wins! Enter your name:',450,100) 
            text(message, 450, 150)     #display name typed by player on screen
        elif self.stage == 7: #draw stage
            image(self.bg1,0,0)
            text('Its a tie! Boring.',400,100)
            text('Press Enter to go to the leaderboard.',400,150)
            self.fighter1.state=0  #display walking frame for both fighters
            self.fighter2.state=0
            self.fighter1.display1()
            self.fighter2.display2()

    def collision(self): #method to check for collisions
        global hit1, hit2, cnt1, cnt2, strike1, strike2
        if (self.fighter1.state==6 or self.fighter1.state==7) and (self.fighter2.state != 8) and ((self.fighter1.x-self.fighter2.x)**2+(self.fighter1.y-self.fighter2.y)**2)**0.5 <= (self.fighter1.r+self.fighter2.r):   
            if self.fighter1.x < self.fighter2.x: #check if fighter1 hit fighter2, fighter2 is not blocking, and the directions are proper
                if self.fighter1.dir>0 and self.fighter2.dir>0:
                    hit1 = True
                    strike1 +=.1   #increment strike points by 0.1
                    cnt1=(cnt1+1)%20  #keep track of total strikes
                if self.fighter1.dir < 0 and self.fighter2.dir < 0:  #check unmatching directions(ex. when next to each other but facing opposite directions --> punch not counted)
                    hit1 = False
                if self.fighter1.dir >0 and self.fighter2.dir < 0:
                    hit1 = True
                    strike1 +=.1
                    cnt1=(cnt1+1)%20
                if self.fighter1.dir < 0 and self.fighter2.dir>0:
                    hit1 = False
            if self.fighter1.x > self.fighter2.x:
                if self.fighter1.dir>0 and self.fighter2.dir>0:
                    hit1 = False
                if self.fighter1.dir < 0 and self.fighter2.dir < 0:
                    hit1= True
                    strike1 +=.1
                    cnt1=(cnt1+1)%20
                if self.fighter1.dir >0 and self.fighter2.dir < 0:
                    hit1 = False
                if self.fighter1.dir < 0 and self.fighter2.dir>0:
                    hit1 = True
                    strike1 +=.1
                    cnt1=(cnt1+1)%20
        if (self.fighter2.state==6 or self.fighter2.state==7) and (self.fighter1.state != 8) and ((self.fighter1.x-self.fighter2.x)**2+(self.fighter1.y-self.fighter2.y)**2)**0.5 <= (self.fighter1.r+self.fighter2.r): 
            if self.fighter2.x < self.fighter1.x: #check if fighter2 hit fighter1
                if self.fighter2.dir>0 and self.fighter1.dir>0: #check if fighter2 hit fighter1, fighter1 is not blocking, and the directions are proper
                    hit2 = True
                    strike2 +=.1
                    cnt2=(cnt2+1)%20
                if self.fighter2.dir < 0 and self.fighter1.dir < 0:
                    hit2 = False
                if self.fighter2.dir >0 and self.fighter1.dir < 0:
                    hit2 = True
                    strike2 +=.1
                    cnt2=(cnt2+1)%20
                if self.fighter2.dir < 0 and self.fighter1.dir>0:
                    hit2 = False
            if self.fighter2.x > self.fighter1.x:
                if self.fighter2.dir>0 and self.fighter1.dir>0:
                    hit2 = False
                if self.fighter2.dir < 0 and self.fighter1.dir < 0:
                    hit2 = True
                    strike2 +=.1
                    cnt2=(cnt2+1)%20
                if self.fighter2.dir >0 and self.fighter1.dir < 0:
                    hit2 = False
                if self.fighter2.dir < 0 and self.fighter1.dir>0:
                    hit2 = True
                    strike2 +=.1
                    cnt2=(cnt2+1)%20
                    
def mouseClicked(): #mouseclicked for main menu and character selection
    if game.stage==1:
        if 270<mouseX<540 and 540<mouseY<585:
            game.stage=4
            game.itstime.rewind()
            game.itstime.play()
        elif 700<mouseX<990 and 540<mouseY<590:
            for i in range(5):
                game.sort_dict()    #call sort_dict method when leaderboard is accessed from main menu
            count_scoreboard=0
            game.file=open('leaderboard.csv','r')
            for line in game.file:
                xline = line.strip('').split(',')
                if count_scoreboard < 5:
                    game.name.append(xline[0])
                    game.scores.append(xline[1])
                count_scoreboard += 1
            game.file.close()
            game.stage = 3
            
    if game.stage==4:        #use global variable to store selected characters of both players
        global choice1, choice2
        if (0<mouseX<200 and 0<mouseY<200):
            choice1 = 1
        elif (205<mouseX<405 and 0<mouseY<200):
            choice1 = 2
        elif (0<mouseX<200 and 205<mouseY<405):
            choice1 = 3
        elif (200<mouseX<400 and 200<mouseY<400):
            choice1 = 4
        if (1017<mouseX<1217 and 0<mouseY<200):
            choice2 = 1
        elif (812<mouseX<1012 and 0<mouseY<200):
            choice2 = 2
        elif (1017<mouseX<1217 and 205<mouseY<405):
            choice2 = 3
        elif (812<mouseX<1012 and 200<mouseY<400):
            choice2 = 4
        if (choice1 != 0 and choice2 != 0):
            game.stage=2
            game.crowd.rewind()
            game.crowd.play()

minim =Minim(this)        
game=Game(1217,610,400)

def setup():
    size(1217,610)

def draw():
    background(0)
    game.display()
