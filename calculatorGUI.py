
import tkinter as tk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.current_input = ""

        self.display = tk.Entry(self.root, font=('Arial', 24), borderwidth=2, relief="solid", justify='right')
        self.display.grid(row=0, column=0, columnspan=4, pady=10)

        buttons = [
            '7', '8', '9', '/', 
            '4', '5', '6', '*', 
            '1', '2', '3', '-', 
            '0', '.', '=', '+'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            tk.Button(self.root, text=button, font=('Arial', 18), command=lambda b=button: self.on_button_click(b)).grid(row=row_val, column=col_val, ipadx=10, ipady=10, padx=5, pady=5)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        clear_button = tk.Button(self.root, text='C', font=('Arial', 18), command=self.clear_display)
        clear_button.grid(row=row_val, column=0, columnspan=4, sticky="nsew", ipadx=10, ipady=10, padx=5, pady=5)

    def on_button_click(self, button):
        if button == "=":
            try:
                self.current_input = str(eval(self.current_input))
            except Exception as e:
                self.current_input = "Error"
        elif button == "C":
            self.current_input = ""
        else:
            self.current_input += button
        self.update_display()

    def clear_display(self):
        self.current_input = ""
        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current_input)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
