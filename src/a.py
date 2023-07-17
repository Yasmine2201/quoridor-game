from search.grid2D import ProblemeGrid2D
from search import probleme
import numpy as np
import random
import s0

class Alea(s0.S0):
   
    def draw_random_wall_location(self):
        # tire au hasard un couple de position permettant de placer un mur
        while True:
            random_loc = (random.randint(self.lMin,self.lMax),random.randint(self.cMin,self.cMax))
            if self.legal_wall_position(random_loc):  
                inc_pos =[(0,1),(0,-1),(1,0),(-1,0)] 
                random.shuffle(inc_pos)
                for w in inc_pos:
                    random_loc_bis = (random_loc[0] + w[0],random_loc[1]+w[1])
                    if self.legal_wall_position(random_loc_bis):
                        return (random_loc,random_loc_bis)

    
    def jouer(self):
        #MISE A JOUR GRILLE
        
        for w in self.wallStates(self.allWalls): # on met False quand murs
            self.g[w]=False

        p00 = ProblemeGrid2D(self.posPlayers[self.id],self.besto,self.g,'manhattan')
        self.bestPath0 = probleme.astar(p00,verbose=False)
        
        #on fait bouger le joueur 0 
        n = random.random() #nombre aleatoire entre 0 et 1
        if(n<0.5 and self.jMur<len(self.walls[self.id])): #on verifie s'il lui reste des murs à placer
            while(True):
                ((x1,y1),(x2,y2)) = self.draw_random_wall_location()
                self.g[x1][y1]=False
                self.g[x2][y2]=False
                ptmp0 = ProblemeGrid2D(self.posPlayers[self.id],self.objectifs[self.id],self.g,'manhattan')
                pathtmp0 = probleme.astar(ptmp0,verbose=False)

                ptmp1 = ProblemeGrid2D(self.posPlayers[self.oid],self.objectifs[self.oid],self.g,'manhattan')
                pathtmp1 = probleme.astar(ptmp1,verbose=False)
                if(self.objectifs[self.id]==pathtmp0[len(pathtmp0)-1] and self.objectifs[self.oid]==pathtmp1[len(pathtmp1)-1]):
                    self.walls[self.id][self.jMur].set_rowcol(x1,y1)
                    self.walls[self.id][self.jMur+1].set_rowcol(x2,y2)
                    self.jMur=self.jMur+2
                    break
                self.g[x1][y1]=True
                self.g[x2][y2]=True
        else: #le joueur se déplace 
            row,col = self.bestPath0[1]
            self.posPlayers[self.id]=(row,col)
            self.players[self.id].set_rowcol(row,col)
            if (row,col) == self.besto:
                self.gagner=True
        # mise à jour du plateau de jeu
        self.game.mainiteration()
        