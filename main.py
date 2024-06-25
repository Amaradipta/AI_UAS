import streamlit as st
import chess
import chess.svg
import cairosvg
from PIL import Image
import io

class ChessAI:
    def __init__(self, depth):
        self.depth = depth

    def evaluate_board(self, board):
        evaluation = 0
        for (piece, value) in [
            (chess.PAWN, 1),
            (chess.KNIGHT, 3),
            (chess.BISHOP, 3),
            (chess.ROOK, 5),
            (chess.QUEEN, 9),
            (chess.KING, 0)
        ]:
            evaluation += len(board.pieces(piece, chess.WHITE)) * value
            evaluation -= len(board.pieces(piece, chess.BLACK)) * value
        return evaluation

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        legal_moves = list(board.legal_moves)

        if is_maximizing:
            max_eval = -float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta is min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def select_move(self, board):
        best_move = None
        best_value = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        for move in board.legal_moves:
            board.push(move)
            board_value = self.minimax(board, self.depth - 1, alpha, beta, False)
            board.pop()
            if board_value > best_value:
                best_value = board_value
                best_move = move

        return best_move

class ChessApp:
    def __init__(self):
        self.board = chess.Board()
        self.ai = ChessAI(depth=3)  # Initialize your AI

    def render_board(self):
        board_svg = chess.svg.board(self.board)
        board_png = cairosvg.svg2png(bytestring=board_svg.encode('utf-8'))
        board_image = Image.open(io.BytesIO(board_png))
        return board_image

    def make_ai_move(self):
        if not self.board.is_game_over():
            move = self.ai.select_move(self.board)
            self.board.push(move)

    def main(self):
        st.title("Chess with AI")
        st.write("Play chess against an AI")

        st.image(self.render_board(), use_column_width=True)

        user_move = st.text_input("Your move (e.g., e2e4):")

        if st.button("Make move"):
            try:
                move = chess.Move.from_uci(user_move)
                if move in self.board.legal_moves:
                    self.board.push(move)
                    self.make_ai_move()
                    st.image(self.render_board(), use_column_width=True)
                else:
                    st.write("Invalid move! Please try again.")
            except ValueError:
                st.write("Invalid move format! Please enter in UCI format (e.g., e2e4).")

if __name__ == "__main__":
    chess_app = ChessApp()
    chess_app.main()
