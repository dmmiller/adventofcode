from __future__ import annotations
from typing import IO

def build_hands(lines: str) -> tuple[list[int], list[int]]:
    return [[int(line) for line in player.split('\n') if not line.startswith('P')] for player in lines.split("\n\n")]

def score_hand(hand: list[int]) -> int:
    return sum(card * (len(hand) - index) for index, card in enumerate(hand))

def return_winning_hand(hand1: list[int], hand2: list[int]) -> tuple[int, list[int]]:
    while len(hand1) != 0 and len(hand2) != 0:
        if hand1[0] > hand2[0]:
            hand1 += [hand1[0], hand2[0]]
        elif hand2[0] > hand1[0]:
            hand2 += [hand2[0], hand1[0]]
        hand1, hand2 = hand1[1:], hand2[1:]

    if len(hand1) > 0:
        return (1, hand1)
    else:
        return (2, hand2)

def return_winning_hand_recursive(hand1: list[int], hand2: list[int]) -> tuple[int, list[int]]:
    previous_round_starts = set()
    while len(hand1) != 0 and len(hand2) != 0:
        top1, *deck1 = hand1
        top2, *deck2 = hand2
        if (tuple(hand1), tuple(hand2)) in previous_round_starts:
            return (1, hand1)
        previous_round_starts.add((tuple(hand1), tuple(hand2)))
        if len(deck1) >= top1 and len(deck2) >= top2:
            winner, _ = return_winning_hand_recursive(deck1[:top1], deck2[:top2])
        elif top1 > top2:
            winner = 1
        else:
            winner = 2
        hand1, hand2 = deck1, deck2
        if winner == 1:
            hand1 += [top1, top2]
        else:
            hand2 += [top2, top1]

    if len(hand1) > 0:
        return (1, hand1)
    else:
        return (2, hand2)

with open('input.txt') as f:
    player1_hand, player2_hand = build_hands(f.read())

# grab a copy of original hands to play game 2
original1_hand, original2_hand = list(player1_hand), list(player2_hand)

winner, winning_hand = return_winning_hand(player1_hand, player2_hand)
print(f"Player {winner} won with a score of {score_hand(winning_hand)}")

winner, winning_hand = return_winning_hand_recursive(original1_hand, original2_hand)
print(f"Player {winner} won with a score of {score_hand(winning_hand)}")
