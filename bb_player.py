# necessary imports
import numpy as np
import scipy.stats as stats
import collections
from typing import Mapping
import random
import math

import attendant

# Note: we use random here, since secrets does not have a float generator

# TODO: move to attendant class, on access
# initial distribution (can update)
# base_distribution = [4 for _ in range(0,13)]

# new state is updated
states = [x for x in range(0,3)]
sigma = [x for x in range(0,13)]
transitions = collections.defaultdict(lambda: collections.defaultdict(float))
emissions = collections.defaultdict(lambda: collections.defaultdict(float))

# initialize transitions matrix with uniform likelihoods
for prior_state in states:
    for current_state in states:
        transitions[prior_state][current_state] = 1/len(states)

# initialize transitions matrix with uniform likelihoods
for current_state in states:
    for card in sigma:
        emissions[current_state][card] = random.random()

# TODO: move to attendant class
# # new batches need a new distribution
def reset_base(base_distribution):
    # initial observation
    base_distribution = [4 for _ in range(0,13)]
    return base_distribution

# update distribution by range
# we take the selected card and add one more in its range
# two cards from the others are also removed -- pseudo-uniform
def update_distribution(base_distribution: list[int], observed: int) -> list[int]:
    # low
    if observed in range(0, 4):
        # increment hits
        low = random.randint(0,3)
        print(base_distribution)
        print(observed)
        base_distribution[observed] += 1
        base_distribution[low] += 1

        # decrement new hits
        medium = random.randint(4,8)
        high = random.randint(9,12)
        base_distribution[medium] += 1
        base_distribution[high] += 1
    # medium
    elif observed in range(4, 9):
        # increment hits
        medium = random.randint(0,3)
        base_distribution[observed] += 1
        base_distribution[medium] += 1

        # decrement new hits
        low = random.randint(0,3)
        high = random.randint(9,12)
        base_distribution[low] += 1
        base_distribution[high] += 1
    # high
    elif observed is range(9, 13):
        # increment hits
        medium = random.randint(0,3)
        base_distribution[observed] += 1
        base_distribution[high] += 1

        # decrement new hits
        low = range(0,3)
        high = random.randint(4,8)
        base_distribution[low] += 1
        base_distribution[medium] += 1
    
    return base_distribution

# TODO: integrate sample to feed into Viterbi as X
# sample a string from a normalized distribution - "gaussian filter"
def sample_string(distribution: list[int]) -> str:
    # convert base distribution to a set of values
    occurrences = []

    # add values to set
    for idx, hits in enumerate(distribution):
        for _ in range(hits):
            occurrences.append(idx)
    
    # convert set to normal distribution
    mean = np.mean(occurrences)
    stdev = np.std(occurrences)
    normal = stats.lognorm(s=stdev, scale=math.exp(mean))

    # generate a sample of int values in range [0,13]
    sample = normal.rvs(1000)
    sample = np.round(sample)

    # filter output to acceptable range
    output = []
    # max 10 values

    for value in sample:
        print(value)
        if value >= 0 and value <= 12:
            output.append(int(value))
        if len(output) == 10:
            break

    # DEBUG
    print(output)

    # done with current sample
    return output

# find most-likely state-sequence appearance, given a sampled sequence
def maximize_states(x: str) -> str:
    # matrix nodes are [prob, backtrack] for viterbi
    matrix = [[[float('-inf'), 0] for i in range(len(x))] for j in range(len(states))]

    # matrix initialization for first col
    for idx, state in enumerate(states):
        matrix[idx][0][0] = np.log(1/len(states)) + np.log(emissions[state][x[0]])

    # matrix initialization for forwards tracking
    for x_idx, current_symbol in enumerate(x[1:len(x)]):
        for cs_idx, current_state in enumerate(states):
            for ps_idx, prior_state in enumerate(states):
                # current probability
                cumulative_prob = np.log(emissions[current_state][current_symbol]) + np.log(transitions[prior_state][current_state]) + matrix[ps_idx][x_idx][0]
                # conditional probability update
                if cumulative_prob > matrix[cs_idx][x_idx + 1][0]:
                    matrix[cs_idx][x_idx + 1] = [cumulative_prob, ps_idx]

    # backtracking process
    # last column in matrix
    last_column = [x[-1] for x in matrix]
    # get last pointer of maximum likelihood
    max_pointer = max(last_column, key = lambda x:x[0])

    print(last_column)

    # utility vars for hidden path
    max_index = last_column.index(max_pointer)
    max_sequence = [states[max_index]]
    max_pointer = max_pointer[1]

    # backwards tracking for hidden sequence
    for ms_idx, _ in reversed(list(enumerate(x[0:-1]))):
        new_value = [states[max_pointer]]
        max_sequence = [*new_value, *max_sequence]
        max_pointer = matrix[max_pointer][ms_idx][1]

    # output hidden path
    print(max_sequence)
    return max_sequence

# TODO: parameter estimation
def learn_params(hidden_path: str, x: str) -> list[Mapping, Mapping]:
    # declare matrices
    T_update = collections.defaultdict(lambda: collections.defaultdict(float))
    E_update = collections.defaultdict(lambda: collections.defaultdict(float))
        
    # T prior -> current counts
    for i in range(1, len(hidden_path)):
        T_update[hidden_path[i - 1]][hidden_path[i]] += 1.0

    # E state-symbol counts
    for i in range(len(hidden_path)):
        E_update[hidden_path[i]][x[i]] += 1.0

    # new T matrix
    for prior_state in states:
        number_transitions = 0.0
        for current_state in states:
            number_transitions += T_update[prior_state][current_state]
        if number_transitions == 0.0:
            for current_state in states:
                T_update[prior_state][current_state] = 1.0 / len(states)
        else:
            for current_state in states:
                T_update[prior_state][current_state] /= number_transitions

    # new E matrix
    for state in states:
        number_transitions = 0.0
        for symbol in sigma:
            number_transitions += E_update[state][symbol]
        if number_transitions == 0.0:
            for symbol in sigma:
                E_update[state][symbol] = 1.0 / len(sigma)
        else:
            for symbol in sigma:
                E_update[state][symbol] /= number_transitions

    return [T_update, E_update]

# transition, emission probabilities
def learn_probabilities(transitions: Mapping, emissions: Mapping, distribution: list[int]) -> list:
    # sampled string
    sampled_string = sample_string(distribution)

    # iterative viterbi learning 
    for x in range(10):
        state_sequence = maximize_states(sampled_string)
        print(state_sequence)
        [transitions, emissions] = learn_params(state_sequence, sampled_string)
    
    # done with learning
    return [transitions, emissions]

# TODO: action decision tree search, using probabilities
def action_tree_step(current_hand: list[int], state: int, distribution: list[int]):
    [new_transitions, new_emissions] = learn_probabilities(transitions, emissions, distribution)

    # if state == 1:
    #     moves = [7,8,9]
    return 7
