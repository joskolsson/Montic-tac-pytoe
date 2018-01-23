import grids, threading, player, pygame,time

class Arena:
    """"""
    __game_working=True
    __actual_grid=(None,None)
    __p1=None
    __p2=None
    
    def __init__(self,terminal):
        self.__terminal=terminal#allow to switch mode as graphic's or terminal's
        self.__grid=grids.Master_Grid()
        self.__window = pygame.display.set_mode((740,700))#open window
        pygame.init()
        #import pictures
        self.__loose=pygame.image.load("Features/Picts/loose.png").convert()
        self.__win=pygame.image.load("Features/Picts/win.png").convert()
        self.__draw=pygame.image.load("Features/Picts/draw.png").convert()
        self.__bg=pygame.image.load("Features/Picts/bg.jpg").convert()
        self.__prev_bg=pygame.image.load("Features/Picts/bg.jpg").convert()
        self.__menu=pygame.image.load("Features/Picts/menu.png").convert()
        self.__croix=pygame.image.load("Features/Picts/grenade.png")\
        .convert_alpha()
        self.__big_g=pygame.image.load("Features/Picts/big_grenade.png")\
        .convert_alpha()
        self.__rond=pygame.image.load("Features/Picts/lapin.png")\
        .convert_alpha()
        self.__big_r=pygame.image.load("Features/Picts/big_rabbit.png")\
        .convert_alpha()
        #import sounds
        self.__win_sound=pygame.mixer.Sound("Features/Sounds/win.wav")
        self.__loose_sound=pygame.mixer.Sound("Features/Sounds/loose.wav")
        self.__draw_sound=pygame.mixer.Sound("Features/Sounds/herring.wav")
        self.__knights_sound=pygame.mixer.Sound("Features/Sounds/knights.wav")
        self.__ni_sound=pygame.mixer.Sound("Features/Sounds/ni.wav")
        self.__icky_sound=pygame.mixer.Sound("Features/Sounds/icky.wav")
        #constants' initialisation
        self.__noobcount=0#count wrong clicks (on grid)
        self.__coord_cells=self.__coord_cells()
        self.__player=False
        self.__playing=None
        self.__x=None
        self.__y=None
        self.__valide_coord=None
        self.__sign_cell_coord=self.__sign_cell_coord()
        self.__continuer_menu=1
        self.__continuer_rules=1
        self.__continuer_game=1
        self.__continue_the_game=1
        self.__player_type="human"
        self.__and_the_winner_is=(None,None)
        self.__authorize_restart=True#disable/ enable(comming soon) restart mode

    def __str__(self):
        '''
        Display who is playing in the terminal
        '''
        return "%s VERSUS %s" % (self.__p1,self.__p2)
    
    def __next_grid(self,x,y):
        '''
        Define the grid which must be played
        '''
        if not self.__grid.cell_status(x,y):
            self.__actual_grid=(x,y)
        else:
            self.__actual_grid=(None,None)
    
    def __game_phase(self,the_player,num):
        '''
        get new played move and put it on the grid if authorized
        then define new authorized zone
        '''
        if self.__terminal:
            print self.__grid
        while self.__continuer_game:
            if the_player.get_type()=="human" and self.__p1.get_type()=="IA"\
            and self.__p2.get_type()=="IA":
                break
            pygame.time.Clock().tick(30)#limit the loop's turns to max 30/second
            if self.__valide_coord==None and (the_player.get_type()=="IA" or\
             (the_player.get_type()=="human" and self.__x!=None)):
                #get new played move
                if the_player.get_type()=="IA":
                    x,y=the_player.reflexion(self.__grid,1,self.__actual_grid)
                    time.sleep(0.1)
                else:
                    if not self.__terminal:
                        x=self.__x
                        y=self.__y
                    if self.__terminal:
                        x,y=the_player.reflexion(self.__grid,0)
                #extract information about the cell's location from x,y
                master_x=x/3
                master_y=y/3
                self.__x=x
                self.__y=y
                x%=3
                y%=3
                #looking where we are on master grid
                if self.__actual_grid[0]==None or self.__actual_grid[1]==None:
                    if not self.__grid.cell_status(master_x,master_y):
                        self.__actual_grid=(master_x,master_y)
                #check if we are at the right place at the opportune time
                # under the asses of blurgin
                if self.__actual_grid[0]==master_x and\
                 self.__actual_grid[1]==master_y:
                    if self.__grid.set_in_inner_grid(num,self.__actual_grid[0],
                                  self.__actual_grid[1],x,y)[0] and\
                                  x!=None and y !=None:
                        self.__valide_coord=True#var checked by display game
                        self.__next_grid(x,y)#Define the next authorized cell
                        break
                    else:
                        if not self.__terminal:
                            self.__valide_coord=False
                #if unauthorized moved..
                elif x!=None:
                    if not self.__terminal:
                        self.__x=None
                        self.__valide_coord=False
            if self.__terminal:
                print self.__grid.search_winner()        
    
    def play(self):
        '''
        run the mechanism of game
        '''
        trololo=True#always name one var trololo (for luck)
        self.__playing=True#define which player turn it is
        if self.__terminal:
            self.__choose_player(None)
        else:
            self.__p1 = player.Human("",1)
            self.__p2 = player.Human("",2)
        self.__player_type=self.__p1.get_type()
        if not self.__terminal:
            #launch the threaded loops
            thread=threading.Thread(target=self.run)
            thread.start()
        while self.__continuer_game:#to infinite
            while self.__game_working:#and further
                if self.__playing:
                    if self.__terminal:
                        print "%s's turn" % self.__p1
                    self.__game_phase(self.__p1,1)
                else:
                    if self.__terminal:
                        print "%s's turn" % self.__p2
                    self.__game_phase(self.__p2,2)
                if self.__grid.search_winner():
                    break
                if self.__playing:
                    self.__player_type=self.__p2.get_type()
                else:
                    self.__player_type=self.__p1.get_type()
                self.__playing=not self.__playing
            if self.__terminal:
                print self.__grid
            else:
                self.__winner()
                if trololo and self.__grid.get_winner() and not self.__terminal:
                    self.__display_winner()
                    trololo=False#display just one end (bug correction)
        if self.__grid.get_winner() and self.__terminal:
            return self.__winner()
            
    #renvoyer au run si on clique sur un bouton restart (comming soon)
    def run (self):
        '''
        first function of graphic threaded part necessary for restart mode
        '''
        self.__make_menu()#display menu screen and functions
        while self.__continuer_game:
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                self.__quit(event)#allow to quit
                self.__choose_player(event)#or to choose player
        
    def __choose_player(self,event):
        '''
        choose players' type and name on graphic or terminal 
        '''
        if self.__terminal:
            while True:
                print "\nPLAYER 1 :\n0. Human\n1. IA\n"
                n=1
                while True:
                    try:
                        n=int(raw_input("valeur 0 ou 1 : "))
                        if -1<n<2:
                            break
                    except:
                        print "Error"
                if 0==n:
                    if  self.__terminal:    
                       name=raw_input("nom : ")
                    else:name="jo"
                    self.__p1 = player.Human(name,1)
                    break
                else:
                    self.__p1 = player.IA("jojo le rigolo",1)
                    break
            while True:
                print "\nPLAYER 2 :\n0. Human\n1. IA\n"
                n=1
                while True:
                    try:
                        n=int(raw_input("valeur 0 ou 1 : "))
                        if -1<n<2:
                            break
                    except:
                        print "Error"
                if 0==n:
                    if self.__terminal:
                        name=raw_input("nom : ")
                    else: name="gogo"
                    self.__p2 = player.Human(name,2)
                    break
                else:
                    self.__p2 = player.IA("gogo le hero",2)
                    break
        else :#graphic mode
                if event.type==pygame.MOUSEBUTTONDOWN and event.button==1\
                and 660<event.pos[1]<690 and self.__authorize_restart==True:
                    x=event.pos[0]
                    if 100<x<200 or 320<x<420 or 540<x<640:
                        time.sleep(0.1)
                        #re-initialisation in case of restart mode(comming son)
                        self.__grid.reboot_master_grid()
                        self.__player=False
                        self.__playing=True
                        self.__actual_grid=(None,None)
                        self.__won_list=[]
                        self.__authorize_restart=False
                        if 100<x<200:#left button clicked
                            self.__p1 = player.Human("",1)
                            self.__p2 = player.Human("",2)
                            self.__player_type="human"
                        elif 320<x<420:#middle button clicked
                            self.__p1 = player.Human("",1)
                            self.__player_type="human"
                            self.__p2 = player.IA("",2)
                        elif 540<x<640:#right button clicked
                            self.__p1 = player.IA("",1)
                            self.__p2 = player.IA("",2)
                            x,y=self.__p1.reflexion(None,0,None)
                            self.__player_type="IA"
                        self.__display_game()#launch game screen
    
    def __winner(self):
        '''
        set win actions depending on who win.
        '''
        w=self.__grid.get_winner()
        self.__game_working=False
        if self.__p1.get_type()=="IA" and self.__p2.get_type()=="IA":
        #bug correction
            if w=="player1":w="player2"
            else: w="player1"
        if w == "player1":
            self.__and_the_winner_is=(self.__win,self.__win_sound)
            return "%s gagne " % self.__p1
        elif w == "player2" :
            self.__and_the_winner_is=(self.__loose,self.__loose_sound)
            return "%s gagne " % self.__p2
        elif w == "null":
            self.__and_the_winner_is=(self.__draw,self.__draw_sound)
            return "draw"
            
    def __display_winner(self):
        '''
        Graphic mode
        '''
        time.sleep(1)
        pygame.draw.rect(self.__window, (255,255,255),
                 pygame.Rect(0,0,740,700))
        #hide game screen
        picture,sound=self.__and_the_winner_is
        sound.play()
        self.__window.blit(picture,(0,0))
        pygame.display.flip()#refresh
        
    def __display_game(self):
        '''
        Main function of graphic mode
        handle mouse's clicks
        display moves...
        '''
        self.__draw_grid_on_bg()
        while self.__continue_the_game:
            if self.__valide_coord!=None:
                #then the move has been read by the other threaded part
                self.__new_move()
            for event in pygame.event.get():
                self.__quit(event)
                #allow to restart while running /!\ (comming soon)
                if event.type==pygame.MOUSEBUTTONDOWN and 660<event.pos[1]<690\
                 and self.__authorize_restart==True:
                    self.__choose_player(event)
                if self.__player_type=="human":
                    #when the mouse is pressed in the grid zone
                    if event.type==pygame.MOUSEBUTTONDOWN and\
                    145<event.pos[0]<595 and 85<event.pos[1]<535 and\
                     self.__x==None:
                        #position is recorded
                        cell=self.__which_case(event.pos[0],event.pos[1])
                        if cell!=None:#set sail (cell) if unanbigous click
                            self.__x=cell["x"]
                            self.__y=cell["y"]
                            self.__new_move()
                        else :
                            self.__wrong_click_sound()
    
    def __make_menu(self):
        '''
        Display menu features
        '''
        pygame.mixer.music.load("Features/Sounds/grailthm.mid")
        pygame.mixer.music.play()
        background=self.__menu
        self.__window.blit(background,(0,0))
        pygame.display.flip()
    
    def __quit(self,event):
            if event.type==pygame.QUIT:
                #break all infinites' loop
                self.__continuer_menu=False
                self.__continuer_rules=False
                self.__continuer_game=False
                self.__continue_the_game=False
                self.__game_working=False
                
    def __draw_grid_on_bg(self):
        '''
        Draw grid on background (what an usefull comment XD)
        '''
        background=self.__bg
        self.__window.blit(background,(0,0))
        for i in (1,2,4,5,7,8):
            for j in xrange(3):
                pygame.draw.rect(self.__window, (168,87,0),
                 pygame.Rect(155+150*j,90+50*i,135,3))
                pygame.draw.rect(self.__window, (168,87,0),
                 pygame.Rect(150+50*i,95+150*j,3,135))
            
        for i in xrange(1,3):
            pygame.draw.rect(self.__window, (165,42,42),
             pygame.Rect(145,85+150*i,450,5))
            pygame.draw.rect(self.__window, (165,42,42),
             pygame.Rect(145+150*i,85,5,450))
        pygame.display.flip()
        
    def __new_move(self):
        '''
        check if the move is correct or not and display corresponding features
        '''
        #if position has been read
        if self.__valide_coord!=None:#bug correction
            #is the player alowed to play here?
            if self.__valide_coord==True:
                #print self.__valide_coord
                #self.__prev_bg=pygame.image.fromstring(self.__prev_bg)
                #self.__window.blit(self.__prev_bg,(0,0))
                self.__print_sign(self.__x,self.__y)
                self.__inter_win()
                pygame.display.flip()
                #pygame.image.save(window, self.__prev_bg)
                #self.__next_hidded_zone()
                #Next player turn
                self.__player=not self.__player
            elif self.__player_type=="human": self.__icky_sound.play()
            self.__reset_X_Y()
            
    def __print_sign(self,x,y):
        '''
        display new moove
        '''
        if self.__player: sign=self.__rond
        else: sign=self.__croix
        x=self.__sign_cell_coord[0][x]
        y=self.__sign_cell_coord[1][y]
        self.__window.blit(sign,(x,y))
        pygame.display.flip()
    
    def __inter_win(self):
        '''
        check if new inter win occured and display them
        '''
        for x in range(3):
            for y in range(3):
                if self.__grid.cell_status(x,y):
                    if not self.__player: sign=self.__big_g
                    else: sign=self.__big_r
                    if not (x,y) in self.__won_list:
                        time.sleep(0.4)
                        pygame.draw.rect(self.__window, (168,87,0),
                        pygame.Rect(155+150*x,95+150*y,135,135))
                        self.__window.blit(sign,(150+150*x,90+150*y))
                        self.__won_list.append((x,y))
                    pygame.display.flip()
   #comming soon!  lot of updates comming soon, isn't it? :-p
    def __next_hidded_zone(self):
        '''
        hide unauthorized zone
        '''
        X,Y=self.__actual_grid
        for x in range(3):
            for y in range(3):
                if (X!=x or Y!=y) and X!=None:
                    self.__hide(x,y)
                
    def __hide(self,i,j):
        if not self.__grid.cell_status(i,j):
            rect = pygame.Surface((140,140), pygame.SRCALPHA, 32)
            rect.fill((168,87,0,60))
            self.__window.blit(rect, (150+150*i,90+150*j))
            pygame.display.flip()   
    
    def __wrong_click_sound(self):
        '''
        display ni when ambiguous click
        '''
        if self.__noobcount==0:    
            self.__knights_sound.play()
            self.__noobcount=1
        else: self.__ni_sound.play()
        
    def __sign_cell_coord(self):
        '''
        attribute coord to the sign depeding on which cell we are in
        '''
        sign_coord_list=[[],[]]
        x=150
        y=90
        for i in xrange(9):
            sign_coord_list[0].append(x)
            sign_coord_list[1].append(y)
            x+=50
            y+=50
        return sign_coord_list
    
    def __reset_X_Y(self):
        '''
        reset x and y when used
        '''
        self.__x=None
        self.__y=None
        self.__valide_coord=None
    
    def __coord_cells(self):
        '''
        make the list of all pixels coord for cells
        '''
        coord_list=[]
        dico_x={}
        dico_y={}
        x_list=[]
        y_list=[]
        x=150
        y=90
        for i in xrange(9):
            dico_x[i]=(x+3,x+47)
            dico_y[i]=(y+3,y+47)
            x+=50
            y+=50
        coord_list.append(dico_x)
        coord_list.append(dico_y)
        return coord_list

    def __which_case(self,x,y):
        '''
        return the cell's position depending on it's pixel clicked
        '''
        dico_coord={}    
        for i in xrange(9):
            tuple_x=self.__coord_cells[0][i]
            tuple_y=self.__coord_cells[1][i]
            if tuple_x[0]<x<tuple_x[1]:
                dico_coord["x"]=i
            if tuple_y[0]<y<tuple_y[1]:
                dico_coord["y"]=i
            if dico_coord.has_key("x") and dico_coord.has_key("y"):
                return dico_coord    
        return None
