# module imports - all other imports done there
import dealer
import attendant

# initialize deck
deck = dealer.generate_deck_distribution()
print("Deck:")
print(deck, '\n')
shuffled_deck = dealer.shuffle_deck(deck)
print("Shuffled deck:")
print(shuffled_deck, '\n')
shoe = dealer.draw_shoe(shuffled_deck)
print("Shoe")
print(shoe, '\n')

# base wager as a decimal float
balance = 1000.00
wager = 10.00

# play some games of blackjack
for game in range(100):
    print("Game #{}".format(game))
    result = attendant.basic_game(shoe, wager)
    # print(result, '\n')
    [winning_hand, wager_outcome, status] = result
    balance += wager_outcome

    # loss
    if status == 4:
        print("You lose!")
        # print("House hand:")
        # print(winning_hand)
        print("Balance: {}\n".format(balance))
    # win
    elif status == 5:
        print("You win!")
        # print("Player hand:")
        # print(winning_hand)
        print("Balance: {}\n".format(balance))
    # draw
    else:
        print("It's a draw...")
        # print("Player hand:")
        # print(winning_hand)
        print("Balance: {}\n".format(balance))