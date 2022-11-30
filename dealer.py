# necessary imports
import secrets
import sys

"""
Definitions:
deck -> list[int]
    * each deck has 52 cards
    * ace (0) are worth 1
    * all face cards are worth face value
    * all court cards (11 - 13; jack - king) are worth 10

shoe -> list[int]
    * the deck is shuffled prior to drawing a shoe
    * each shoe has 26 cards
    * all blackjack games in a round are played using duplicates of the same shoe
"""

# generate house deck, the "shoe"
def generate_deck_distribution() -> list[int]:
    # shoe attribute vars
    rank_size = 13
    base = 52

    # deck basis (13 card types, 4 each in base)
    deck = [1 for x in range(rank_size)]

    # generate a distribution at random
    for _ in range(base - rank_size):
        # random card value
        value = secrets.randbelow(13)
        # add card to deck
        deck[value] += 1
    
    # deck is complete
    return deck

# sample a specific portion of the deck
def sample_deck_distribution(deck: list[int], sample_size: int) -> list[int]:
    # start sample
    sample = []

    # copy of deck
    deck_copy = []
    for value in deck:
        deck_copy.append(value)

    # error boundary check: make sure sample size valid
    if sum(deck) < sample_size:
        print("Error: sample size exceeds deck size!")
        sys.exit(1)

    # generate a distribution at random
    while(len(sample) != sample_size):
        # random card value
        value = secrets.randbelow(13)
        # check if card is a valid draw
        if deck_copy[value] > 0:
            # card drawn
            deck_copy[value] -= 1
            # add card to deck
            sample.append(value)
    
    return sample

# shuffle the generated deck
def shuffle_deck(deck: list[int]) -> list[int]:
    # deck basis (13 card types, 4 each in base)
    shuffled_deck = sample_deck_distribution(deck, 52)
    
    # deck is shuffled
    return shuffled_deck

# draw 26 cards from the distribution
# use the same shoe for all tables (for parity)
def draw_shoe(shuffled_deck: list[int]) -> list[int]:
    # new shoe, or hand of 26 cards
    # shoe = sample_deck_distribution(deck, 26)
    shoe = shuffled_deck[0:26]
    
    # deck is shuffled
    return shoe