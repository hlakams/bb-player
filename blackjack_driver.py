# module imports - all other imports done there
import dealer
import attendant
import benchmark

# initialize deck
deck = dealer.generate_deck_distribution()
# # DEBUG
# print("Deck:")
# print(deck, '\n')

# # FINAL
# # real agents in test
names = ["bb", "random", "hi_lo", "ko", "zen", "ten", "halves", "uston"]

# maintain running count of results
results = [["", 0, 0, 0, 0, 0.0, 0.0] for _ in names]

# maximum batch runs
batch_runs = 10

# play some games of blackjack
# play this many batches of games (new deck for each batch)
for batch_no in range(batch_runs):
    # new batch
    batch_no += 1
    
    # 
    for name_idx, name in enumerate(names):
        # base wager as a decimal float
        balance = 1000.00
        wager = 10.00

        # keep track of game results
        wins = 0
        losses = 0
        draws = 0
        games = 100

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

        # # final results per bulk game run
        # print("End results for {} agent:\n".format(name))
        # print("Games: {}".format(games))
        # print("Wins: {}".format(wins))
        # print("Losses: {}".format(losses))
        # print("Draws: {}".format(draws))
        # print("Final win likelihood: {}".format(win_likelhood))
        # print("Final balance: {}".format(balance))

        # store result
        current_result = [name, games, wins, losses, draws, win_likelhood, balance]
        # previous (running) result
        previous_result = results[name_idx]

        results[name_idx] = benchmark.update_results(previous_result, current_result, batch_no)

print(results)