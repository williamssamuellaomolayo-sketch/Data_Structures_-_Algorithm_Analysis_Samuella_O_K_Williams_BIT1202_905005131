"""
DCOMP320 - Data Structures and Algorithms
Assignment: Stacks Implementation

Reads mathematical expressions from input.txt, evaluates each one using
stacks, and writes the results to output.txt in the same format
(results replace expressions; separator lines are preserved).
"""

import sys

SEPARATOR_CHARS = set("-")
OPERATORS = {"+": 1, "-": 1, "*": 2, "/": 2}


class Stack:
    """A simple LIFO stack backed by a Python list."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


def tokenize(expression):
    """Split an expression string into numbers, operators and parentheses.
    A '-' is treated as a unary minus (part of a negative number) when it
    appears at the start, after '(' or after another operator."""
    tokens = []
    i, n = 0, len(expression)
    while i < n:
        ch = expression[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit() or ch == ".":
            j = i
            while j < n and (expression[j].isdigit() or expression[j] == "."):
                j += 1
            try:
                tokens.append(float(expression[i:j]))
            except ValueError:
                raise ValueError(f"invalid number '{expression[i:j]}'")
            i = j
        elif ch in OPERATORS or ch in "()":
            if ch == "-" and (not tokens or tokens[-1] == "(" or tokens[-1] in OPERATORS):
                tokens.append("u-")          # unary minus marker
            else:
                tokens.append(ch)
            i += 1
        else:
            raise ValueError(f"invalid character '{ch}'")
    return tokens


def apply_operator(operators, values):
    """Pop one operator and its operand(s), compute, push the result."""
    op = operators.pop()
    if op == "u-":
        if values.is_empty():
            raise ValueError("malformed expression")
        values.push(-values.pop())
        return
    if values.size() < 2:
        raise ValueError("malformed expression")
    b = values.pop()
    a = values.pop()
    if op == "+":
        values.push(a + b)
    elif op == "-":
        values.push(a - b)
    elif op == "*":
        values.push(a * b)
    elif op == "/":
        if b == 0:
            raise ZeroDivisionError("division by zero")
        values.push(a / b)


def evaluate_expression(expression):
    """Evaluate an infix expression using an operand stack and an operator
    stack (Dijkstra's shunting-yard idea). Handles + - * /, parentheses,
    precedence, decimals and unary minus."""
    values = Stack()
    operators = Stack()
    prev_was_operand = False

    for token in tokenize(expression):
        if isinstance(token, float):
            if prev_was_operand:
                raise ValueError("malformed expression")
            values.push(token)
            prev_was_operand = True
        elif token == "(":
            if prev_was_operand:
                raise ValueError("malformed expression")
            operators.push(token)
        elif token == ")":
            while not operators.is_empty() and operators.peek() != "(":
                apply_operator(operators, values)
            if operators.is_empty():
                raise ValueError("mismatched parentheses")
            operators.pop()                  # discard '('
            prev_was_operand = True
        elif token == "u-":
            operators.push(token)
            prev_was_operand = False
        else:                                # binary operator
            if not prev_was_operand:
                raise ValueError("malformed expression")
            while (not operators.is_empty() and operators.peek() != "("
                   and (operators.peek() == "u-"
                        or OPERATORS[operators.peek()] >= OPERATORS[token])):
                apply_operator(operators, values)
            operators.push(token)
            prev_was_operand = False

    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("mismatched parentheses")
        apply_operator(operators, values)

    if values.size() != 1:
        raise ValueError("malformed expression")
    return values.pop()


def format_result(value):
    """Show whole numbers without a decimal point (13, not 13.0)."""
    if value == int(value):
        return str(int(value))
    return str(round(value, 6))


def is_separator(line):
    s = line.strip()
    return len(s) >= 3 and all(c in SEPARATOR_CHARS for c in s)


def process_file(input_path="input.txt", output_path="output.txt"):
    """Read expressions, evaluate each, and write results in the same layout."""
    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    out_lines = []
    for line in lines:
        if is_separator(line):
            out_lines.append(line.strip())   # keep the same separator
        elif line.strip() == "":
            continue                         # ignore blank lines
        else:
            try:
                out_lines.append(format_result(evaluate_expression(line)))
            except (ValueError, ZeroDivisionError) as e:
                out_lines.append(f"Error: {e}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines) + "\n")
    return out_lines


if __name__ == "__main__":
    in_file = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "output.txt"
    try:
        results = process_file(in_file, out_file)
        print(f"Done. {len(results)} lines written to {out_file}")
    except FileNotFoundError:
        print(f"Error: '{in_file}' not found.")
