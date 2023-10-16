#version 0.4 : lancement d'une partie et gestion de l'input

from random import randint
from os import system
from math import floor
from time import process_time_ns
import sys

sys.setrecursionlimit(1000000)
from math import log10, floor
from time import process_time_ns

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
        '''Obtient la valeur de la case si elle est révélée, -1 sinon'''
        if self.est_revelee :
            return self.__valeur
        return -1
    
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
        self.__a_cliquer = []

    def click(self, x, y) :
        '''Permet de reveler un case de coordonée (x,y)
        (x/y sont des entiers entre 0 et largueur/longueur respectivement)
        renvoie False si on revele une bombe
        renvoie True si le click est hors de la grille ou sur une case sure'''
        if type(x)!=int or type(y)!=int or x<0 or x>=self.__largueur or x<0 or y>=self.__longueur :
            return True
        
        if self.__map==[] :
            self.__premier_click(x, y)
        
        rslt = self.__map[y][x].reveler()

        if rslt and self.__map[y][x].get_valeur()==0 :
            for voisin in self.__voisins(x,y) :
                if self.__map[voisin[1]][voisin[0]].get_valeur()==-1:
                    self.click(voisin[0],voisin[1])

        return rslt

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
        if type(x)!=int or type(y)!=int or x<0 or x>=self.__largueur or x<0 or y>=self.__longueur or self.__map==[] :
            return False
        
        return self.__map[y][x].marquer()

    def affichage(self) :
        '''Renvoie un string pour l'affichage de la grille sur plusieurs lignes'''
        map0 = False
        if self.__map == [] :
            map0 = True
        
        rslt = ""
        espacement_vertrical = floor(log10(self.__largueur-1))+1
        espacement_d_ligne = floor(log10(self.__longueur-1))+1
        rslt += " "*(espacement_d_ligne+3)
        for i in range(self.__largueur) :
            rslt += formatint(i, espacement_vertrical)+" "
        rslt += "\n"
        rslt += " "*(espacement_d_ligne+3)+"-"*(espacement_vertrical+1)*self.__largueur+"\n"

        for j in range(self.__longueur) :
            rslt += f"{formatint(j, espacement_d_ligne)} | "
            for i in range(self.__largueur) :
                if map0 :
                    rslt += "#"
                else :
                    rslt += self.__map[j][i].afficher()
                rslt += espacement_vertrical*" "
            rslt += "\n"

        if not "#" in rslt and rslt.count("P")==self.__nb_bombe :
            return rslt + "\n\n!!! Vous avez gagné !!!!"

        return rslt

def formatint(number, n) :
    number = str(number)
    if len(number)>n :
        return "0"*n
    else :
        return "0"*(n-len(number))+number

def jouer(largueur,longueur, nb_bombe) :
    p = Plateau(largueur, longueur, nb_bombe)
    while True :
        system('cls')

        afficher = p.affichage()
        if afficher[-1]=="!" :
            print(afficher)
            break
        print(afficher)
        try :
            action, x, y = input("Saisir 0(drapeau) ou 1(creuser) puis les coordonnées x y de la case\n/!\ tous les nombres doivent être séparés par des espaces :\n").split(" ")
            action = bool(int(action))
            x, y = int(x), int(y)
        except ValueError :
            continue
        
        if action :
            rslt = p.click(x,y)
            if not rslt :
                print("Perdu, apprend à viser !!!")
                break
        else :
            p.click_droit(x,y)

        
jouer(10,10,10)