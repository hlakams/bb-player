# module imports - all other imports done there
import dealer
import attendant

# initialize deck
deck = dealer.generate_deck_distribution()
# # DEBUG
# print("Deck:")
# print(deck, '\n')

# old initialization
# shuffled_deck = dealer.shuffle_deck(deck)
# print("Shuffled deck:")
# print(shuffled_deck, '\n')
# shoe = dealer.draw_shoe(shuffled_deck)
# print("Shoe")
# print(shoe, '\n')

# base wager as a decimal float
balance = 1000.00
wager = 10.00

wins = 0
losses = 0
draws = 0
games = 100

name = "random"


# play some games of blackjack
for game in range(games):
    # current game initialization
    # # DEBUG
    # print("Game #{}".format(game))
    shuffled_deck = dealer.shuffle_deck(deck)
    # # DEBUG
    # print("Shuffled deck:")
    # print(shuffled_deck, '\n')
    shoe = dealer.draw_shoe(shuffled_deck)
    # # DEBUG
    # print("Shoe")
    # print(shoe, '\n')
    result = attendant.basic_game(shoe, wager, name)
    # print(result, '\n')
    [winning_hand, wager_outcome, status] = result
    balance += wager_outcome

    # loss
    if status == 4:
        losses += 1
        # DEBUG
        # print("You lose!")
        # print("House hand:")
        # print(winning_hand)
        # print("Balance: {}\n".format(balance))
    # win
    elif status == 5:
        wins += 1
        # DEBUG
        # print("You win!")
        # print("Player hand:")
        # print(winning_hand)
        # print("Balance: {}\n".format(balance))
    # draw
    else:
        draws += 1
        # print("It's a draw...")
        # print("Player hand:")
        # print(winning_hand)
        # print("Balance: {}\n".format(balance))

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