from __future__ import annotations
from typing import IO, Iterator
from abc import ABCMeta, abstractmethod

class Expression(metaclass=ABCMeta):
    @abstractmethod
    def match(self, expressions: Grammar, string: str, i: int) -> int:
        pass

Grammar = dict[int, Expression]

class SequenceExpression(Expression):
    def __init__(self, _id: int, sequence: list[int]):
        self._id = _id
        self.sequence = sequence

    def match(self, expressions: Grammar, string: str, i: int) -> int:
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

    def match(self, expressions: Grammar, string: str, i: int) -> int:
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

    def match(self, expressions: Grammar, string: str, i: int) -> int:
        if string[i:i+(len(self.literal))] == self.literal:
            return i + len(self.literal)
        else:
            return -1

def yield_block(f: IO) -> Iterator[str]:
    while (line := f.readline().strip()) != "":
        yield line

def build_rules(rules: Iterator[str]) -> Grammar:
    expressions_map = {}
    for rule in rules:
        rule_id, rule = rule.split(":")
        rule_id = int(rule_id)
        terms = [term for term in rule.strip().split(" ")]
        if '"' in terms[0]:
            expressions_map[rule_id] = LiteralExpression(rule_id, terms[0][1:-1])
        else:
            if "|" in terms:
                or_index = terms.index('|')
                lhs = SequenceExpression(rule_id, [int(term) for term in terms[:or_index]])
                rhs = SequenceExpression(rule_id, [int(term) for term in terms[or_index + 1:]])
                expressions_map[rule_id] = OrExpression(rule_id, lhs, rhs)
            else:
                expressions_map[rule_id] = SequenceExpression(rule_id, [int(term) for term in terms])        
    return expressions_map

def matches(rules: Grammar, start: int, message: str) -> bool:
    top_level_expression = rules[start]
    return top_level_expression.match(rules, message, 0) == len(message)

with open('input.txt') as f:
    rules = build_rules(yield_block(f))
    messages = yield_block(f)
    total = sum(1 for message in messages if matches(rules, 0, message))
    print(f"Total number of messages that match is {total}")
