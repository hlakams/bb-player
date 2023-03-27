# module imports - all other imports done there
import dealer
import attendant

# library imports
import warnings

# silence misc warnings
warnings.filterwarnings(action='ignore', category=RuntimeWarning)

# base wager as a decimal float
initial_balance = 1000.00
running_balance = 0
wager = 10.00

# keep track (for all games)
wins = 0
losses = 0
draws = 0

# testing params
games = 100
epochs = 10

# strategy/agent to run
name = "bb"


for epoch in range(epochs):
    balance = initial_balance
    # initialize deck
    deck = dealer.generate_deck_distribution()
    shuffled_deck = dealer.shuffle_deck(deck)
    shoe = dealer.draw_shoe(shuffled_deck)

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

    running_balance += balance

# calculate win likelihood
win_likelhood = (2 * wins + draws) / (2 * (games * epochs))

# final results per bulk game run
# print("Results for Epoch #{}".format(epoch + 1))
print("End results for {} agent:".format(name))
print("Games: {}".format(games * epochs))
print("Wins: {}".format(wins))
print("Losses: {}".format(losses))
print("Draws: {}".format(draws))
print("Final win likelihood: {}".format(win_likelhood))
print("Final balance: {}".format(balance))
print("Running balance multiplier: {}\n".format(running_balance/epochs/initial_balance))