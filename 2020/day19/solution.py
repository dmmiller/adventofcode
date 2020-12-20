from __future__ import annotations
from typing import IO, Iterator
from abc import ABCMeta, abstractmethod

class Expression(metaclass=ABCMeta):
    @abstractmethod
    def match(self, expressions: dict[int, Expression], string: str, i: int) -> int:
        pass

class SequenceExpression(Expression):
    def __init__(self, _id: int, sequence: list[int]):
        self._id = _id
        self.sequence = sequence

    def match(self, expressions: dict[int, Expression], string: str, i: int) -> int:
        for expr_id in self.sequence:
            expr = expressions[expr_id]
            i = expr.match(expressions, string, i)
            if i == -1:
                break
        return i

class OrExpression(Expression):
    def __init__(self, _id: int, lhs : Expression, rhs: Expression):
        self._id = _id
        self.lhs = lhs
        self.rhs = rhs

    def match(self, expressions: dict[int, Expression], string: str, i: int) -> int:
        original_i = i
        i = self.lhs.match(expressions, string, i)
        if i != -1:
            return i
        i = original_i
        return self.rhs.match(expressions, string, i)
    
class LiteralExpression(Expression):
    def __init__(self, _id: int, literal: str):
        self._id = _id
        self.literal = literal

    def match(self, expressions: dict[int, Expression], string: str, i: int) -> int:
        if string[i:i+(len(self.literal))] == self.literal:
            return i + len(self.literal) 
        return -1

def yield_block(f: IO) -> Iterator[str]:
    while (line := f.readline().strip()) != "":
        yield line

def build_rules(rules: Iterator[str]) -> dict[int, Expression]:
    rules_map = {}
    for rule in rules:
        rule_id, rule = rule.split(":")
        rules_map[int(rule_id)] = [term for term in rule.strip().split(" ")]
    complete_expresssions = {}
    for k, v in rules_map.items():
        if '"' in v[0]:
            complete_expresssions[k] = LiteralExpression(k, v[0][1:-1])
        else:
            if "|" in v:
                or_index = v.index('|')
                lhs = SequenceExpression(k, [int(term) for term in v[:or_index]])
                rhs = SequenceExpression(k, [int(term) for term in v[or_index + 1:]])
                complete_expresssions[k] = OrExpression(k, lhs, rhs)
            else:
                complete_expresssions[k] = SequenceExpression(k, [int(term) for term in v])
    return complete_expresssions

def matches(rules: dict[int, Expression], start: int, message: str) -> bool:
    top_level_expression = rules[start]
    return top_level_expression.match(rules, message, 0) == len(message)

with open('input.txt') as f:
    rules = build_rules(yield_block(f))
    messages = yield_block(f)
    total = sum(1 for message in messages if matches(rules, 0, message))
    print(f"Total number of messages that match is {total}")
