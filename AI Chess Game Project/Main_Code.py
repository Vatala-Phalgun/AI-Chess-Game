import ChessEngine as ce
import chess as ch

class Main:

    def __init__(self, board=ch.Board):
        """
        Constructor for the Main class.

        Parameters:
        - board: The chessboard state.
        """
        self.board = board

    def playHumanMove(self):
        """
        Facilitates the human player's move.

        Displays legal moves, provides an option to undo the last move, and updates the board based on user input.
        """
        try:
            print(self.board.legal_moves)
            print("""To undo your last move, type "undo".""")
            # Get human move
            play = input("Your move: ")
            if play == "undo":
                self.board.pop()
                self.board.pop()
                self.playHumanMove()
                return
            self.board.push_san(play)
        except:
            self.playHumanMove()

    def playEngineMove(self, maxDepth, color):
        """
        Initiates the chess engine's move.

        Parameters:
        - maxDepth: Maximum depth for the search algorithm.
        - color: The color of the player controlling the engine.
        """
        engine = ce.Engine(self.board, maxDepth, color)
        self.board.push(engine.getBestMove())

    def startGame(self):
        """
        Initiates and orchestrates a game.

        Allows the human player to select their color and the depth of the engine's analysis.
        Alternates moves between the human player and the engine until a checkmate occurs.
        Resets the board for subsequent games.
        """
        # Get human player's color
        color = None
        while color not in ["b", "w"]:
            color = input("""Play as (type "b" or "w"): """)
        maxDepth = None
        while not isinstance(maxDepth, int):
            maxDepth = int(input("""Choose depth: """))
        if color == "b":
            while not self.board.is_checkmate():
                print("The engine is thinking...")
                self.playEngineMove(maxDepth, ch.WHITE)
                print(self.board)
                self.playHumanMove()
                print(self.board)
            print(self.board)
            print(self.board.outcome())    
        elif color == "w":
            while not self.board.is_checkmate():
                print(self.board)
                self.playHumanMove()
                print(self.board)
                print("The engine is thinking...")
                self.playEngineMove(maxDepth, ch.BLACK)
            print(self.board)
            print(self.board.outcome())
        # Reset the board
        self.board.reset
        # Start another game
        self.startGame()

# Create an instance and start a game
newBoard = ch.Board()
game = Main(newBoard)
bruh = game.startGame()
