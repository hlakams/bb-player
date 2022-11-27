# biased-blackjack
A planning method for biased blackjack
> Harsha Lakamsani and Nicholas Ngo, November 2022

# Introduction
To the lay gambler or even advanced players, card counting is an optimal strategy for blackjack. No sleight of hand: it depends on what you know about the shuffled deck as it's being played. The core heuristic is partially informed and weights specific likelihoods over others.

Let's take it one step further. The deck is no longer uniformly distributed, like the standard we're all familiar with. There are still four suits, albeit lacking the guarantee of 13 cards each. Each rank, however, has at least one card. Will your naive strategy still work?

We propose a novel approach to "biased" blackjack, named "BB-Player." A Hidden Markov Model (HMM) is used a simulator for MDP RL, extracting Bayesian posterior probabilities. Then, this is used an input for an online decision tree. Online search is performed to find the optimal plan.

# Background
(need to fill)

# Methodology and Constraints
Expanding on the HMM mentioned earlier, we use Viterbi learning through a HMM to simulate the posterior probabilities encountered at each step in a Viterbi graph. We prefer this since the environment is only partially observable: we only have bare knowledge of the minimum card distribution.

Our step-wise optimality is defined as the move most-likely to lead to a positive state ("Win" or "Double"), over steps which could result in a higher likeihood for a negative state ("Lose" or "Draw").

BB-Player is benchmarked against decision tree methods using naive card-counting heuristics. Methods from Class 1, 2, and 3 are used as their heuristic weighting varies slightly (and since they differ in projected levels of ease).
