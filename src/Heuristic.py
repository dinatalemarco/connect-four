from Player import Player


class Heuristic(Player):
    

    def __init__(self, Intel):
        self.Intelligent = Intel


    def MinMax(self, depth, matrix, curr_player_simbol):

        legal_moves = []
        for i in xrange(6):
            if self.Intelligent.isLegalMove(i, matrix):
                # simulate the move in column i for curr_player
                tmp_matrix = self.Intelligent._simulate_move(matrix, i, curr_player_simbol)
                legal_moves.append(tmp_matrix)


        if depth == 0 or len(legal_moves) == 0 or self.Intelligent.GameOver(matrix):
            # return the heuristic value of node
            return self.Intelligent._eval_game(depth, matrix, curr_player_simbol)


        # Assegnamo il nuovo simbolo
        if curr_player_simbol == self.Intelligent.SIMBOL[1]:
            set_player_simbol = self.Intelligent.SIMBOL[0] # Setto il nuovo simbolo 
            return max([self.MinMax(depth-1, child, set_player_simbol) for child in legal_moves])
        else:
            set_player_simbol = self.Intelligent.SIMBOL[1] # Setto il nuovo simbolo 
            return min([self.MinMax(depth-1, child, set_player_simbol) for child in legal_moves])


