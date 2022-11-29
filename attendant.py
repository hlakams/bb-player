# necessary imports
import secrets

"""
The attendant draws cards and verifies hands

Definitions:
Status codes
status -> int
    * 0: hand sum < 17
    * 1: hand sum >= 17
    * 2: hand sum == 21
    * 3: hand sum > 21
outcome_status -> int
    * 4: loss
    * 5: win
    * 6: draw
action_status -> int
    * 7: hit
    * 8: stand
    * 9: double
"""

# the attendant draws blackjack cards
def draw_card(shoe: list[int], hand: list[int]) -> list[list[int], list[int]]:
    # draw a card from top of shoe
    pulled_card = shoe[0]
    # add pulled card to hand
    hand.append(pulled_card)
    # shoe is updated
    shoe = shoe[1:]

    # return the game state
    return [shoe, hand]

# return a hand's status
def verify(hand: list[int]) -> int:
    # check hand's sum
    hand_sum = blackjack_sum(hand)

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

# TODO: add support for attendant to run Final games, or split to own class
# status code 4 is loser
def loser(winning_hand: list[int], wager: float) -> list[list[int], float, int]:
    return [winning_hand, -1.0 * wager, 4]

# status code 5 is winner, gain 1.5x wager
def winner(player_hand: list[int], wager: float) -> list[list[int], float, int]:
    return [player_hand, 1.5 * wager, 5]

# status code 6 is a draw, lose nothing
def draw(player_hand: list[int], wager: float) -> list[list[int], float, int]:
    return [player_hand, 0.0 * wager, 6]

# a basic, proof-of-concept blackjack game that runs for a single round
# our player plays against the house and randomly selects hit/stand/double
# returns winning hand (if draw, player's hand) and status for player
def basic_game(shoe: list[int], wager: float) -> list[list[int], float, int]:
    # initialization
    house_hand = []
    player_hand = []

    # actions are hit/stand/double for player
    action_status = 7

    # first deal, 2 cards each
    for _ in range(2):
        [shoe, player_hand] = draw_card(shoe, player_hand)
        [shoe, house_hand] = draw_card(shoe, house_hand)

    # DEBUG
    print("Initial decks:")
    print("Player hand: ", player_hand)
    print("Player sum: ", blackjack_sum(player_hand))
    print("House hand: ", house_hand)
    print("House sum: ", blackjack_sum(house_hand), '\n')

    # keep track of game state
    state = 0

    # game state machine
    while True:
        # new state
        state += 1

        if state == 1:
            action_status = secrets.choice(range(7,10))
            if action_status == 9:
                # DEBUG
                print("DOUBLE\n")
                wager = wager * 2
                [shoe, player_hand] = draw_card(shoe, player_hand)
        
        # decide if player will draw or not
        if action_status == 7:
            # TODO: have player agent heuristic decide plan
            # TODO: card counting strategies for benchmark
            # TODO: base deck manipulation
            # pick hit or stand
            action_status = secrets.choice(range(7,9))
            if action_status == 7:
                # DEBUG
                print("HIT\n")
                [shoe, player_hand] = draw_card(shoe, player_hand)
            # DEBUG
            else:
                print("STAND\n")

        # house draw
        [shoe, house_hand] = draw_card(shoe, house_hand)


        # get game state status
        house_status = verify(house_hand)
        player_status = verify(player_hand)
        # get hand sums
        house_sum = blackjack_sum(house_hand)
        player_sum = blackjack_sum(player_hand)

        # DEBUG
        print("State {} decks:".format(state))
        print("Player hand:", player_hand)
        print("Player sum:", player_sum)
        print("Player status", player_status)
        print("House hand:", house_hand)
        print("House sum:", house_sum, )
        print("House status:", house_status, '\n')

        # house hand is playable
        if house_status == 0:
            # check if player hand is playable
            if player_status < 2:
                # do nothing, go to action
                continue
            # check if player has blackjack
            elif player_status == 2:
                # winner!
                return winner(player_hand, wager)
            # player lost
            else:
                # loser :(
                return loser(house_hand, wager)

        # house hand is >= 17 but not >= 21; end gameplay
        elif house_status == 1:
            # check if player hand is playable
            if player_status == 1:
                # check if house won
                if house_sum > player_sum:
                    # loser :(
                    return loser(house_hand, wager)
                # check if player won
                elif house_sum < player_sum:
                    # winner!
                    return winner(player_hand, wager)
                # draw
                else:
                    return draw(player_hand, wager)
            # check if player has blackjack
            elif player_status == 2:
                # winner!
                return winner(player_hand, wager)
            # player lost
            else:
                # loser :(
                return loser(house_hand, wager)
            
        # house hand is blackjack
        elif house_status == 2:
            # draw, player also has blackjack
            if player_status == 2:
                return winner(player_hand, wager)
            # loser :(
            else:
                return loser(house_hand, wager)
        # house went bust
        else:
            # draw, player also went bust
            if player_status == 3:
                return draw(player_hand, wager)
            # winner! any value that isn't a bust
            else:
                return winner(player_hand, wager)
