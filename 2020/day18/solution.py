from  __future__ import annotations
from typing import Generator, Iterable
from functools import reduce

operation_map = {
    '+' : int.__add__,
    '*' : int.__mul__
}

def tokens(line: str) -> Generator[str, None, None]:
    for c in line:
        if c != " ":
            yield c

def eval(tokens: Iterable[str]) -> int:
    last_value = None
    op = None
    for token in tokens:
        if token in "0123456789":
            value = int(token)
        elif token in "+*":
            op = operation_map[token]
            continue
        elif token == "(":
            value = eval(tokens)
        elif token == ")":
            return last_value

        if op == None:
            last_value = value
        else:
            last_value = op(last_value, value)
            op = None

    return last_value

def eval2(tokens: Iterable[str]) -> int:
    value_stack = []
    op = None
    for token in tokens:
        if token in "0123456789":
            value = int(token)
        elif token in "+*":
            op = token
            continue
        elif token == "(":
            value = eval2(tokens)
        elif token == ")":
            return reduce(int.__mul__, value_stack)
        if op == None:
            value_stack.append(value)
        else:
            if op == "+":
                value_stack.append(value_stack.pop() + value)
            else:
                value_stack.append(value)
            op = None

    return reduce(int.__mul__, value_stack)

def evaluate(line: str) -> int:
    return eval(tokens(line))

def evaluate2(line: str) -> int:
    return eval2(tokens(line))

with open('input.txt') as f:
    lines = [line.strip() for line in f.readlines()]
    total = sum(evaluate(line) for line in lines)
    total2 = sum(evaluate2(line) for line in lines)
    print(f"Total of all expressions is {total}")
    print(f"Total with Addition precedence is {total2}")