import ast
import operator
import tkinter as tk
import re


class Calculator:
    def __init__(self, root):
        self.root = root
        root.title("Calculator")
        root.resizable(False, False)
        self.expression = ""
        self.just_calculated = False

        self.display = tk.Entry(root, font=("Consolas", 24), justify="right", width=18,
                                state="readonly", readonlybackground="#202b41",
                                foreground="white", relief="flat", bd=0)
        self.display.grid(row=0, column=0, columnspan=4, padx=12, pady=12, ipady=18)
        self.refresh()

        buttons = [
            ("AC", "clear"), ("+/-", "sign"), ("%", "percent"), ("/", "/"),
            ("7", "7"), ("8", "8"), ("9", "9"), ("*", "*"),
            ("4", "4"), ("5", "5"), ("6", "6"), ("-", "-"),
            ("1", "1"), ("2", "2"), ("3", "3"), ("+", "+"),
            ("0", "0"), (".", "decimal"), ("=", "equals"),
        ]
        for index, (label, action) in enumerate(buttons):
            row, col = divmod(index, 4)
            if label == ".":
                col = 1
            elif label == "=":
                col = 3
            button = tk.Button(root, text=label, font=("Segoe UI", 16, "bold"),
                               width=5, height=2, command=lambda a=action: self.press(a))
            button.grid(row=row + 1, column=col, padx=5, pady=5, sticky="nsew")
        self.root.bind("<Key>", self.on_key)

    def refresh(self):
        self.display.configure(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression or "0")
        self.display.xview_moveto(1)
        self.display.configure(state="readonly")

    @staticmethod
    def evaluate(text):
        """Evaluate basic arithmetic without executing arbitrary Python code."""
        tree = ast.parse(text, mode="eval")
        binary = {ast.Add: operator.add, ast.Sub: operator.sub,
                  ast.Mult: operator.mul, ast.Div: operator.truediv}
        unary = {ast.UAdd: operator.pos, ast.USub: operator.neg}

        def visit(node):
            if isinstance(node, ast.Expression):
                return visit(node.body)
            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return node.value
            if isinstance(node, ast.BinOp) and type(node.op) in binary:
                return binary[type(node.op)](visit(node.left), visit(node.right))
            if isinstance(node, ast.UnaryOp) and type(node.op) in unary:
                return unary[type(node.op)](visit(node.operand))
            raise ValueError("Invalid expression")

        result = visit(tree)
        if not isinstance(result, (int, float)) or not float("-inf") < result < float("inf"):
            raise ValueError("Invalid result")
        return f"{result:.11g}"

    def press(self, action):
        if action == "clear":
            self.expression = ""
            self.just_calculated = False
        elif action == "equals":
            if self.expression and self.expression[-1] not in "+-*/.":
                try:
                    self.expression = self.evaluate(self.expression)
                except (SyntaxError, ValueError, ZeroDivisionError, OverflowError):
                    self.expression = "Error"
                self.just_calculated = True
        elif action == "decimal":
            if self.just_calculated:
                self.expression = ""
            self.just_calculated = False
            operand = re.split(r"[+*/]|(?<!^)-", self.expression)[-1]
            if "." not in operand:
                self.expression += ("" if operand else "0") + "."
        elif action == "sign":
            match = re.search(r"\d*\.?\d+$", self.expression)
            if match:
                start = match.start()
                if start > 0 and self.expression[start - 1] == "-":
                    self.expression = self.expression[:start - 1] + self.expression[start:]
                else:
                    self.expression = self.expression[:start] + "-" + self.expression[start:]
        elif action == "percent":
            match = re.search(r"\d*\.?\d+$", self.expression)
            if match:
                number = float(match.group()) / 100
                self.expression = self.expression[:match.start()] + f"{number:.11g}"
        elif action in "0123456789":
            if self.just_calculated or self.expression == "Error":
                self.expression = ""
            self.expression += action
            self.just_calculated = False
        elif action in "+-*/":
            self.just_calculated = False
            if self.expression and self.expression[-1] in "+-*/":
                self.expression = self.expression[:-1] + action
            elif self.expression and self.expression[-1] != ".":
                self.expression += action
        self.refresh()

    def on_key(self, event):
        key = {"Return": "equals", "KP_Enter": "equals", "Escape": "clear",
               "BackSpace": "backspace", "asterisk": "*", "slash": "/"}.get(
                   event.keysym, event.char)
        if key == "backspace":
            self.expression = self.expression[:-1]
            self.just_calculated = False
            self.refresh()
        elif key == ".":
            self.press("decimal")
        elif key in "0123456789+-*/":
            self.press(key)
        elif key in ("equals", "clear"):
            self.press(key)
        elif key == "%":
            self.press("percent")


if __name__ == "__main__":
    app = tk.Tk()
    Calculator(app)
    app.mainloop()
