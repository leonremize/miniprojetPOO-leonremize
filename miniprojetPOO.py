#version 0.3 : Finalisation du plateau (affichage, click) et ajout des drapeaux (marquer, click_droit)

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
        renvoie True si tout va bien (pas de bombe), False sinon
        '''
        if self.est_drapeau :
            self.est_drapeau = False
            return True
        
        self.est_revelee = True
        return not self.__est_bombe

    def marquer(self) :
        '''Permet de mettre un drapeau sur une case
        renvoie True si le drapeau est bien placé car la case est bein masquée, False sinon'''
        if not self.est_revelee :
            self.est_drapeau = True
        
        return not self.est_revelee
    
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
            return str(self.__valeur)
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
        self.__map = []
        self.__nb_bombe = nb_bombe

    def click(self, x, y) :
        '''Permet de reveler un case de coordonée (x,y)
        (x/y sont des entiers entre 0 et largueur/longueur respectivement)
        renvoie False si on revele une bombe
        renvoie True si le click est hors de la grille ou sur une case sure'''
        if type(x)!=int or type(y)!=int or x<0 or x>=self.__largueur or x<0 or y>=self.__longueur :
            return True
        
        if self.__map==[] :
            self.__premier_click(x, y)
        
        return self.__map[y][x].reveler()

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
            self.__map.append([])
            for i in range(self.__largueur) :
                if (i, j) in bombes :
                    self.__map[j].append(Case(True))
                else :
                    self.__map[j].append(Case(False))

        #mise à jour des valeurs des cases :
        for j in range(self.__longueur) :
            for i in range(self.__largueur) :
                nb_bombes_voisines = 0
                for voisin in self.__voisins(i,j) :
                    if voisin in bombes :
                        nb_bombes_voisines += 1
                self.__map[j][i].set_valeur(nb_bombes_voisines)

        

    def __voisins(self, x, y) :
        '''Renvoie la liste des voisins existants pour une case de coordonée (x,y)'''
        potentiels_voisins = [(x,y),(x,y+1),(x+1,y+1),(x+1,y),(x+1,y-1),(x,y-1),(x-1,y-1),(x-1,y),(x-1,y+1)]
        voisins = []
        for v in potentiels_voisins :
            if v[0]>=0 and v[0]<self.__largueur and v[1]>=0 and v[1]<self.__longueur :
                voisins.append(v)
        return voisins


    def click_droit(self, x, y) :
        '''Permet de click-droit la case(x,y) pour y placer un drapeau
        (x/y sont des entiers entre 0 et largueur/longueur respectivement)
        Renvoie True si le drapeau est bien placé
        False sinon (hors de grille OU case déjà révélée)'''
        if type(x)!=int or type(y)!=int or x<0 or x>=self.__largueur or x<0 or y>=self.__longueur :
            return False
        
        return self.__map[y][x].marquer()

    def affichage(self) :
        '''Renvoie un string pour l'affichage de la grille sur plusieurs lignes'''
        if self.__map == [] :
            return ("# "*self.__largueur + "\n")*self.__longueur
        
        rslt = ""
        for j in range(self.__longueur) :
            for i in range(self.__largueur) :
                rslt += self.__map[j][i].afficher() +" "
            rslt += "\n"

        return rslt

#Création du plateau
p = Plateau(50, 50, 50)  
print(p.affichage())          
assert p.click(2,2)==True
#On peut cliquer sur les 8 cases autour de 2,2
assert p.click(1,1)==True
assert p.click(1,2)==True
assert p.click(1,3)==True
assert p.click(2,3)==True
assert p.click(3,3)==True
assert p.click(3,2)==True
assert p.click(3,1)==True
assert p.click(2,1)==True

#On place un drapeau, tout se passe bien
assert p.click_droit(5,5)==True
print(p.affichage())

#On enlève le drapeau sans problème
assert p.click(5,5)==True

#On prend un risque et on creuse la case ou il y avait le drapeau
p.click(5,5)

print(p.affichage())