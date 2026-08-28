RANKS = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
    "A"
]


def rank_value(rank, level):

    order = RANKS.copy()

    if level in order:
        order.remove(level)
        order.append(level)

    order += ["B", "R"]

    return order.index(rank)

def compare_moves(my_move, last_move, level):

    """
    return:
    1  -> my_move wins
    0  -> equal
    -1 -> loses
    """

    my_type = my_move["type"]
    last_type = last_move["type"]

    if my_type == "quad_kings":
        if last_type == "quad_kings":
            return 0
        return 1

    if my_type == "bomb":

        if last_type not in ["bomb", "quad_kings"]:
            return 1

        if last_type == "bomb":

            if len(my_move["cards"]) > len(last_move["cards"]):
                return 1

            if len(my_move["cards"]) < len(last_move["cards"]):
                return -1

    if my_type != last_type:
        return -1

    my_rank = rank_value(my_move["rank"], level)
    last_rank = rank_value(last_move["rank"], level)

    if my_rank > last_rank:
        return 1

    if my_rank < last_rank:
        return -1

    return 0
