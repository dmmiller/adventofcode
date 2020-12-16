from __future__ import annotations
from functools import reduce
from typing import IO
import re

field_re = re.compile(r"(?P<field>.+): (?P<range_1_min>\d+)-(?P<range_1_max>\d+) or (?P<range_2_min>\d+)-(?P<range_2_max>\d+)")

Field = tuple[str, int, int, int, int]
Ticket = list[int]

def parse_fields(f: IO) -> list[Field]:
    fields = []
    for line in f:
        line = line.strip()
        if line == "":
            break
        match = field_re.match(line)
        fields.append((match['field'], int(match['range_1_min']), int(match['range_1_max']), int(match['range_2_min']), int(match['range_2_max'])))
    return fields

def parse_your_ticket(f: IO) -> Ticket:
    _ = f.readline()
    ticket = f.readline().strip()
    _ = f.readline()
    return [int(field) for field in ticket.split(',')]

def parse_other_tickets(f: IO) -> list[Ticket]:
    _ = f.readline()
    tickets = []
    for line in f:
        tickets.append([int(field) for field in line.strip().split(',')])
    return tickets

def determine_valid_numbers(fields: list[Field]) -> set[int]:
    min_value = min(field[1] for field in fields)
    max_value = max(field[4] for field in fields)
    valid = set(i for i in range(min_value, max_value + 1) 
                if any(field[1] <= i <= field[2] or field[3] <= i <= field[4] for field in fields))
    return valid

def determine_error_rate(tickets: list[Ticket], valid_numbers: set[int]) -> int:
    total = 0
    total = sum(field for ticket in tickets for field in ticket if field not in valid_numbers)
    return total

def is_ticket_valid(ticket: Ticket, valid_numbers: set[int]) -> bool:
    return not any(True for field in ticket if field not in valid_numbers)

def determine_field_order(tickets: list[Ticket], fields: list[Field]) -> dict[str,int]:

    def is_field_valid_for_column(field: str, col: int) -> bool:
        ranges = field_map[field]
        return all(map(lambda ticket: ranges[0] <= ticket[col] <= ranges[1] or ranges[2] <= ticket[col] <= ranges[3], tickets))

    field_map = { field[0] : (field[1:]) for field in fields }
    unmapped_fields = set(field_map)
    field_order = {}
    used = set()
    while len(unmapped_fields) > 0:
        for i in range(len(fields)):
            if i in used:
                continue
            valid_fields = [field for field in unmapped_fields if is_field_valid_for_column(field, i)]
            if len(valid_fields) == 1:
                field = valid_fields[0]
                field_order[field] = i
                unmapped_fields.remove(field)
                used.add(i)
    return field_order

with open('input.txt') as f:
    fields = parse_fields(f)
    your_ticket = parse_your_ticket(f)
    other_tickets = parse_other_tickets(f)
    valid_numbers = determine_valid_numbers(fields)
    error_rate = determine_error_rate(other_tickets, valid_numbers)
    print(f"The error rate for part 1 is {error_rate}")
    valid_tickets = list(filter(lambda x: is_ticket_valid(x, valid_numbers), other_tickets))
    valid_tickets.append(your_ticket)
    field_order = determine_field_order(valid_tickets, fields)
    part2_answer = reduce(lambda x, y: x * y, (your_ticket[column] for field, column in field_order.items() if field.startswith("departure")))
    print(f"The product of all 'departure' fields is {part2_answer}")