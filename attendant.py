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
def winner(player_hand: list[int], wager: float, state: int) -> list[list[int], float, int]:
    # get hand sum
    hand_sum = benchmark.blackjack_sum(player_hand)
    
    # check if blackjack win (initial state)
    if hand_sum == 21 and state == 0:
        # blackjack hand, 3:2 odds
        return [player_hand, 1.5 * wager, 5]
    # standard win, 1:1 odds
    else:
        return [player_hand, 1.0 * wager, 5]

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
    for _ in range(2):
        [shoe, house_hand] = draw_card(shoe, house_hand)
    
    # get initial game state status
    house_init_status = verify(house_hand)
    player_init_status = verify(player_hand)

    # house has blackjack
    if house_init_status == 2:
        # player also has blackjack, draw
        if player_init_status == 2:
            return winner(player_hand, wager, 0)
        # player loses
        else:
            return loser(house_hand, wager)
    # house bust
    elif house_init_status == 3:
        # player bust, loses
        if player_init_status == 3:
            return loser(house_hand, wager)
        # player wins
        else:
            return winner(player_hand, wager, 0)
    # house policy still allows hits
    else:
        # player wins on blackjack
        if player_init_status == 2:
            return winner(player_hand, wager, 0)
        # player bust
        elif player_init_status == 3:
            return loser(house_hand, wager)

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

        # check if the current house hand falls under certain conditions
        if state > 1:
            # get house pre-status
            house_pre_status = verify(house_hand)
            # hosue draws new card if allowed by static policy
            if house_pre_status == 0:
                # house draw
                [shoe, house_hand] = draw_card(shoe, house_hand)

            # get house post-status
            house_post_status = verify(house_hand)
            # house has 21 on a non-initial state, so they win
            if house_post_status == 3:
                return loser(house_hand, wager)
        
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
                # ccount_agent.ccount(name, np.abs(6 - house_hand[1]))

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


        # get game state status
        house_status = verify(house_hand)
        player_status = verify(player_hand)
        # get hand sums
        house_sum = benchmark.blackjack_sum(house_hand)
        player_sum = benchmark.blackjack_sum(player_hand)

        # player hits
        if action_status == 7:
            # house hand is >= 17 but not >= 21; end gameplay
            if house_status == 1:
                # check if player hand is playable
                if player_status == 1:
                    # check if house won
                    if house_sum > player_sum:
                        return loser(house_hand, wager)
                    # check if player won
                    elif house_sum < player_sum:
                        return winner(player_hand, wager, state)
                    # draw
                    else:
                        return draw(player_hand, wager)
                # check if player has a winning hand
                elif player_status == 2:
                    return winner(player_hand, wager, state)
                # player lost
                elif player_status == 3:
                    return loser(house_hand, wager)
                
            # house hand has a winning hand
            elif house_status == 2:
                # draw, player also has a winning hand
                if player_status == 2:
                    return draw(player_hand, wager)
                # loser
                else:
                    return loser(house_hand, wager)
            # house hand has a winning hand
            elif house_status == 3:
                # player loses with a bust hand too
                if player_status == 3:
                    return loser(house_hand, wager)
                # player wins
                else:
                    return winner(player_hand, wager, state)
                        # house hand is playable
            # house can still play
            else:
                # check if player has a winning hand
                if player_status == 2:
                    return winner(player_hand, wager, state)
                # player lost
                elif player_status == 3:
                    return loser(house_hand, wager)

        # player stands or doubles: conditionals based on wins by player
        # we also check for house bust beforehand, and house plays until sum >= 17
        else:
            # house has stopped hitting
            if house_status == 1:
                # player in same sum interval
                if player_status <= 2:
                    # same sum, draw
                    if player_sum == house_sum:
                        return draw(player_hand, wager)
                    # player sum is greater but non-bust, win by default
                    elif player_sum > house_sum:
                        return winner(player_hand, wager, state)
                    # player sum less than house, they lose
                    else:
                        return loser(house_hand, wager)
                # player cannot make any more moves, so they lose
                else:
                    return loser(house_hand, wager)
            # house has a winning hand
            elif house_status == 2:
                # player has a winning hand
                if player_status == 2:
                    return draw(player_hand, wager)
                # player loses otherwise
                else:
                    return loser(house_hand, wager)
            # house bust
            elif house_status == 3:
                # player also bust, loses
                if player_status == 3:
                    return loser(player_hand, wager)
                # player winner by default
                else:
                    return winner(player_hand, wager, state)
            # house can still play
            else:
                # player has winning hand
                if player_status == 2:
                    return winner(player_hand, wager, state)
                # player bust
                elif player_status == 3:
                    return loser(house_hand, wager)
