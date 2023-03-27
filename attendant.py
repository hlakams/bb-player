# necessary imports
import secrets
import ccount_agent
import benchmark
import bb_player
import numpy as np

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

# list of strategies to test in main driver function 
names = [
    "bb",
    "random",
    "hi_lo",
    "ko",
    "zen",
    "ten",
    "halves",
    "uston"
]

# the "attendant" draws blackjack cards (hand) from a defined
def draw_card(shoe: list[int], hand: list[int]) -> list[list[int], list[int]]:
    # draw a card from top of shoe
    pulled_card = shoe[0]
    # add pulled card to hand
    hand.append(pulled_card)
    # shoe is updated
    shoe = shoe[1:]

    # return the game state
    return [shoe, hand]

# check the hand's sum and output status code (to inform game state)
def verify(hand: list[int]) -> int:
    # check hand's sum
    hand_sum = benchmark.blackjack_sum(hand)

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

# status code 4 is loser
def loser(winning_hand: list[int], wager: float) -> list[list[int], float, int]:
    # losing hand, bet is removed from balance
    return [winning_hand, -1.0 * wager, 4]

# status code 5 is winner
def winner(player_hand: list[int], wager: float) -> list[list[int], float, int]:
    # winning hand, gain 1.5x wager
    return [player_hand, 1.5 * wager, 5]

# status code 6 is a draw
def draw(player_hand: list[int], wager: float) -> list[list[int], float, int]:
    # no loss, gain nothing
    return [player_hand, 0.0 * wager, 6]

# Verification Section
# a basic, proof-of-concept blackjack game that runs for a single round
# our player plays against the house and randomly selects hit/stand/double

# returns winning hand (if draw, player's hand) and status for player
def basic_game(shoe: list[int], wager: float, name: str) -> list[list[int], float, int]:
    # initialization
    house_hand = []
    player_hand = []

    # actions are hit/stand/double for player
    action_status = 7

    # first deal, 2 cards each
    for _ in range(2):
        [shoe, player_hand] = draw_card(shoe, player_hand)
        [shoe, house_hand] = draw_card(shoe, house_hand)

    # keep track of game state
    state = 0
    count = 0.0
    base_distribution = [4 for _ in range(13)]
    # for bb-agent
    transitions = benchmark.transitions
    emissions = benchmark.emissions

    # game state machine
    while True:
        # new state
        state += 1
        
        # post-initial
        if state == 1:
            # check if name is a ccount strategy
            if name not in names[0:2]:
                # do preliminary card counting
                # player counts
                for card in player_hand:
                    count += ccount_agent.ccount(name, card)
                # assumed "house" hand
                for card in house_hand[1:]:
                    count += ccount_agent.ccount(name, card)
                # account for other card
                ccount_agent.ccount(name, np.random.randint(13))

                # figure out action
                action_status = ccount_agent.ccount_action(state, count)

                # action conditionals
                # double the wager
                if action_status == 9:    
                    wager = wager * 2
                    # draw new card and count it
                    [shoe, player_hand] = draw_card(shoe, player_hand)
                    count += ccount_agent.ccount(name, player_hand[-1])
                # hit
                elif action_status == 7:
                    # draw new card and count it
                    [shoe, player_hand] = draw_card(shoe, player_hand)
                    count += ccount_agent.ccount(name, player_hand[-1])

            # random agent preliminaries
            elif name == names[1]:
                # choose a random valid action
                action_status = secrets.choice(range(7,10))
                # double wager
                if action_status == 9:
                    wager = wager * 2
                    # draw new card
                    [shoe, player_hand] = draw_card(shoe, player_hand)
                # play a hit
                if action_status == 7:
                    # draw new card
                    [shoe, player_hand] = draw_card(shoe, player_hand)
            # bb-player preliminaries
            elif name == names[0]:
                # update distribution with player hand
                for card in player_hand:
                    base_distribution = bb_player.update_distribution(base_distribution, card)
                # update distribution with assumed house hand
                for card in house_hand[1:]:
                    base_distribution = bb_player.update_distribution(base_distribution, card)
                # get step from current tree level
                [action_status, transitions, emissions] = bb_player.action_tree_step(transitions, emissions, player_hand, state, base_distribution)

                # double wager
                if action_status == 9:
                    wager = wager * 2
                    # draw new card and update distribution with new card
                    [shoe, player_hand] = draw_card(shoe, player_hand)
                    base_distribution = bb_player.update_distribution(base_distribution, player_hand[-1])
                # hit
                elif action_status == 7:
                    # draw new card and update distribution with new card
                    [shoe, player_hand] = draw_card(shoe, player_hand)
                    base_distribution = bb_player.update_distribution(base_distribution, player_hand[-1])
        
        # decide if player will draw or not
        elif state != 1 and action_status == 7:
            # check if name is a ccount strategy
            if name not in names[0:2]:
                # update card count with the new house card
                count += ccount_agent.ccount(name, card)
                # figure out action
                action_status = ccount_agent.ccount_action(state, count)
                # player chooses to hit
                if action_status == 7:
                    # draw card and update count from known count
                    [shoe, player_hand] = draw_card(shoe, player_hand)
                    count += ccount_agent.ccount(name, player_hand[-1])

            # random action agent
            elif name == names[1]:
                # pick hit or stand
                action_status = secrets.choice(range(7,9))
                # agent chooses to hit
                if action_status == 7:
                    # get a new card
                    [shoe, player_hand] = draw_card(shoe, player_hand)

            
            # bb-player agent
            elif name == names[0]:
                # get current action state 
                [action_status, transitions, emissions] = bb_player.action_tree_step(transitions, emissions, player_hand, state, base_distribution)
                # agent chooses to hit
                if action_status == 7:
                    # draw card and update distribution
                    [shoe, player_hand] = draw_card(shoe, player_hand)
                    base_distribution = bb_player.update_distribution(base_distribution, player_hand[-1])

        # house draw
        [shoe, house_hand] = draw_card(shoe, house_hand)

        # get game state status
        house_status = verify(house_hand)
        player_status = verify(player_hand)
        # get hand sums
        house_sum = benchmark.blackjack_sum(house_hand)
        player_sum = benchmark.blackjack_sum(player_hand)

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
