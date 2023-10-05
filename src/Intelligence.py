import time
from Player import Player
from Heuristic import Heuristic


class Intelligence(Player):

    SIMBOL = ["X", "O"]

    # Assegna al Player Artificial Intelligence una pedina di gioco
    def __init__(self, type, simbol):       
        super(Intelligence, self).__init__(simbol)
        self.NamePlayer = type

    # get_move viene invocato come metodo predefinito per la gestione delle pedine nella matrice
    # nel caso seguente il metodo get_move invoca un euristica per gestire l'inserimento, mentre
    # nella classe Human invoca la lettura da terminale, per consentire l'input all'utente
    def get_move(self, matrix):  

        # misuriamo il tempo di calcolo dell'algoritmo MinMax
        start_time = int(round(time.time() * 1000))
        # determina la pedina dell'avversario
        if self.SimbolPalyer == self.SIMBOL[0]:
            human_simbol = self.SIMBOL[1]
        else:
            human_simbol = self.SIMBOL[0]

        # elenca tutte le mosse consentite
        # mappa gli stati dei movimenti legati ai loro valori
        legal_moves = {}
        # verifica se la mossa e legale per ogni colonna
        for col in xrange(7):
            if self.isLegalMove(col, matrix):
                # simula la mossa nella colonna per il giocatore corrente
                tmp_matrix = self._simulate_move(matrix, col, self.SimbolPalyer)

                # INVOCHIAMO LA FUNZIONE MinMax #
                legal_moves[col] = Heuristic(self).MinMax(4, tmp_matrix, human_simbol)


        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        # cerca il miglio spostamento con il valore piu alto
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        end_time = int(round(time.time() * 1000))
        print "Tempo di risposta : %d" % (end_time - start_time)

        return best_move


    # Verifichiamo che una mossa su una colonna della matrice sia consentita    
    def isLegalMove(self, column, matrix):        
        for i in xrange(6 - 1, -1, -1):
            if matrix[i][column] == ' ':
                # once we find the first empty, we know it's a legal move
                return True
        # if we get here, the column is full
        return False


    def GameOver(self, matrix):
        if self.FindCombination(matrix, self.SIMBOL[0], 4) > 0:
            return True
        elif self.FindCombination(matrix, self.SIMBOL[1], 4) > 0:
            return True
        else:
            return False

    def _simulate_move(self, matrix, column, color):

        tmp_matrix = [x[:] for x in matrix]
        for i in xrange(6 - 1, -1, -1):
            if tmp_matrix[i][column] == ' ':
                tmp_matrix[i][column] = color
                return tmp_matrix

    def _eval_game(self, depth, matrix, player_simbol):

        if player_simbol == self.SIMBOL[0]:
            opp_color = self.SIMBOL[1]
        else:
            opp_color = self.SIMBOL[0]
        # get scores of human and IA player with theirs streaks
        ia_fours = self.FindCombination(matrix, player_simbol, 4)
        ia_threes = self.FindCombination(matrix, player_simbol, 3)
        ia_twos = self.FindCombination(matrix, player_simbol, 2)
        human_fours = self.FindCombination(matrix, opp_color, 4)
        human_threes = self.FindCombination(matrix, opp_color, 3)
        human_twos = self.FindCombination(matrix, opp_color, 2)
        # calculate and return the alpha
        if human_fours > 0:
            return -100000 - depth
        else:
            return (ia_fours * 100000 + ia_threes * 100 + ia_twos * 10) - (human_threes * 100 + human_twos * 10) + depth


    def FindCombination(self, matrix, color, streak):

        count = 0
        # for each box in the matrix...
        for i in xrange(6):
            for j in xrange(7):
                # ...that is of the color we're looking for...
                if matrix[i][j] == color:
                    # check if a vertical streak starts at index [i][j] of the matrix game
                    count += self.FindsVerticalCombination(i, j, matrix, streak)

                    # check if a horizontal streak starts at index [i][j] of the matrix game
                    count += self.FindsHorizontalCombination(i, j, matrix, streak)

                    # check if a diagonal streak starts at index [i][j] of the matrix game
                    count += self.FindsDiagonalCombination(i, j, matrix, streak)
        # return the sum of streaks of length 'streak'

        return count

    def FindsVerticalCombination(self, row, col, matrix, streak):

        consecutive_count = 0
        if row + streak - 1 < 6:
            for i in xrange(streak):
                if matrix[row][col] == matrix[row + i][col]:
                    consecutive_count += 1
                else:
                    break

        if consecutive_count == streak:
            return 1
        else:
            return 0

    def FindsHorizontalCombination(self, row, col, matrix, streak):
        consecutive_count = 0
        if col + streak - 1 < 7:
            for i in xrange(streak):
                if matrix[row][col] == matrix[row][col + i]:
                    consecutive_count += 1
                else:
                    break

        if consecutive_count == streak:
            return 1
        else:
            return 0

    def FindsDiagonalCombination(self, row, col, matrix, streak):
        total = 0
        # check for diagonals with positive slope
        consecutive_count = 0
        if row + streak - 1 < 6 and col + streak - 1 < 7:
            for i in xrange(streak):
                if matrix[row][col] == matrix[row + i][col + i]:
                    consecutive_count += 1
                else:
                    break

        if consecutive_count == streak:
            total += 1

        # check for diagonals with negative slope
        consecutive_count = 0
        if row - streak + 1 >= 0 and col + streak - 1 < 7:
            for i in xrange(streak):
                if matrix[row][col] == matrix[row - i][col + i]:
                    consecutive_count += 1
                else:
                    break

        if consecutive_count == streak:
            total += 1

        return total