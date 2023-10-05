# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from Player import Player

class Human(Player):

    def __init__(self, type, simbo):
        super(Human, self).__init__(simbo)
        self.NamePlayer = type

    # Gestisce l'inserimento da consolle da parte dell'utente
    # get_mode nella classe Intelligent invoca l'euristica MinMax
    def get_move(self, matrix):

        column = None
        while column == None:
            try:
                column = int(raw_input("E' il tuo Turno : ")) - 1
            except ValueError:
                column = None
            if 0 <= column <= 6:
                return column
            else:
                column = None
                print("Inserisci un numero tra 1 e 7")
