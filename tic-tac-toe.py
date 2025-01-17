
import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.current_player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def create_board(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text="", font=('normal', 40), width=5, height=2,
                                   command=lambda r=row, c=col: self.click_button(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def click_button(self, row, col):
        if self.buttons[row][col]["text"] == "" and self.current_player != "":
            self.buttons[row][col]["text"] = self.current_player
            if self.check_win(self.current_player):
                self.end_game(f"Player {self.current_player} wins!")
            elif self.check_draw():
                self.end_game("It's a draw!")
            else:
                self.current_player = "O" if self.current_player == "X" else "X"

    def check_win(self, player):
        for row in range(3):
            if all(self.buttons[row][col]["text"] == player for col in range(3)):
                return True
        for col in range(3):
            if all(self.buttons[row][col]["text"] == player for row in range(3)):
                return True
        if all(self.buttons[i][i]["text"] == player for i in range(3)):
            return True
        if all(self.buttons[i][2-i]["text"] == player for i in range(3)):
            return True
        return False

    def check_draw(self):
        return all(self.buttons[row][col]["text"] != "" for row in range(3) for col in range(3))

    def end_game(self, message):
        messagebox.showinfo("Game Over", message)
        self.current_player = ""
        self.root.after(2000, self.reset_board)

    def reset_board(self):
        self.current_player = "X"
        for row in range(3):
            for col in range(3):
                self.buttons[row][col]["text"] = ""

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
