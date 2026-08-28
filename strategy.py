from generator import generate_moves
from comparator import compare_moves
from card_tracker import get_unseen_cards, count_unseen_by_rank, higher_ranks_remaining

RANK_ORDER_BASE = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]

BOMB_TYPES = {"bomb", "quad_kings"}
COMBO_TYPES = {"pair", "triple", "full_house", "straight", "plate", "steel", "straight_flush"}

DANGER_HAND_SIZE = 2


def rank_score(rank, level):
    order = RANK_ORDER_BASE.copy()
    if level in order:
        order.remove(level)
        order.append(level)
    order += ["B", "R"]
    return order.index(rank)


def choose_move(hand, level, last_play, last_player, my_seat, teams,
                 trick_history=None, hand_counts=None):
    moves = generate_moves(hand, level)

    if not moves:
        return []

    hand_size = len(hand)

    unseen_by_rank = {}
    if trick_history is not None:
        unseen = get_unseen_cards(hand, trick_history)
        unseen_by_rank = count_unseen_by_rank(unseen)

    opponent_in_danger = seat_opponent_near_finish(my_seat, hand_counts)

    if not last_play:
        return choose_lead(moves, hand, hand_size, level, unseen_by_rank)

    is_teammate = (
        last_player is not None
        and last_player % 2 == my_seat % 2
        and last_player != my_seat
    )

    if is_teammate:
        finishing = [m for m in moves if len(m["cards"]) == hand_size
                     and compare_against_last(m, last_play, level)]
        if finishing:
            return finishing[0]["cards"]
        return []

    candidates = [m for m in moves if compare_against_last(m, last_play, level)]
    if not candidates:
        return []

    return choose_beat(candidates, hand, hand_size, level, unseen_by_rank, opponent_in_danger)


def seat_opponent_near_finish(my_seat, hand_counts):
    if not hand_counts:
        return False
    for seat, count in enumerate(hand_counts):
        if seat == my_seat:
            continue
        if seat % 2 == my_seat % 2:
            continue
        if 0 < count <= DANGER_HAND_SIZE:
            return True
    return False


def safety_score(move, level, unseen_by_rank):
    if not unseen_by_rank:
        return 0
    if move["type"] in BOMB_TYPES:
        return 0
    return higher_ranks_remaining(move["rank"], level, unseen_by_rank)


def hand_shape_score(hand, cards_played, level):
    """
    Lower = better. Estimates how "awkward" the hand is after
    removing cards_played, by counting how many isolated singles
    would be left with no pair/triple/straight potential --
    those are the hardest cards to get rid of later.

    We approximate this cheaply: rather than re-running full move
    generation (expensive), we count leftover rank duplicates.
    Cards whose rank has no duplicate left behind, and no
    neighboring ranks (for straights), are treated as "stranded."
    """
    remaining = hand.copy()
    for c in cards_played:
        remaining.remove(c)

    if not remaining:
        return 0  # empty hand is perfect

    ranks_left = [get_rank(c) for c in remaining]
    from collections import Counter
    rank_counts = Counter(ranks_left)

    stranded = 0
    rank_positions = {r: i for i, r in enumerate(RANK_ORDER_BASE)}

    for rank, count in rank_counts.items():
        if count >= 2:
            continue  # part of a pair/triple/bomb potential, not stranded
        if rank not in rank_positions:
            continue  # joker/level card, rarely stranded
        idx = rank_positions[rank]
        neighbors = RANK_ORDER_BASE[max(0, idx - 2):idx + 3]
        has_neighbor = any(
            n != rank and n in rank_counts for n in neighbors
        )
        if not has_neighbor:
            stranded += 1

    return stranded


def get_rank(card):
    if card in ("B", "R"):
        return card
    return card[1:]


def choose_lead(moves, hand, hand_size, level, unseen_by_rank):
    finishing = [m for m in moves if len(m["cards"]) == hand_size]
    if finishing:
        return finishing[0]["cards"]

    non_bomb = [m for m in moves if m["type"] not in BOMB_TYPES]
    pool = non_bomb if non_bomb else moves

    max_len = max(len(m["cards"]) for m in pool)
    top_pool = [m for m in pool if len(m["cards"]) == max_len]

    top_pool.sort(key=lambda m: (
        hand_shape_score(hand, m["cards"], level),
        safety_score(m, level, unseen_by_rank),
        rank_score(m["rank"], level)
    ))
    return top_pool[0]["cards"]


def choose_beat(candidates, hand, hand_size, level, unseen_by_rank, opponent_in_danger):
    finishing = [m for m in candidates if len(m["cards"]) == hand_size]
    if finishing:
        return finishing[0]["cards"]

    non_bomb = [m for m in candidates if m["type"] not in BOMB_TYPES]
    bombs = [m for m in candidates if m["type"] in BOMB_TYPES]

    if opponent_in_danger and bombs:
        bombs.sort(key=lambda m: (len(m["cards"]), rank_score(m["rank"], level)))
        return bombs[0]["cards"]

    if non_bomb:
        min_len = min(len(m["cards"]) for m in non_bomb)
        cheapest = [m for m in non_bomb if len(m["cards"]) == min_len]
        cheapest.sort(key=lambda m: (
            hand_shape_score(hand, m["cards"], level),
            rank_score(m["rank"], level)
        ))
        return cheapest[0]["cards"]

    if bombs:
        bombs.sort(key=lambda m: (len(m["cards"]), rank_score(m["rank"], level)))
        return bombs[0]["cards"]

    return []


def compare_against_last(move, last_play, level):
    from recognizer import recognize
    result = recognize(last_play, level)
    ...
    last_move = {
        "cards": last_play,
        "type": result[0]["type"],
        "rank": result[0]["rank"]    
    }
    return compare_moves(move, last_move, level) > 0