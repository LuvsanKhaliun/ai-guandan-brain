from collections import Counter

NORMAL_RANKS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
SUITS = ['S','H','D','C']


def build_full_deck():
    """
    GuanDan uses 2 standard decks:
    - each normal rank appears 4 suits x 2 decks = 8 copies total
    - jokers: 2 small (B) + 2 big (R) = 4 total
    """
    deck = []
    for _ in range(2):
        for suit in SUITS:
            for rank in NORMAL_RANKS:
                deck.append(suit + rank)
        deck.append("B")
        deck.append("R")
    return deck


FULL_DECK = build_full_deck()


def get_rank(card):
    if card in ("B", "R"):
        return card
    return card[1:]


def flatten_played_cards(trick_history):
    """
    trick_history entries look like [seat, [cards]] (pass = empty list).
    Returns a flat list of every card that has actually been played so far.
    """
    played = []
    for entry in trick_history:
        _, cards = entry
        played.extend(cards)
    return played


def get_unseen_cards(hand, trick_history):
    """
    Everything not in your own hand and not yet played by anyone.
    This is exactly the set of cards distributed across the other
    three players' hands right now (you can't tell which player
    holds which, but you know the pool).
    """
    remaining = Counter(FULL_DECK)

    remaining.subtract(Counter(hand))
    remaining.subtract(Counter(flatten_played_cards(trick_history)))

    unseen = []
    for card, count in remaining.items():
        unseen.extend([card] * max(count, 0))

    return unseen


def count_unseen_by_rank(unseen_cards):
    """
    How many unseen copies exist of each rank, regardless of suit.
    e.g. {'A': 5, 'K': 2, 'B': 1, ...}
    """
    return Counter(get_rank(c) for c in unseen_cards)


def rank_fully_accounted_for(rank, unseen_by_rank):
    """
    True if there are zero unseen copies of this rank left --
    meaning nobody else can possibly be holding one.
    """
    return unseen_by_rank.get(rank, 0) == 0


def higher_ranks_remaining(rank, level, unseen_by_rank):
    """
    Given a rank, how many unseen cards exist that outrank it
    (using GuanDan's level-adjusted rank order). Useful to judge
    how "safe" it is to lead with a given single/pair/etc.
    """
    order = NORMAL_RANKS.copy()
    if level in order:
        order.remove(level)
        order.append(level)
    order += ["B", "R"]

    if rank not in order:
        return 0

    idx = order.index(rank)
    higher = order[idx + 1:]

    return sum(unseen_by_rank.get(r, 0) for r in higher)