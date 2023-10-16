#fonctionnel sans récursivité

import random
from collections import deque
from time import process_time_ns
from math import floor

class Case:
    def __init__(self):
        self.has_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

class Demineur:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.grid = [[Case() for _ in range(cols)] for _ in range(rows)]
        self.first_click = True
    
    def generate_mines(self, first_row, first_col):
        # Place les mines aléatoirement, en excluant la première case cliquée
        mines_placed = 0
        safe_cells = []
        for r in range(max(0, first_row - 1), min(self.rows, first_row + 2)):
            for c in range(max(0, first_col - 1), min(self.cols, first_col + 2)):
                safe_cells.append((r, c))

        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.grid[row][col].has_mine and (row, col) not in safe_cells:
                self.grid[row][col].has_mine = True
                mines_placed += 1
                self.increment_adjacent_cells(row, col)
    
    def increment_adjacent_cells(self, row, col):
        # Incrémente le nombre de mines adjacentes à chaque cellule
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.cols, col + 2)):
                self.grid[r][c].adjacent_mines += 1
    
    def display_grid(self):
        # Affiche la grille en fonction de l'état des cases, avec numéros de ligne et de colonne
        header = "  " + " ".join(str(i) for i in range(self.cols))
        print(header)
        for i, row in enumerate(self.grid):
            row_str = str(i) + " "
            for cell in row:
                if cell.is_revealed:
                    if cell.has_mine:
                        row_str += "* "
                    else:
                        row_str += str(cell.adjacent_mines) + " "
                elif cell.is_flagged:
                    row_str += "F "
                else:
                    row_str += "X "
            print(row_str)
    
    def reveal_cell(self, row, col):
        # Révèle une cellule et révèle automatiquement les voisins si la cellule a une valeur de 0 (approche itérative)
        stack = deque([(row, col)])
        while stack:
            r, c = stack.pop()
            cell = self.grid[r][c]
            if not cell.is_revealed and not cell.is_flagged:
                cell.is_revealed = True
                if cell.adjacent_mines == 0:
                    for rr in range(max(0, r - 1), min(self.rows, r + 2)):
                        for cc in range(max(0, c - 1), min(self.cols, c + 2)):
                            stack.append((rr, cc))
    
    def toggle_flag(self, row, col):
        # Met en drapeau ou retire le drapeau d'une cellule
        cell = self.grid[row][col]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged

    def play(self):
        self.display_grid()
        while True:
            try:
                row = int(input("Entrez le numéro de ligne : "))
                col = int(input("Entrez le numéro de colonne : "))
                if not (0 <= row < self.rows) or not (0 <= col < self.cols):
                    print("Coordonnées non valides. Réessayez.")
                    continue
                if self.first_click:
                    self.generate_mines(row, col)
                    self.first_click = False
                action = input("Révéler (R) ou mettre en drapeau (F) ? ").upper()
                if action == "R":
                    if not self.reveal_cell(row, col):
                        print("Vous avez perdu !")
                        self.display_grid()
                        break
                    elif all(cell.is_revealed or cell.has_mine for row in self.grid for cell in row):
                        print("Bravo ! Vous avez gagné !")
                        self.display_grid()
                        break
                elif action == "F":
                    self.toggle_flag(row, col)
                else:
                    print("Action non valide. Réessayez.")
                self.display_grid()
            except ValueError:
                print("Entrée invalide. Réessayez.")

# Exemple d'utilisation
if __name__ == "__main__":
    d = Demineur(20,20,100)
    d.play()