from __future__ import annotations
import time

class DLLNode:

    def __init__(self, value:int):
        self.value = value
        self.next =  None
        self.previous = None

def build_list(cups: list[int]) -> DLLNode:
    nodes = [DLLNode(cup) for cup in cups]
    for i in range(len(nodes)):
        nodes[i].next = nodes[(i + 1) % len(nodes)]
        nodes[i].previous = nodes[(i - 1) % len(nodes)]
    return nodes[0]

def build_map(start: DLLNode) -> dict[int,DLLNode]:
    node_map = {}
    node = start
    while node.value not in node_map:
        node_map[node.value] = node
        node = node.next
    return node_map

def move(node_map: dict[int, DLLNode], current_node: DLLNode, max_number: int) -> DLLNode:
    current_cup = current_node.value
    next1 = current_node.next.value
    next2 = current_node.next.next.value
    next3 = current_node.next.next.next.value

    destination_cup = current_cup
    while destination_cup == current_cup or destination_cup == next1 or destination_cup == next2 or destination_cup == next3:
        destination_cup = destination_cup - 1
        if destination_cup < 1:
            destination_cup = max_number

    destination_node = node_map[destination_cup]
    triple_start = current_node.next
    triple_end = current_node.next.next.next

    triple_start.previous = destination_node
    current_node.next = triple_end.next
    triple_end.next = destination_node.next
    destination_node.next = triple_start

    return current_node.next

def label(node_map: dict[int, DLLNode]) -> str:
    node1 = node_map[1]
    label = ""
    temp = node1.next
    while temp != node1:
        label += str(temp.value)
        temp = temp.next
    return label

def multiple_of_next_two(node_map: dict[int, DLLNode]) -> int:
    node1 = node_map[1]
    return node1.next.value * node1.next.next.value

start_time = time.time()
start = '135468729'
cups = [int(c) for c in start]

start_node = build_list(cups)
node_map = build_map(start_node)

moves = 100
max_number = max(cups)
for i in range(moves):
    start_node = move(node_map, start_node, max_number)
print(f"The final label for Part 1 after {moves} moves is {label(node_map)}")
print(f"{moves} took {time.time() - start_time} seconds")

# Part 2, many more moves :)
start_time = time.time()
moves = 10000000
# And much longer cup circle
cups = [int(c) for c in start] + list(range(10, 1000001))

start_node = build_list(cups)
node_map = build_map(start_node)

max_number = max(cups)
for i in range(moves):
    start_node = move(node_map, start_node, max_number)
print(f"The final multiple for Part 2 after {moves} moves is {multiple_of_next_two(node_map)}")
print(f"{moves} took {time.time() - start_time} seconds")