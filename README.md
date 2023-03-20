# BB-Player
A HMM planning strategy for blackjack
> November 2022 - May 2023

## Background
To the lay gambler or even advanced players, card counting is an optimal strategy for blackjack. No sleight of hand: it depends on what you know about the shuffled deck as it's being played. The core heuristic is partially informed and weights specific likelihoods over others. Let's take it one step further; now, you're playing in a multiplayer online blackjack game.

We propose a novel approach to multiplayer blackjack, named "BB-Player." A Hidden Markov Model (HMM) is used a simulator (with possible sampled action sequences) for RL, extracting Bayesian posterior probabilities. Then, this is used an input for an online decision tree. BFS is performed at each level to find the optimal action node.

## Methodology and Constraints
Expanding on the HMM mentioned earlier, we use Viterbi learning through a HMM to simulate the Bayesian posterior probabilities encountered at each step in a Viterbi graph. We prefer this since the environment is only partially observable: we only have bare knowledge of the minimum card distribution. Plans are constructed piecewise; since blackjack is a three-state game with two kill-states in "stand" and "double," there is only one "true" action state - "hit".

We define step-wise optimality as the move most-likely to lead to a positive state ("Win" or "Double"), over steps which could result in a higher likeihood for a negative state ("Lose" or "Draw"). The distance between the current hand's sum and 21 is add-one smoothed and multiplied by the emission-to-transmission ratio of the observed sequence to expected to form the BFS node decision heuristic.

BB-Player is benchmarked against decision tree methods using naive card-counting heuristics. Methods from Class 1, 2, and 3 are preferred as their heuristic weighting varies slightly (and since they differ in projected levels of ease). We further constrain the system by preventing forfeits and insurance plays.

## Usage
Initialize a Conda environment using `requirements.txt` (note that function type hinting requires Python 3.10+).

Use the following command to benchmark BB-Player against various card counting strategies:
```lang=python
    python3 blackjack_driver.py
```

Alternatively, use the following command to observe BB-Player by itself:
```lang=python
    python3 solo_driver.py
```