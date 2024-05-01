import chess as ch
import random as rd

class Engine:

    def __init__(self, board, maxDepth, color):
        """
        Constructor for the Engine class.

        Parameters:
        - board: The chessboard state.
        - maxDepth: Maximum depth for the search algorithm.
        - color: The color of the player controlling the engine.
        """
        self.board = board
        self.color = color
        self.maxDepth = maxDepth
    
    def getBestMove(self):
        """
        Initiates the engine to find the best move.

        Returns:
        The best move calculated by the engine.
        """
        return self.engine(None, 1)

    def evalFunct(self):
        """
        Calculates an evaluation score for the current board position.

        Returns:
        The evaluation score.
        """
        compt = 0
        # Sums up the material values
        for i in range(64):
            compt += self.squareResPoints(ch.SQUARES[i])
        compt += self.mateOpportunity() + self.openning() + 0.001 * rd.random()
        return compt

    def mateOpportunity(self):
        """
        Checks for checkmate opportunities.

        Returns:
        A high or low score based on the color of the player.
        """
        if self.board.legal_moves.count() == 0:
            if self.board.turn == self.color:
                return -999
            else:
                return 999
        else:
            return 0

    def openning(self):
        """
        Encourages the engine to make developmental moves in the opening phase.

        Returns:
        A score adjustment based on the player's turn.
        """
        # To make the engine develop in the first moves
        if self.board.fullmove_number < 10:
            if self.board.turn == self.color:
                return 1 / 30 * self.board.legal_moves.count()
            else:
                return -1 / 30 * self.board.legal_moves.count()
        else:
            return 0

    def squareResPoints(self, square):
        """
        Takes a square as input and returns the corresponding value of its resident.

        Parameters:
        - square: The square on the chessboard.

        Returns:
        The value of the piece on the given square.
        """
        pieceValue = 0
        if self.board.piece_type_at(square) == ch.PAWN:
            pieceValue = 1
        elif self.board.piece_type_at(square) == ch.ROOK:
            pieceValue = 5.1
        elif self.board.piece_type_at(square) == ch.BISHOP:
            pieceValue = 3.33
        elif self.board.piece_type_at(square) == ch.KNIGHT:
            pieceValue = 3.2
        elif self.board.piece_type_at(square) == ch.QUEEN:
            pieceValue = 8.8

        if self.board.color_at(square) != self.color:
            return -pieceValue
        else:
            return pieceValue

    def engine(self, candidate, depth):
        """
        The engine's recursive method implementing the minimax algorithm with alpha-beta pruning.

        Parameters:
        - candidate: The best candidate move.
        - depth: The depth of the search tree.

        Returns:
        The evaluation score or the best move, depending on the depth.
        """
        # Reached max depth of search or no possible moves
        if depth == self.maxDepth or self.board.legal_moves.count() == 0:
            return self.evalFunct()
        else:
            # Get list of legal moves of the current position
            moveListe = list(self.board.legal_moves)
            
            # Initialize newCandidate
            newCandidate = None
            # Uneven depth means engine's turn
            if depth % 2 != 0:
                newCandidate = float("-inf")
            else:
                newCandidate = float("inf")
            
            # Analyze board after deeper moves
            for i in moveListe:

                # Play move i
                self.board.push(i)

                # Get value of move i (by exploring the repercussions)
                value = self.engine(newCandidate, depth + 1) 

                # Basic minmax algorithm:
                # If maximizing (engine's turn)
                if value > newCandidate and depth % 2 != 0:
                    # Need to save move played by the engine
                    if depth == 1:
                        move = i
                    newCandidate = value
                # If minimizing (human player's turn)
                elif value < newCandidate and depth % 2 == 0:
                    newCandidate = value

                # Alpha-beta pruning cuts: 
                # (if the previous move was made by the engine)
                if candidate is not None and value < candidate and depth % 2 == 0:
                    self.board.pop()
                    break
                # (if the previous move was made by the human player)
                elif candidate is not None and value > candidate and depth % 2 != 0:
                    self.board.pop()
                    break
                
                # Undo last move
                self.board.pop()

            # Return result
            if depth > 1:
                # Return value of a move in the tree
                return newCandidate
            else:
                # Return the move (only on the first move)
                return move
