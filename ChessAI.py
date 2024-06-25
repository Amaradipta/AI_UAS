import tkinter as tk
from tkinter import messagebox
import chess

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Catur dengan AI")
        
        self.board = chess.Board()
        self.ai = ChessAI(depth=3)
        
        self.canvas = tk.Canvas(root, width=480, height=480)
        self.canvas.pack()
        
        self.square_size = 60
        self.selected_square = None
        
        self.canvas.bind("<Button-1>", self.on_square_click)
        
        self.draw_board()
        self.update_board()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = 'white' if (row + col) % 2 == 0 else 'gray'
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    def update_board(self):
        self.canvas.delete("piece")
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                x = (square % 8) * self.square_size + self.square_size // 2
                y = (7 - square // 8) * self.square_size + self.square_size // 2
                self.canvas.create_text(x, y, text=piece.symbol(), tags="piece", font=("Helvetica", 32))
        self.check_game_status()

    def check_game_status(self):
        if self.board.is_checkmate():
            messagebox.showinfo("Game Over", "Checkmate! You lost.")
        elif self.board.is_stalemate():
            messagebox.showinfo("Game Over", "Stalemate! It's a draw.")
        elif self.board.is_insufficient_material():
            messagebox.showinfo("Game Over", "Draw due to insufficient material.")
        elif self.board.is_seventyfive_moves():
            messagebox.showinfo("Game Over", "Draw due to the seventy-five-move rule.")
        elif self.board.is_fivefold_repetition():
            messagebox.showinfo("Game Over", "Draw due to fivefold repetition.")

    def on_square_click(self, event):
        col = event.x // self.square_size
        row = 7 - event.y // self.square_size
        square = chess.square(col, row)
        
        if self.selected_square is None:
            if self.board.piece_at(square) and self.board.piece_at(square).color == chess.WHITE:
                self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.update_board()
                self.root.after(100, self.ai_move)
            else:
                self.selected_square = None

    def ai_move(self):
        if not self.board.is_game_over():
            move = self.ai.select_move(self.board)
            self.board.push(move)
            self.update_board()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()