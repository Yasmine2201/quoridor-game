from search.grid2D import ProblemeGrid2D
from search import probleme
import numpy as np
import s0

class S2(s0.S0):
    def __init__(self,game,id,posPlayers):
        
        #on initialise les attributs du joueur adverse
        super().__init__(game,id,posPlayers)
        self.p1 = ProblemeGrid2D(self.initStates[self.oid],self.objectifs[self.oid],self.g,'manhattan')
        self.path1 = probleme.astar(self.p1,verbose=False)
        
        self.besto1=self.objectifs[self.oid]
        self.bestPath1=self.path1

      

    def jouer(self):
        """
            permet de jouer un coup avec la stratégie qui lui a fait appel 
        """
        
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
                self.besto1=o
        p00 = ProblemeGrid2D(self.posPlayers[self.id],self.besto,self.g,'manhattan')
        self.bestPath0 = probleme.astar(p00,verbose=False)
        p11 = ProblemeGrid2D(self.posPlayers[self.oid],self.besto1,self.g,'manhattan')
        path11 = probleme.astar(p11,verbose=False)
        seDeplacer=True
        
        #on introduit un booléen qui vaut True si la longueur du chemin du joueur < à celle de son adversaire
        long_deplace=len(self.bestPath0)<len(path11)

        #on verifie s'il nous reste des murs a placer et si on est entrain de perdre, on pose des murs
        if(self.jMur<len(self.walls[self.id]) and not long_deplace):
            #calcule les coordoonés des murs à placer devant l'adversaire
            x1,y1=self.trouver_mur() 
            x2,y2=x1,y1+1
            
            devant=(x1,y1) #devant le joueur adverse
            devantD=(x2,y2) #devant a droite du joueur adverse
            
            #on vérifie que les murs sont sur des positions légales
            peutMettreD=self.legal_wall_position(devant) and self.legal_wall_position(devantD)
          
            if(peutMettreD):
                #on met à jour seDeplacer et on pose des murs si c'est possible
                seDeplacer=self.ne_pas_bloquer(x1,x2,y1,y2)
            
            #si les positions ne sont pas  légales, on change l'emplacement du 2 eme mur
            else:
                devantG=(x2,y1-1) #devant à gauche de l'adversaire
                
                peutMettreG=self.legal_wall_position(devant) and self.legal_wall_position(devantG)
                
                if(peutMettreG): 
                   
                    seDeplacer=self.ne_pas_bloquer(x1,x2,y1,y1-1)
        
        
        
        if(seDeplacer): #notre joueur se déplace via A* et on met à jour la position du joueur
            row,col = self.bestPath0[1]
            self.posPlayers[self.id]=(row,col)
            self.players[self.id].set_rowcol(row,col)
            
            if (row,col) == self.besto: # le joueur a atteint son objectif 
                self.gagner=True
        
        # mise à jour du plateau de jeu
        self.game.mainiteration()
        
            