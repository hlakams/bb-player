# module imports - all other imports done there
import dealer
import attendant
import benchmark
import bb_player

# alias for agent names
names = attendant.names

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
        
        # special case for bb-player: update HMM vars
        if name == "bb":
            # transition matrix
            benchmark.transitions = bb_player.init_transitions()
            # emissions matrix
            benchmark.emissions = bb_player.init_emissions()
        
        # action procedures for all games
        for game in range(games):
            # resample deck distribution
            shuffled_deck = dealer.shuffle_deck(deck)
            # subsample of drawn deck
            shoe = dealer.draw_shoe(shuffled_deck)
            # conduct a new game and memoize result
            result = attendant.basic_game(shoe, wager, name)

            # decompose the result tuple
            [winning_hand, wager_outcome, status] = result
            # update running balance for agent
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
        # strategy contents updated with benchmark result
        results[name_idx] = benchmark.update_results(previous_result, current_result, batch_no)

print(results)