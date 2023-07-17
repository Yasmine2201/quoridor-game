from search.grid2D import ProblemeGrid2D
from search import probleme
import numpy as np

class S0:
    
    
    def __init__(self,game,id,posPlayers):
        self.gagner=False
        self.game=game
        self.id=id      #id du joueur
        if(id==0):
            self.oid=1   #id de l'adversaire
        else:
            self.oid=0
        self.nbLignes = game.spriteBuilder.rowsize
        self.nbCols = game.spriteBuilder.colsize
        self.lMin=2  # les limites du plateau de jeu (2 premieres lignes utilisees pour stocker les murs)
        self.lMax=self.nbLignes-2 
        self.cMin=2
        self.cMax=self.nbCols-2
        self.players = [o for o in game.layers['joueur']]
        self.initStates = [o.get_rowcol() for o in self.players]
        self.ligneObjectif = (self.initStates[1][0],self.initStates[0][0]) # chaque joueur cherche a atteindre la ligne ou est place l'autre
        self.walls = [[],[]]
        self.walls[0] = [o for o in game.layers['ramassable'] if (o.get_rowcol()[0] == 0 or o.get_rowcol()[0] == 1)]  
        self.walls[1] = [o for o in game.layers['ramassable'] if (o.get_rowcol()[0] == self.nbLignes-2 or o.get_rowcol()[0] == self.nbLignes-1)]  
        self.allWalls = self.walls[0]+self.walls[1]
        self.allObjectifs = ([(self.ligneObjectif[0],i) for i in range(self.cMin,self.cMax)],[(self.ligneObjectif[1],i) for i in range(self.cMin,self.cMax)])
        self.objectifs = (self.allObjectifs[0][0], self.allObjectifs[1][0])
        self.g =np.ones((self.nbLignes,self.nbCols),dtype=bool)  # une matrice remplie par defaut a True  
        for w in self.wallStates(self.allWalls):            # on met False quand murs
            self.g[w]=False
        for i in range(self.nbLignes):                 # on exclut aussi les bordures du plateau
            self.g[0][i]=False
            self.g[1][i]=False
            self.g[self.nbLignes-1][i]=False
            self.g[self.nbLignes-2][i]=False
            self.g[i][0]=False
            self.g[i][1]=False
            self.g[i][self.nbLignes-1]=False
            self.g[i][self.nbLignes-2]=False

        self.p0 = ProblemeGrid2D(self.initStates[self.id],self.objectifs[self.id],self.g,'manhattan')
        self.path0 = probleme.astar(self.p0,verbose=False)
        self.posPlayers =posPlayers 
        self.jMur=0
        self.besto=self.objectifs[self.id]
        self.bestPath0=self.path0

        

    def wallStates(self,walls): 
        """
            donne la liste des coordonnees des murs
        """
        return [w.get_rowcol() for w in walls]
    
    def playerStates(self,players):
        """
            donne la liste des coordonnees des joueurs
        """
        return [p.get_rowcol() for p in players]
    
    def legal_wall_position(self,pos):
        """
            rend True si le joueur peut poser un mur
        """
        row,col = pos
        # une position legale est dans la carte et pas sur un mur deja pose ni sur un joueur
        # attention: pas de test ici qu'il reste un chemin vers l'objectif
        return ((pos not in self.wallStates(self.allWalls)) and (pos not in self.playerStates(self.players)) and row>self.lMin and row<self.lMax-1 and col>=self.cMin and col<self.cMax)
    
    def ne_pas_bloquer(self,x1,x2,y1,y2):
        """
            rend True si le joueur peut se déplacer, False sinon
            Un joueur ne peut pas se déplacer du moment qu'il dépose des murs aux coordonnées passées en argument sans bloquer à jamais son adversaire
        """ 
        #on suppose qu'il peut deposer des murs
        self.g[x1][y1]=False
        self.g[x2][y2]=False
        ptmp0 = ProblemeGrid2D(self.posPlayers[self.id],self.objectifs[self.id],self.g,'manhattan')
        pathtmp0 = probleme.astar(ptmp0,verbose=False)
        seDeplacer=True
        ptmp1 = ProblemeGrid2D(self.posPlayers[self.oid],self.objectifs[self.oid],self.g,'manhattan')
        pathtmp1 = probleme.astar(ptmp1,verbose=False)
        #on vérifie que les murs posés ne bloque pas l'adversaire à jamais
        if(self.objectifs[self.id]==pathtmp0[len(pathtmp0)-1] and self.objectifs[self.oid]==pathtmp1[len(pathtmp1)-1]):
            self.walls[self.id][self.jMur].set_rowcol(x1,y1)
            self.walls[self.id][self.jMur+1].set_rowcol(x2,y2)
            self.jMur=self.jMur+2
            seDeplacer=False #si le joueur ajoute un mur, il ne peut plus se deplacer 
        
        else:
            self.g[x1][y1]=True
            self.g[x2][y2]=True
        
        return seDeplacer
    
    def trouver_mur(self):
        """
            calcule les coordonnées (x,y) du premier mur à placer devant l'adversaire 
        """
        #calcule les coordoonés devant l'adversaire
        if(self.id==0):
            x1=self.posPlayers[self.oid][0]-1
        else:
            x1=self.posPlayers[self.oid][0]+1
        
        y1=self.posPlayers[self.oid][1]
        
        return (x1,y1)