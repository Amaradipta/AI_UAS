import streamlit as st
import chess
import ChessAI

class StreamlitChessApp:
    def __init__(self):
        self.board = chess.Board()
        self.ai = ChessAI(depth=3)

    def render_board(self):
        st.write("### Chess Board")
        board_svg = chess.svg.board(self.board, size=400)
        st.image(board_svg, use_column_width=True, format='svg')

    def run(self):
        st.title("Chess with AI")
        self.render_board()
        
        user_move = st.text_input("Your move (e.g., e2e4):")
        if st.button("Make move"):
            try:
                move = chess.Move.from_uci(user_move.strip())
                if move in self.board.legal_moves:
                    self.board.push(move)
                    if not self.board.is_game_over():
                        ai_move = self.ai.select_move(self.board)
                        self.board.push(ai_move)
                    self.render_board()
                else:
                    st.warning("Invalid move! Please try again.")
            except ValueError:
                st.warning("Invalid move format! Please enter in UCI format (e.g., e2e4).")

        if self.board.is_checkmate():
            st.warning("Checkmate! Game over.")
        elif self.board.is_stalemate():
            st.warning("Stalemate! Game over.")
        elif self.board.is_insufficient_material():
            st.warning("Draw due to insufficient material.")
        elif self.board.is_seventyfive_moves():
            st.warning("Draw due to the seventy-five-move rule.")
        elif self.board.is_fivefold_repetition():
            st.warning("Draw due to fivefold repetition.")

if __name__ == "__main__":
    app = StreamlitChessApp()
    app.run()
