from search.grid2D import ProblemeGrid2D
from search import probleme
import numpy as np
import s0

class M(s0.S0):

    def __init__(self,game,id,posPlayers):
        
        #on initialise les attributs du joueur adverse
        super().__init__(game,id,posPlayers)
        self.p1 = ProblemeGrid2D(self.initStates[self.oid],self.objectifs[self.oid],self.g,'manhattan')
        self.path1 = probleme.astar(self.p1,verbose=False)
        
        self.bestO1=self.objectifs[self.oid]
        self.bestPath1=self.path1
        

      
    def non_blocage(self,x1,x2,y1,y2):
        """
            rend True si la pose des murs ne bloque pas l'adversaire à jamais, False sinon 
        """
        #on suppose qu'il peut poser des murs
        self.g[x1][y1]=False
        self.g[x2][y2]=False
        ptmp0 = ProblemeGrid2D(self.posPlayers[self.id],self.objectifs[self.id],self.g,'manhattan')
        pathtmp0 = probleme.astar(ptmp0,verbose=False)
        seDeplacer=True
        ptmp1 = ProblemeGrid2D(self.posPlayers[self.oid],self.objectifs[self.oid],self.g,'manhattan')
        pathtmp1 = probleme.astar(ptmp1,verbose=False)
        #on vérifie que les murs posés ne bloque pas l'adversaire à jamais
        if(self.objectifs[self.id]==pathtmp0[len(pathtmp0)-1] and self.objectifs[self.oid]==pathtmp1[len(pathtmp1)-1]):
            
            return True

        else:
            #on retire les murs
            self.g[x1][y1]=True
            self.g[x2][y2]=True
            return False
        

    
    
    def evaluate(self):
        return len(self.bestPath1) - len(self.bestPath0)
    
    def minimax(self,pos,depth,maximizingPlayer):
        
        
        pos0= self.posPlayers[self.id]
        posAd=self.posPlayers[self.oid]
        if depth==0 or (pos0==self.besto or posAd==self.bestO1):
            return self.evaluate(),None 
        
       
        #coordonnées murs
        fWall,sWall=(0,0),(0,0)
        pose_mur=False #booleen qui vaut True si on peut deposer mur
        if self.jMur<len(self.walls[self.id]) :
            x1,y1=self.trouver_mur() 
            x2,y2=x1,y1+1
        
        
            fWall=(x1,y1) #devant le joueur adverse
            sWall=(x2,y2) #devant a droite du joueur adverse
        
            
            #on vérifie que les murs sont sur des positions légales
            peutMettreD=self.legal_wall_position(fWall) and self.legal_wall_position(sWall)
        
            if(peutMettreD):
                pose_mur=self.non_blocage(fWall[0],sWall[0],fWall[1],sWall[1])
            else:
                sWall=(x2,y1-1) #devant à gauche de l'adversaire
                
                peutMettreG=self.legal_wall_position(fWall) and self.legal_wall_position(sWall)
                
                if(peutMettreG): 
                        pose_mur=self.non_blocage(fWall[0],sWall[0],fWall[1],sWall[1])
        
        deplacer= self.bestPath0[1]

        moves=[(fWall,sWall),deplacer]
        
        if maximizingPlayer:
            max_value = float('-inf')
            best_move=None
            i_best=-1 #o si  il pose mur, 1 s'il se deplace
            for i in range(len(moves)):
                if(i==0 and pose_mur): #poseMur
                    (x1,y1),(x2,y2)=moves[i]
                    self.g[x1][y1]=False
                    self.g[x2][y2]=False
                    value,_=self.minimax(pos,depth-1,False)
                    self.g[x1][y1]=True
                    self.g[x2][y2]=True
                else:
                    
                    row,col = moves[i]
                    self.posPlayers[self.id]=(row,col)
                    
                    #self.players[self.id].set_rowcol(row,col)
                    value,_=self.minimax(moves[i],depth-1,False)
                    
                    row,col = pos
                    self.posPlayers[self.id]=(row,col)
                    
                    #self.players[self.id].set_rowcol(row,col)
                    
                    

                
                if value > max_value:
                    max_value = value
                    best_move = moves[i]
                    i_best=i
                
            return (max_value,(best_move,i_best))
            
        else:
            min_value = float('inf')
            best_move=None
            i_best=-1
            for i in range(len(moves)):
                if(i==0 and pose_mur): #poseMur
                    (x1,y1),(x2,y2)=moves[i]
                    self.g[x1][y1]=False
                    self.g[x2][y2]=False
                    value,_=self.minimax(pos,depth-1,True)
                    self.g[x1][y1]=True
                    self.g[x2][y2]=True
                else:
                    
                    row,col = moves[i]
                    self.posPlayers[self.id]=(row,col)
                    #self.players[self.id].set_rowcol(row,col)
                    value,_=self.minimax(moves[i],depth-1,True)
                    row,col = pos
                    self.posPlayers[self.id]=(row,col)
                    #self.players[self.id].set_rowcol(row,col)
                    


                
                if value < min_value:
                    min_value = value
                    best_move = moves[i]
                    i_best=i
                
            return (min_value,(best_move,i_best))
        

        

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
                self.bestO1=o
       
        _,(move,i)=self.minimax(self.posPlayers[self.id],5,True)
        if(i==0): #poseMur
                
                (x1,y1),(x2,y2)=move
                self.g[x1][y1]=False
                self.g[x2][y2]=False
                self.walls[self.id][self.jMur].set_rowcol(x1,y1)
                self.walls[self.id][self.jMur+1].set_rowcol(x2,y2)
                self.jMur=self.jMur+2
        else:
            
            row,col = move
            self.posPlayers[self.id]=(row,col)
            self.players[self.id].set_rowcol(row,col)
        
            if (row,col) == self.besto: # le joueur a atteint son objectif 
                self.gagner=True
        
        # mise à jour du plateau de jeu
        self.game.mainiteration()

        

    
        

    