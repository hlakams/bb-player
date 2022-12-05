# BB-Player
A planning method for biased blackjack
> Harsha Lakamsani and Nicholas Ngo, November 2022

# Introduction
To the lay gambler or even advanced players, card counting is an optimal strategy for blackjack. No sleight of hand: it depends on what you know about the shuffled deck as it's being played. The core heuristic is partially informed and weights specific likelihoods over others. Let's take it one step further. The deck is no longer uniformly distributed. There are still four suits, albeit lacking the guarantee of 13 cards each. Each rank will have at least one card. On top of that, you don't know how many decks are in play. Will your naive strategy still work?

We propose a novel approach to "biased" blackjack, named "BB-Player." A Hidden Markov Model (HMM) is used a simulator (with possible sampled action sequences) for RL, extracting Bayesian posterior probabilities. Then, this is used an input for an online decision tree. Stepwise graph search is performed to find the optimal plan.

# Methodology and Constraints
Expanding on the HMM mentioned earlier, we use Viterbi learning through a HMM to simulate the posterior probabilities encountered at each step in a Viterbi graph. We prefer this since the environment is only partially observable: we only have bare knowledge of the minimum card distribution. Plans are constructed piecewise; since blackjack is a three-state game with two kill-states in "stand" and "double" there is only one "true" action state -- "hit".

While standard blackjack tables are played with 6-8 deck 52-card shoes, each game using a single shoe, we use a single 52-card deck and draw 26 cards for the shoe. This reduces runtime complications for reshuffling. Due to this, step-wise optimality is defined here as the move most-likely to lead to a positive state ("Win" or "Double"), over steps which could result in a higher likeihood for a negative state ("Lose" or "Draw"). The distance between the current blackjack hand's sum and 21 is multiplied by the emission:transmission ratio of the observed sequence to form the BFS node decision heuristic.

BB-Player is benchmarked against decision tree methods using naive card-counting heuristics. Methods from Class 1, 2, and 3 are preferred as their heuristic weighting varies slightly (and since they differ in projected levels of ease). We further constrain the system by preventing forfeits and insurance plays.
