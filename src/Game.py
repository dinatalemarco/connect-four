
import random
from Human import Human
from Intelligence import Intelligence


class Game(object):
    
    MATRIX = None
    ROUND = None
    END = False
    WINNER = None
    PLAYERS = [None, None]
    SIMBOL = ["X", "O"]

    def __init__(self, player1="H", palyer2="I"):
        self.ROUND = 1
        self.END = False
        self.WINNER = None

        # display PLAYERS's status
        print "#############################################"
        print "##### Home Work 2 Artificial Intelligent ####"
        print "##### Realizzato da:                     ####"
        print "##### Ciavarro Cristina                  ####"
        print "##### Di Natale Marco                    ####"
        print "#############################################\n"        
        
        if player1 == "H" and palyer2 == "I":
            name = raw_input("Sei il giocatore 1 digita il tuo nome: ")
            self.PLAYERS[0] = Human(name,self.SIMBOL[0])
            self.PLAYERS[1] = Intelligence("Artificial Intelligence", self.SIMBOL[1])
        elif player1== "I" and palyer2 == "I":
            self.PLAYERS[0] = Intelligence("Artificial Intelligence (1)", self.SIMBOL[0]) 
            self.PLAYERS[1] = Intelligence("Artificial Intelligence (2)", self.SIMBOL[1]) 
        elif player1 == "H" and palyer2 == "H":
            name1 = raw_input("Digita il nome del giocatore 1: ")
            self.PLAYERS[0] = Human(name1, self.SIMBOL[0])
            name2 = raw_input("Digita il nome del giocatore 2: ")
            self.PLAYERS[1] = Human(name2, self.SIMBOL[1])            
        else:
            name = raw_input("Sei il giocatore 1 digita il tuo nome: ")
            self.PLAYERS[0] = Human(name, self.SIMBOL[0])
            self.PLAYERS[1] = Intelligence("Artificial Intelligence", self.SIMBOL[1])
            
        
        for i in xrange(2):
            print('%s gioca con ( %s ) ' % (self.PLAYERS[i].NamePlayer, self.SIMBOL[i]))
        print "#############################################"
        # choose the first player randomly
        self._current_player = self.PLAYERS[random.randint(0, 1)]
        # init grid with white spaces
        self.MATRIX = []
        for i in xrange(6):
            self.MATRIX.append([])
            for j in xrange(7):
                self.MATRIX[i].append(' ')

    # Se invocato permette di avviare il gioco
    def Start(self):
        # Stampo la matrice vuota
        self.PrintState()
        while not self.END:
            self.NextMove()

    # Cambia il giocatore durante le fasi di gio
    def SwitchPlayer(self):
        if self._current_player == self.PLAYERS[0]:
            self._current_player = self.PLAYERS[1]
        else:
            self._current_player = self.PLAYERS[0]

    def NextMove(self):

        # get the "move" (column) that the player played
        column = self._current_player.get_move(self.MATRIX)
        # search the available line in the selected column
        for i in xrange(6 - 1, -1, -1):
            if self.MATRIX[i][column] == ' ':
                # set the color in the grid
                self.MATRIX[i][column] = self._current_player.SimbolPalyer
                self.CheckStatus()
                self.PrintState()
                # swith player
                self.SwitchPlayer()
                # increment the round
                self.ROUND += 1
                return

        # column selected is full
        print("Colonna piena! Scegliere una colonna libera")
        return

    def CheckStatus(self):
        if self.isFull():
            self.END = True
        elif self.isConnect():
            self.END = True
            self.WINNER = self._current_player

    def isFull(self):
        # the number of round can't be superior to the number of case of the grid
        return self.ROUND > 7 * 6

    def isConnect(self):
        # for each box of the grid
        for i in xrange(6 - 1, -1, -1):
            for j in xrange(7):
                if self.MATRIX[i][j] != ' ':
                    # check for vertical connect four
                    if self.FindVertical(i, j):
                        return True

                    # check for horizontal connect four
                    if self.FindHorizontal(i, j):
                        return True

                    # check for diagonal connect four
                    if self.FindDiagonal(i, j):
                        return True

        return False

    def FindVertical(self, row, col):
        consecutive_count = 0

        if row + 3 < 6:
            for i in xrange(4):
                if self.MATRIX[row][col] == self.MATRIX[row + i][col]:
                    consecutive_count += 1
                else:
                    break

            # define the winner
            if consecutive_count == 4:
                if self.PLAYERS[0].SimbolPalyer == self.MATRIX[row][col]:
                    self.WINNER = self.PLAYERS[0]
                else:
                    self.WINNER = self.PLAYERS[1]
                return True

        return False

    def FindHorizontal(self, row, col):

        consecutive_count = 0

        if col + 3 < 7:
            for i in xrange(4):
                if self.MATRIX[row][col] == self.MATRIX[row][col + i]:
                    consecutive_count += 1
                else:
                    break

            # define the winner
            if consecutive_count == 4:
                if self.PLAYERS[0].SimbolPalyer == self.MATRIX[row][col]:
                    self.WINNER = self.PLAYERS[0]
                else:
                    self.WINNER = self.PLAYERS[1]
                return True

        return False

    def FindDiagonal(self, row, col):

        consecutive_count = 0
        # check positive slope
        if row + 3 < 6 and col + 3 < 7:
            for i in xrange(4):
                if self.MATRIX[row][col] == self.MATRIX[row + i][col + i]:
                    consecutive_count += 1
                else:
                    break

            # define the winner
            if consecutive_count == 4:
                if self.PLAYERS[0].SimbolPalyer == self.MATRIX[row][col]:
                    self.WINNER = self.PLAYERS[0]
                else:
                    self.WINNER = self.PLAYERS[1]
                return True

        consecutive_count = 0
        # check negative slope
        if row - 3 >= 0 and col + 3 < 7:
            for i in xrange(4):
                if self.MATRIX[row][col] == self.MATRIX[row - i][col + i]:
                    consecutive_count += 1
                else:
                    break

            # define the winner
            if consecutive_count == 4:
                if self.PLAYERS[0].SimbolPalyer == self.MATRIX[row][col]:
                    self.WINNER = self.PLAYERS[0]
                else:
                    self.WINNER = self.PLAYERS[1]
                return True

        return False

    def PrintState(self):

        # print the round
        print("")
        print "#############################"
        print "## ROUND %s                ##" % (str(self.ROUND))
        print "#############################"
        print("")
        # print the grid
        for i in xrange(6):
            
            for j in xrange(7):
                print("| " + str(self.MATRIX[i][j])),
            print("|")
        
        print "#############################"

        for k in xrange(7):
            print("  %d" % (k + 1)),
        print "\n#############################"
        print("")
        # print final message when the game is finished
        if self.END:
            print ""
            print "-------------------------------------------"

            if self.WINNER != None:
                print("---- "+str(self.WINNER.NamePlayer) + " e' il vincitore!")
            else:
                print("Game is a draw")
            print "------------------------------------------"





