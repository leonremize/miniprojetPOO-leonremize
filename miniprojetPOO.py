#version 0.2 : Ajouter la classe Plateau (génération, click simple)

from random import randint

class Case :
    '''
    Représente une case du démineur
    
    Constructeur :
    Case(est_bombe(bool))
    
    Attributs :
    est_revelee(bool), est_drapeau(bool)
    
    Méthode
    reveler, marquer, set_valeur, get_valeur, afficher
    '''

    def __init__(self, bombe):
        self.__est_bombe = bombe
        self.est_revelee = False
        self.est_drapeau = False
        self.__valeur = 0

    def reveler(self) :
        '''
        Permet de reveler la case, ou d'enlever le drapeu s'il y en a 1
        renvoie True si c'était une bombe et qu'il n'y avait pas de drapeau, False sinon
        '''
        if self.est_drapeau :
            self.est_drapeau = False
            return False
        
        self.est_revelee = True
        return not self.__est_bombe

    def marquer(self) :
        '''Permet de mettre un drapeau sur une case'''
        pass
    
    def set_valeur(self, v) :
        '''Fixe la valeur sur la case, lors de la configuration initiale
        La valeur correspond au nombre de bombe adjacentes (max 8) et vaut 9 si la case est une bombe'''
        if self.__est_bombe :
            self.__valeur = 9
        else :
            self.__valeur = v

    def get_valeur(self) :
        '''Obtient la valeur de la case si elle est révélée, False sinon'''
        if self.est_revelee :
            return self.__valeur
        return False
    
    def afficher(self) :
        '''Renvoie le symbole correspondant à cette case pour l'affichage
        # si masquée
        P si marquée
        " " si revelee et valeur=0
        {valeur} si revelee et valeur>0'''

        if self.est_drapeau :
            return "P"
        elif self.est_revelee :
            if self.__valeur == 0 :
                return " "
            return self.__valeur
        else :
            return "#"

class Plateau :
    '''
    Classe gérant le plateau ainsi que les inetraction avec le joueur
    
    Constructeur :
    Plateau(largueur, longueur, nb_bombe)
    
    Méthodes :
    click, click_droit, affichage
    '''
    def __init__(self, largueur:int, longueur:int, nb_bombe:int):
        self.__largueur = largueur
        self.__longueur = longueur
        self.map = []                           #map doit être un attribut privé mais ne l'est pas encore pour pouvoire effectuer des tests
        self.__nb_bombe = nb_bombe

    def click(self, x, y) :
        '''Permet de reveler un case de coordonée (x,y)
        renvoie False si on revele une bombe
        renvoie True si le click est hors de la grille ou sur une case sure'''
        if type(x)!=int or type(y)!=int or x<0 or x>=self.__largueur or x<0 or y>=self.__longueur :
            return True
        
        if self.map==[] :
            self.__premier_click(x, y)
        
        return self.map[y][x].reveler()

    def __premier_click(self, x, y) :
        '''Génére le pllateau en prenant en compte le lieu du premier click'''
        
        
        #placement des bombes
        interdit = self.__voisins(x,y)
        bombes = []
        while len(bombes)<self.__nb_bombe :
            xbombe, ybombe = randint(0,self.__largueur-1), randint(0,self.__longueur-1)
            if (xbombe,ybombe) not in interdit and (xbombe,ybombe) not in bombes :
                bombes.append((xbombe,ybombe))

        #création de la map
        for j in range(self.__longueur) :
            self.map.append([])
            for i in range(self.__largueur) :
                if (i, j) in bombes :
                    self.map[j].append(Case(True))
                else :
                    self.map[j].append(Case(False))

        #mise à jour des valeurs des cases :
        for j in range(self.__longueur) :
            for i in range(self.__largueur) :
                nb_bombes_voisines = 0
                for voisin in self.__voisins(i,j) :
                    if voisin in bombes :
                        nb_bombes_voisines += 1
                self.map[j][i].set_valeur(nb_bombes_voisines)

        

    def __voisins(self, x, y) :
        '''Renvoie la liste des voisins existants pour une case de coordonée (x,y)'''
        potentiels_voisins = [(x,y),(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1),(x,y-1),(x-1,y-1),(x-1,y),(x-1,y+1)]
        voisins = []
        for v in potentiels_voisins :
            if v[0]>=0 and v[0]<self.__largueur and v[1]>=0 and v[1]<self.__longueur :
                voisins.append(v)
        return voisins


    def click_droit(self, x, y) :
        pass

    def affichage(self) :
        pass

#Création du plateau
p = Plateau(3, 3, 3)            
p.click(0,1)
#Le plateau ressemble forcément à  :    □29
#                                       □39
#                                       □29

#Car 3 bombes doivent être placée dans un carré de 9 cases sans être voisines de la case à gauche au milieu

#Acutuellement, l'affiche du plateau donnérait :    ###
#                                                    ##
#                                                   ###
#Car seule la case de coordonée (0,1) est révélée

#Tests pour vérifier le bon déroulement de la procédure de création
assert p.click(0,0)==True      #On clique sur la case en haut à gauche, sans tomber sur une bombe
assert p.click(2,0)==False     #On clique sur la case en haut à droite (bombe)
assert p.click(1,1)==True      #On clique sur la case du milieu, sans tomber sur une bombe
assert p.map[1][1].get_valeur()==3      #On regarde la valeur sur la case centrale, on obtient bien 3 pour les 3 bombes sur la colonne de droite
assert p.map[2][1].get_valeur()==False  #On regarde la valeur sur une case non-revelée (en bas au milieu), on ne peux pas la regardée (renvoie False)
assert p.click("hello",-12)==True