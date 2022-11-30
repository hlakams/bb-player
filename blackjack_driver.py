# module imports - all other imports done there
import dealer
import attendant
import benchmark
import bb_player

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

    # initialize deck
    deck = dealer.generate_deck_distribution()

    # play X# games with a stable deck
    for name_idx, name in enumerate(names):
        # base wager as a decimal float
        balance = 1000.00
        wager = 10.00

        # keep track of game results
        wins = 0
        losses = 0
        draws = 0
        games = 100

        if name == "bb":
            benchmark.transitions = bb_player.init_transitions()
            benchmark.emissions = bb_player.init_emissions()

        for game in range(games):
            shuffled_deck = dealer.shuffle_deck(deck)

            shoe = dealer.draw_shoe(shuffled_deck)

            result = attendant.basic_game(shoe, wager, name)

            [winning_hand, wager_outcome, status] = result
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

        # store result
        current_result = [name, games, wins, losses, draws, win_likelhood, balance]
        # previous (running) result
        previous_result = results[name_idx]

        results[name_idx] = benchmark.update_results(previous_result, current_result, batch_no)

print(results)