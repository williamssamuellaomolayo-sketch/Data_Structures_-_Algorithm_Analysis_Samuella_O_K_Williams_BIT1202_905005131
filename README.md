# Stack-Based Expression Evaluator (DCOMP320)

## Description
Reads mathematical expressions from `input.txt`, evaluates each using stacks,
and writes the results to `output.txt` in the same layout.

## How to run
1. Requires Python 3.8+ (no external libraries).
2. Put `stack_evaluator.py` and `input.txt` in the same folder.
3. Run: `python stack_evaluator.py`
   (optional: `python stack_evaluator.py my_input.txt my_output.txt`)
4. Open `output.txt` for the results.

## Input format
- One expression per line; expressions are separated by a line of dashes (`-----`).
- Supported: `+  -  *  /`, parentheses, decimals, negative numbers, spaces.

```
3 + 5 * 2
-----
(8 / 4) + 7 * 2
-----
10 - (2 + 3) * 4
```

## Output format
Each expression is replaced by its result; separators are kept unchanged.

```
13
-----
16
-----
-10
```

## Program structure
- `Stack` class: `push`, `pop`, `peek`, `is_empty`, `size`.
- `tokenize()`: splits text into numbers, operators, parentheses (detects unary minus).
- `evaluate_expression()`: two stacks (operands and operators) with precedence rules.
- `process_file()`: reads input, evaluates, writes output.

## Assumptions and limitations
- `*` and `/` have higher precedence than `+` and `-`; same-precedence operators evaluate left to right.
- Whole-number results print without decimals (13, not 13.0); others are rounded to 6 places.
- Invalid expressions (division by zero, mismatched parentheses, bad characters)
  produce a line `Error: <reason>` instead of stopping the program.
- Implicit multiplication such as `2(3)` is not supported.
- Note: in the assignment sheet, `(8 / 4) + 7 * 2` is shown as 17, but the correct value is 2 + 14 = **16**.
