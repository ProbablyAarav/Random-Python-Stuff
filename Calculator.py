import tkinter as tk

class TI84Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("TI-84 Calculator")
        self.root.resizable(False, False)
        self.display = tk.Entry(root, font=('Helvetica', 24), bd=10, insertwidth=2, width=14, borderwidth=4, relief="ridge")
        self.display.grid(row=0, column=0, columnspan=4)
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', '(', ')', '^'
        ]
        row_val = 1
        col_val = 0
        for button in buttons:
            self.create_button(button, row_val, col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1
    def create_button(self, value, row, col):
        button = tk.Button(self.root, text=value, padx=20, pady=20, font=('Helvetica', 18), command=lambda: self.on_button_click(value))
        button.grid(row=row, column=col)
    def on_button_click(self, value):
        current_text = self.display.get()
        if value == "C":
            self.display.delete(0, tk.END)
        elif value == "=":
            try:
                result = eval(current_text.replace('^', '**'))
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(0, "Error")
        else:
            self.display.insert(tk.END, value)
if __name__ == "__main__":
    root = tk.Tk()
    calculator = TI84Calculator(root)
    root.mainloop()
