import bb_player

"""
Assorted utilities for benchmarking agent/strategy performance
"""

transitions = bb_player.init_emissions()
emissions = bb_player.init_emissions()

# update win likelihood
def win_likelihood_update(prior: float, current: float, batch_no: int) -> float:
    if batch_no == 1:
        return current
    else:
        return (((batch_no - 1) * prior + current) / batch_no)

def update_results(previous_result: list, current_result: list, batch_no: int) -> list:
    return [
            # name
            current_result[0],
            # games
            previous_result[1] + current_result[1],
            # wins
            previous_result[2] + current_result[2],
            # losses
            previous_result[3] + current_result[3],
            # draws
            previous_result[4] + current_result[4],
            # win likelihood update
            win_likelihood_update(previous_result[5], current_result[5], batch_no),
            # new balance
            current_result[6],
            # batch balance
            previous_result[7] + current_result[7]
        ]

def blackjack_sum(hand: list[int]) -> int:
    # indexing starts from 0 (ace)
    # face cards are indexed at value - 1
    # court cards are indices 10 - 12, value 10
    blackjack_dict = dict([
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 8),
        (8, 9),
        (9, 10),
        (10, 10),
        (11, 10),
        (12, 10)
    ])
    # running sum
    hand_sum = 0

    # iterate over all cards
    for card in hand:
        hand_sum += blackjack_dict.get(card)
    
    # done with sum
    return hand_sum