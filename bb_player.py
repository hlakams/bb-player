# necessary imports
import numpy as np
import scipy.stats as stats
import collections
from typing import Mapping
import random
import math
import benchmark

# Note: we use random here, since secrets does not have a float generator

# static access vars (dictionary)
states = [x for x in range(0,13)]
sigma = [x for x in range(0,13)]

def init_transitions() -> Mapping:
    # use to update new state predictions
    transitions = collections.defaultdict(lambda: collections.defaultdict(float))
    # initialize transitions matrix with uniform likelihoods
    for prior_state in states:
        for current_state in states:
            transitions[prior_state][current_state] = 1/len(states)
    return transitions

def init_emissions() -> Mapping:
    # use to update new state predictions
    emissions = collections.defaultdict(lambda: collections.defaultdict(float))
    # initialize transitions matrix with uniform likelihoods
    for current_state in states:
        for card in sigma:
            emissions[current_state][card] = random.random()
    return emissions

# new batches need a new distribution
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
        base_distribution[observed] += 1
        base_distribution[low] += 1

        # decrement new hits
        medium = random.randint(4,8)
        high = random.randint(9,12)
        base_distribution[medium] -= 1
        base_distribution[high] -= 1
    # medium
    elif observed in range(4, 9):
        # increment hits
        medium = random.randint(0,3)
        base_distribution[observed] += 1
        base_distribution[medium] += 1

        # decrement new hits
        low = random.randint(0,3)
        high = random.randint(9,12)
        base_distribution[low] -= 1
        base_distribution[high] -= 1
    # high
    elif observed is range(9, 13):
        # increment hits
        medium = random.randint(0,3)
        base_distribution[observed] += 1
        base_distribution[high] += 1

        # decrement new hits
        low = range(0,3)
        high = random.randint(4,8)
        base_distribution[low] -= 1
        base_distribution[medium] -= 1
    
    return base_distribution

# integrate sample to feed into Viterbi
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

    # normalization of the observed distribution
    # normal = stats.norm(mean, stdev)
    normal = stats.lognorm(s=stdev, scale=math.exp(mean))

    # generate a sample of int values in range [0,13]
    sample = normal.rvs(1000)
    sample = np.round(sample)

    # filter output to acceptable range
    output = []
    # max 10 values

    for value in sample:
        if value >= 0 and value <= 12:
            output.append(int(value))
        if len(output) == 10:
            break

    # # alternatively, random sample from standardized categorical distribution
    # norm_dist = [x / sum(distribution) for x in distribution]
    # output = np.random.choice([x for x in range(len(distribution))], size = 10, p = norm_dist)

    # done with current sample
    return output

# find most-likely state-sequence appearance, given a sampled sequence
def maximize_states(x: str, transitions: Mapping, emissions) -> str:
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
    return max_sequence

# estimating parameters (emission, transmission)
def learn_params(true_states: str, x: str) -> list[Mapping, Mapping]:
    # declare matrices
    T_update = collections.defaultdict(lambda: collections.defaultdict(float))
    E_update = collections.defaultdict(lambda: collections.defaultdict(float))
        
    # T prior -> current counts
    for i in range(1, len(true_states)):
        T_update[true_states[i - 1]][true_states[i]] += 1.0

    # E state-symbol counts
    for i in range(len(true_states)):
        E_update[true_states[i]][x[i]] += 1.0

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

    return [T_update, E_update, true_states]

# transition, emission probabilities
def learn_probabilities(transitions: Mapping, emissions: Mapping, distribution: list[int]) -> list:
    # sampled string
    sampled_string = sample_string(distribution)

    # iterative viterbi learning
    # prediction for state likelihoods will converge based on frequency of appearance
    for _ in range(10):
        state_sequence = maximize_states(sampled_string, transitions, emissions)
        [transitions, emissions, true_states] = learn_params(state_sequence, sampled_string)
    
    # done with learning
    return [transitions, emissions, true_states, sampled_string]

# action trees
def action_tree_step(transitions: Mapping, emissions: Mapping, current_hand: list[int], game_state: int, distribution: list[int]):
    [new_transitions, new_emissions, true_states, sampled_string] = learn_probabilities(transitions, emissions, distribution)

    # assumption: incoming action status will always be 7
    action_status = 7

    # the aggregate probability of state emissions for the current string
    emissions_probability = 0.0
    for card_idx, card in enumerate(sampled_string):
        emissions_probability += new_emissions[true_states[card_idx]][card]
    
    transitions_probability = 0.0
    for card_idx, card in enumerate(true_states[0:-1]):
        transitions_probability += new_transitions[card][true_states[card_idx + 1]]

    # add-X smoothing for log ratio
    # we use smoothing to prevent divide-by-zero errors, and this is used for the upcoming state
    et_ratio = np.log((emissions_probability + game_state) / (transitions_probability + game_state))
    # expectation of distance to transmit to a valid card state per symbol left
    symbol_distance = (21 - benchmark.blackjack_sum(current_hand)) * abs(et_ratio)

    # posssible_actions: 7, 8, 9
    if game_state == 1:
        if symbol_distance >= 0 and symbol_distance <= 1:
            action_status = 8
        elif symbol_distance > 1 and symbol_distance <= 1.5:
            action_status = 9
        else:
            action_status = 7
    else:
        if symbol_distance >= 0 and symbol_distance <= 1:
            action_status = 8
        else:
            action_status = 7

    return [action_status, new_transitions, new_emissions]
