#version 0.1 : Créer la classe Case

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
        


#initialisation
case1 = Case(False)
case2 = Case(True)
case3 = Case(True)
case1.set_valeur(1)
case2.set_valeur(1)
case3.set_valeur(1)
case3.est_drapeau = True

#test
assert case1.afficher()=="#"
assert case2.afficher()=="#"
assert case1.get_valeur()==False
assert case1.reveler()==True
assert case1.get_valeur()==1
assert case2.reveler()==False #perdu
assert case3.afficher()=="P"
assert case3.reveler()==False
assert case3.est_drapeau==False
assert case3.est_revelee==False