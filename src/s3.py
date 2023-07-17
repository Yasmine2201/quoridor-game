from search.grid2D import ProblemeGrid2D
from search import probleme
import numpy as np
import s0

class S3(s0.S0):
    def __init__(self,game,id,posPlayers):
        
        #on initialise les attributs du joueur adverse
        super().__init__(game,id,posPlayers)
        self.p1 = ProblemeGrid2D(self.initStates[self.oid],self.objectifs[self.oid],self.g,'manhattan')
        self.path1 = probleme.astar(self.p1,verbose=False)
        
        self.bestO1=self.objectifs[self.oid]
        self.bestPath1=self.path1
    


    
    
    def jouer(self):
        #MISE A JOUR GRILLE
        for w in self.wallStates(self.allWalls): # on met False quand murs
            self.g[w]=False
        
        #MISE A JOUR DES BEST OBJECTIVES pour prendre l'objectif le plus proche de sa position actuelle
        for o in self.allObjectifs[self.id]:
            p00 = ProblemeGrid2D(self.posPlayers[self.id],o,self.g,'manhattan')
            path00 = probleme.astar(p00,verbose=False)
            if(len(path00)<len(self.bestPath0)):
                self.bestPath0=path00
                self.besto=o
        for o in self.allObjectifs[self.oid]: #on parcourt tous les objectifs du joueur adverse
            p11 = ProblemeGrid2D(self.posPlayers[self.oid],o,self.g,'manhattan')
            path11 = probleme.astar(p11,verbose=False)
            if(len(path11)<len(self.bestPath1)):
                self.bestPath1=path11
                self.bestO1=o
        p00 = ProblemeGrid2D(self.posPlayers[self.id],self.besto,self.g,'manhattan')
        self.bestPath0 = probleme.astar(p00,verbose=False)
        
        seDeplacer=True
        
        #on verifie s'il nous reste des murs a placer 
        
        if(self.jMur<len(self.walls[self.id])): 
            #
            for i in range(1,len(self.bestPath1)-1,2):
                #on calcule les positions des murs à placer sur le chemin BestPath de l'adversaire
                x1,y1 = self.bestPath1[i]
                x2,y2=x1,y1+1
              
                devant=(x1,y1) #devant le joueur adverse
                devantD=(x2,y2) #devant a droite du joueur adverse
                
                #on vérifie que les murs sont sur des positions légales
                peutMettreD=self.legal_wall_position(devant) and self.legal_wall_position(devantD)
                
                if(peutMettreD):
                    #on met à jour seDeplacer et on pose des murs si c'est possible
                    seDeplacer=self.ne_pas_bloquer(x1,x2,y1,y2)
                    break
                
                y2=y1-1
                devantG=(x1,y2)
                peutMettreG=self.legal_wall_position(devant) and self.legal_wall_position(devantG)
                if(peutMettreG):
                    seDeplacer=self.ne_pas_bloquer(x1,x2,y1,y2)
                    break
                
        if(seDeplacer): #le joueur se déplace via A*
            row,col = self.bestPath0[1]
            self.posPlayers[self.id]=(row,col)
            self.players[self.id].set_rowcol(row,col)
            if (row,col) == self.besto:
                self.gagner=True
        # mise à jour du plateau de jeu
        self.game.mainiteration()
        
