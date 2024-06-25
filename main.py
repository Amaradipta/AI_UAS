import streamlit as st
import chess
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

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
                beta = min(beta, eval)
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

board = chess.Board()
ai = ChessAI(depth=3)

def render_board(board):
    svg_board = chess.svg.board(board)

    drawing = svg2rlg(io.BytesIO(svg_board.encode('utf-8')))
    img = Image.new("RGB", drawing.getBounds()[2:])
    renderPM.drawToFile(drawing, img)

    return img

st.title("Chess with AI")
st.write("Play chess against an AI")

st.image(render_board(board), use_column_width=True)

user_move = st.text_input("Your move (e.g., e2e4):")

if st.button("Make move"):
    try:
        move = chess.Move.from_uci(user_move)
        if move in board.legal_moves:
            board.push(move)
            if not board.is_game_over():
                ai_move = ai.select_move(board)
                board.push(ai_move)
            st.image(render_board(board), use_column_width=True)
        else:
            st.write("Invalid move! Please try again.")
    except ValueError:
        st.write("Invalid move format! Please enter in UCI format (e.g., e2e4).")

if board.is_checkmate():
    st.write("Checkmate! Game over.")
elif board.is_stalemate():
    st.write("Stalemate! Game over.")
elif board.is_insufficient_material():
    st.write("Draw due to insufficient material.")
elif board.is_seventyfive_moves():
    st.write("Draw due to the seventy-five-move rule.")
elif board.is_fivefold_repetition():
    st.write("Draw due to fivefold repetition.")
