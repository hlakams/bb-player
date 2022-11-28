"""
The attendant draws cards and verifies hands

Definitions:
status -> int
    * 0: hand sum < 17
    * 1: hand sum >= 17
    * 2: hand sum == 17
    * 3: hand sum > 21
"""

# the attendant draws blackjack cards
def draw_card(shoe: list[int], hand: list[int]) -> list[list[int], list[int], int]:
    # draw a card from top of shoe
    pulled_card = shoe[0]
    # add pulled card to hand
    hand.append(pulled_card)
    # shoe is updated
    shoe = shoe[1:]

    # return the game state
    return [shoe, hand, pulled_card]

# return a hand's status
def verify(hand: list[int]) -> int:
    # check hand's sum
    hand_sum = sum(hand)

    # check if hand is valid
    if hand_sum > 21:
        # invalid hand
        status = 3
    # blackjack?
    elif hand_sum == 21:
        # hand has a blackjack
        status = 2
    # valid for player?
    elif hand_sum < 21:
        # invalid for dealer?
        if hand_sum >= 17:
            # stop game, check hands
            status = 1
        else:
            # game is valid for player
            status = 0
    
    # card status settled
    return status