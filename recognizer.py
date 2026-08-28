from collections import Counter
from itertools import product

NORMAL_RANKS = [
    '2','3','4','5','6','7',
    '8','9','T','J','Q','K','A'
]

SUITS = ['S','H','D','C']

def is_joker(card):
    return card in ('B','R')

def get_rank(card):
    if is_joker(card):
        return card
    return card[1]

def get_suit(card):
    if is_joker(card):
        return None
    return card[0]

def is_wildcard(card, level):
    """
    Wildcard = Heart + current level.
    Example:
        level = J
        HJ is wildcard.
    """
    return card == "H" + level

def count_ranks(cards):
    return Counter(get_rank(c) for c in cards)

def build_rank_order(level):
    """
    Build comparison order.

    Example

    level = 7

    2 3 4 5 6 8 9 T J Q K A 7 B R
    """
    order = []

    for r in NORMAL_RANKS:
        if r != level:
            order.append(r)

    order.append(level)
    order.append("B")
    order.append("R")

    return {
        r:i
        for i,r in enumerate(order)
    }

def compare_rank(a,b,level):
    order = build_rank_order(level)
    return order[a] - order[b]

def rank_index(rank):
    return NORMAL_RANKS.index(rank)

def is_straight_ranks(ranks):

    if len(set(ranks)) != 5:
        return False

    if set(ranks) == {
        "A",
        "2",
        "3",
        "4",
        "5"
    }:
        return True

    ordered = sorted(
        ranks,
        key=rank_index
    )

    for i in range(4):

        if rank_index(ordered[i+1]) != rank_index(ordered[i]) + 1:
            return False

    return True

def is_rank_consecutive(ranks):

    values = sorted(
        rank_index(r)
        for r in ranks
    )

    for i in range(len(values)-1):

        if values[i+1] != values[i]+1:
            return False

    return True

def generate_replacements(rank):
    if rank in NORMAL_RANKS:
        return [
            suit + rank
            for suit in SUITS
        ]


def expand_wildcards(cards, level):
    """
    Generate every possible replacement of wildcards.

    H7/HJ/etc can become any non-joker card.
    """

    wildcard_positions = []

    for i, c in enumerate(cards):
        if is_wildcard(c, level):
            wildcard_positions.append(i)

    if not wildcard_positions:
        return [cards.copy()]

    replacement_cards = []

    for rank in NORMAL_RANKS:
        for suit in SUITS:
            replacement_cards.append(
                suit + rank
            )

    possibilities = []

    for replacements in product(
        replacement_cards,
        repeat=len(wildcard_positions)
    ):

        new_cards = cards.copy()

        for pos, new_card in zip(
            wildcard_positions,
            replacements
        ):
            new_cards[pos] = new_card

        possibilities.append(new_cards)

    return possibilities

def make_result(type_name, rank):
    return {
        "type": type_name,
        "rank": rank
    }

def recognize_single(cards, level):
    if len(cards) != 1:
        return []
    answers = []
    for possibility in expand_wildcards(cards, level):
        ranks = [get_rank(c) for c in possibility]
        result = make_result("single", ranks[0])
        if result not in answers:
            answers.append(result)
    
    return answers

def recognize_pair(cards, level):
    if len(cards) != 2:
        return []
    
    answers = []

    for possibility in expand_wildcards(cards, level):

        ranks = [get_rank(c) for c in possibility]

        if ranks[0] == ranks[1]:
            result = make_result("pair", ranks[0])

            if result not in answers:
                answers.append(result)
    return answers

def recognize_triple(cards, level):

    if len(cards) != 3:
        return []
    
    answers = []
    for possibility in expand_wildcards(cards, level):
        ranks = [get_rank(c) for c in possibility]
        if len(set(ranks)) == 1:
            result = make_result("triple", ranks[0])

            if result not in answers:
                answers.append(result)
    return answers

def recognize_bomb(cards, level):
    if len(cards) < 4:
        return []
    
    answers = []
    for possibility in expand_wildcards(cards, level):
        ranks = [get_rank(c) for c in possibility]
        if len(set(ranks)) == 1:
            result = make_result("bomb", ranks[0])
            
            if result not in answers:
                answers.append(result)
    return answers

def recognize_quad_kings(cards):
    if len(cards) != 4:
        return []
    
    counter = Counter(cards)
    if counter["B"] == 2 and counter["R"] == 2:
        return [
            {
                "type":"quad_kings",
                "rank":"R"
            }
        ]
    return []

def recognize_full_house(cards, level):
    if len(cards) != 5:
        return []
    
    answers = []

    for possibility in expand_wildcards(cards, level):
        ranks = [get_rank(c) for c in possibility]
        counter = Counter(ranks)
        counts = sorted(counter.values())
        if counts == [2,3]:
            triple_rank = None
            for r,c in counter.items():
                if c == 3:
                    triple_rank = r

            result = make_result(
                "full_house",
                triple_rank
            )
            if result not in answers:
                answers.append(result)
    return answers

def recognize_straight(cards, level):

    if len(cards) != 5:
        return []

    answers=[]

    for possibility in expand_wildcards(cards, level):

        ranks=[
            get_rank(c)
            for c in possibility
        ]

        if "B" in ranks or "R" in ranks:
            continue

        if is_straight_ranks(ranks):

            ordered = sorted(
                ranks,
                key=rank_index
            )

            if set(ranks)=={
                "A",
                "2",
                "3",
                "4",
                "5"
            }:
                high="5"
            else:
                high=ordered[-1]

            result=make_result(
                "straight",
                high
            )

            if result not in answers:
                answers.append(result)

    return answers

def recognize_plate(cards, level):
    if len(cards) != 6:
        return []
    answers = []

    for possibility in expand_wildcards(cards, level):
        ranks = [get_rank(c) for c in possibility]

        if "B" in ranks or "R" in ranks:
            continue

        counter = Counter(ranks)

        if len(counter) != 3:
            continue

        if sorted(counter.values()) != [2,2,2]:
            continue

        ordered = sorted(counter.keys(), key=rank_index)

        if "2" in ordered:
            continue
        
        if is_rank_consecutive(ordered):

            result = make_result(
                "plate",
                ordered[-1]
            )

            if result not in answers:
                answers.append(result)
    return answers

def recognize_steel(cards, level):

    if len(cards) != 6:
        return []
    
    answers = []

    for possibility in expand_wildcards(cards, level):

        ranks = [get_rank(c) for c in possibility]

        if "B" in ranks or "R" in ranks:
            continue
        
        counter = Counter(ranks)

        if len(counter) != 2:
            continue

        if sorted(counter.values()) != [3,3]:
            continue
        
        ordered = sorted(counter.keys(), key=rank_index)

        if "2" in ordered:
            continue

        if is_rank_consecutive(ordered):

            result = make_result(
                "steel",
                ordered[-1]
            )

            if result not in answers:
                answers.append(result)

    return answers

def recognize_straight_flush(cards, level):

    if len(cards) != 5:
        return []

    answers = []

    for possibility in expand_wildcards(cards, level):

        suits = [get_suit(c) for c in possibility]
        ranks = [get_rank(c) for c in possibility]

        if "B" in ranks or "R" in ranks:
            continue

        if len(set(suits)) != 1:
            continue

        if len(set(ranks)) != 5:
            continue

        if "2" in ranks:
            continue

        ordered = sorted(ranks, key=rank_index)

        if is_straight_ranks(ranks):

            result = make_result(
                "straight_flush",
                ordered[-1]
            )

            if result not in answers:
                answers.append(result)

    return answers

def remove_duplicate(results):

    seen=set()
    output=[]

    for r in results:

        key=(
            r["type"],
            r["rank"]
        )

        if key not in seen:
            seen.add(key)
            output.append(r)

    return output

def recognize(cards, level):

    result = []

    result.extend(recognize_single(cards, level))
    result.extend(recognize_pair(cards, level))
    result.extend(recognize_triple(cards, level))
    result.extend(recognize_bomb(cards, level))
    result.extend(recognize_quad_kings(cards))
    result.extend(recognize_full_house(cards, level))
    result.extend(recognize_straight(cards, level))
    result.extend(recognize_plate(cards, level))
    result.extend(recognize_steel(cards, level))
    result.extend(recognize_straight_flush(cards, level))

    return remove_duplicate(result)


