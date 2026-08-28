from collections import Counter
from recognizer import recognize


def generate_moves(hand, level):

    moves = []

    counter = Counter(get_rank(c) for c in hand)

    for card in hand:

        add_move(
            moves,
            [card],
            level
        )

    for rank, count in counter.items():

        cards = [
            c for c in hand
            if get_rank(c) == rank
        ]

        if count >= 2:

            for combo in combinations(cards,2):

                add_move(
                    moves,
                    list(combo),
                    level
                )

        if count >= 3:

            for combo in combinations(cards,3):

                add_move(
                    moves,
                    list(combo),
                    level
                )

        if count >= 4:

            add_move(
                moves,
                cards[:4],
                level
            )

    ranks = list(counter.keys())

    for triple_rank in ranks:

        if counter[triple_rank] >= 3:

            triple = [
                c for c in hand
                if get_rank(c)==triple_rank
            ][:3]

            for pair_rank in ranks:

                if pair_rank != triple_rank and counter[pair_rank]>=2:

                    pair = [
                        c for c in hand
                        if get_rank(c)==pair_rank
                    ][:2]

                    add_move(
                        moves,
                        triple+pair,
                        level
                    )

    result=[]

    seen=set()

    for m in moves:

        key=(
            tuple(sorted(m["cards"])),
            m["type"],
            m["rank"]
        )

        if key not in seen:

            seen.add(key)
            result.append(m)

    return result

def add_move(moves, cards, level):

    result = recognize(
        cards,
        level
    )

    for r in result:

        moves.append(
            {
                "cards":cards,
                "type":r["type"],
                "rank":r["rank"]
            }
        )

def get_rank(card):

    if card in ["B","R"]:
        return card

    return card[1:]

def combinations(cards, n):

    from itertools import combinations as c

    return c(cards,n)