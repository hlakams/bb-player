# module imports - all other imports done there
import dealer
import attendant

# initialize deck
deck = dealer.generate_deck_distribution()
shuffled_deck = dealer.shuffle_deck(deck)
shoe = dealer.draw_shoe(shuffled_deck)

# base wager as a decimal float
balance = 1000.00
wager = 10.00

# keep track
wins = 0
losses = 0
draws = 0
games = 100

# strategy/agent to run
name = "random"

# play some games of blackjack
for game in range(games):
    # play game
    [winning_hand, wager_outcome, status] = attendant.basic_game(shoe, wager, "bb")
    balance += wager_outcome

    # loss
    if status == 4:
        losses += 1
    # win
    elif status == 5:
        wins += 1
    # draw
    else:
        draws += 1

# calculate win likelihood
win_likelhood = (2 * wins + draws) / (2 * games)

# final results per bulk game run
print("End results for {} agent:\n".format(name))
print("Games: {}".format(games))
print("Wins: {}".format(wins))
print("Losses: {}".format(losses))
print("Draws: {}".format(draws))
print("Final win likelihood: {}".format(win_likelhood))
print("Final balance: {}".format(balance))