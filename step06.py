import requests
import json

URL = "http://183.175.14.145:8006/step_06"
USERNAME = "0221915013"

SUIT_ORDER = {
    'S': 0,
    'H': 1,
    'D': 2,
    'C': 3
}

NORMAL_RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

def build_rank_order(level):
    """
    Build rank order according to current level card.

    Example:
    level = '7'

    2 3 4 5 6 8 9 T J Q K A 7 B R
    """
    order = []
    for r in NORMAL_RANKS:
        if r != level:
            order.append(r)

    order.append(level)
    order.append('B')
    order.append('R')

    return {rank: i for i, rank in enumerate(order)}

def card_key(card, rank_order):
    """
    Sorting key.
    """

    if card == 'B':
        return (rank_order['B'], 0)

    if card == 'R':
        return (rank_order['R'], 0)

    suit = card[0]
    rank = card[1]

    return (
        rank_order[rank],
        SUIT_ORDER[suit]
    )

def sort_hand(hand, level):
    rank_order = build_rank_order(level)
    return sorted(
        hand,
        key=lambda x: card_key(x, rank_order)
    )

response = requests.get(
    URL,
    params={"user": USERNAME}
)

data = response.json()
print("Server Response:")
print(json.dumps(data, indent=4, ensure_ascii=False))
level = data["level"]
hands = data["hands"]
print("\nCurrent Level:", level)
answers = []

for hand in hands:
    sorted_hand = sort_hand(hand, level)
    answers.append(sorted_hand)

print("\nSorted Hands:")

for h in answers:
    print(h)

submit = requests.get(
    URL,
    params={
        "user": USERNAME,
        "ans": json.dumps(answers)
    }
)

print("\n==============================")
print("Submission Result:")
print(submit.text)