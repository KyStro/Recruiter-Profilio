#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 11:03:41 2019

@author: Kyle Strokes
"""
import numpy as np

obs = [0, 0, 2, 2, 0, 0, 0, 2, 1, 0, 0, 2, 1, 0, 0, 0,
       1, 1, 0, 0, 0, 1, 1, 1, 2, 2, 0, 1, 2, 2, 1, 2, 
       0, 2, 1, 0, 0, 1, 1, 2, 2, 0, 0, 0, 2, 0, 2, 1, 
       2, 2, 0, 1, 1, 0, 2, 2, 2, 2, 2, 2, 1, 1, 2, 0]

transitions = np.array([[0.7, 0.2, 0.1],
                       [0.2, 0.5, 0.3],
                       [0.2, 0.3, 0.6]])

observations = np.array([[0.8, 0.2, 0.0],
                        [0.2, 0.7, 0.1],
                        [0.2, 0.5, 0.3]])

inital_dist = transitions[0]

def get_col_of(matrix, col):
    new = []
    for i in range(len(matrix)):
        new.append(matrix[i][col])
    return new


def get_trans_prob(trans, post, pres):
    return trans[post, pres]
    
def get_obs_prob(obs, state, ob):
    return obs[state, ob]

def get_inital(obs):
    post = []
    #[0.8, 0.2, 0.2]
    col_of_init = get_col_of(observations, obs[0])
    for i in range(len(inital_dist)):
        #[0.7, 0.2, 0.1]
        post.append((inital_dist[i] * col_of_init[i], i))
    #idx_max = np.argmax(post)
    #pair = (idx_max, post[idx_max])
    
    return post
    #[(probability, index), ....]


def default_maxs():
    new = {0: None, 1: None, 2: None}
    return new


def max_4_ends(info, maxs):
    new = info[-1]
    prob = new[0]
    end_state = new[2]
  
    if maxs[end_state] == None:
        maxs[end_state] = new
        return maxs
    if maxs[end_state][0] <= prob:
        maxs[end_state] = new
        return maxs
    return maxs

def maxs_to_inital(maxs):
    new = []
    for key in maxs:
        new.append((maxs[key][0], maxs[key][2]))
    return new

def add_first(inits, results):
    maxo = 0
    maxo_idx = 0
    for tup in inits:
        if maxo <= tup[0]:
            maxo = tup[0]
            max_idx = tup[1]
   
    results.append(maxo_idx)
    return results

def viterbi(obs):
    maxs = {0: None, 1: None, 2: None}
    results = []
    
    inital_t0 = get_inital(obs)
    
    results = add_first(inital_t0, results)
    
    for ob in range(1, len(obs)):
       o = obs[ob]
       for i in range(len(transitions)):
            #for previous state

            info = []

            for j in range(len(transitions)):
                #for end state
                p_next_state = get_trans_prob(transitions, i, j)
                #P(i -> j)
                p_o_given_state = get_obs_prob(observations, j, o)
                #P(observation | i -> j)
                
                info.append((inital_t0[i][0] * p_next_state * p_o_given_state,
                                      i, j, o))
                maxs = max_4_ends(info, maxs)
       most_prob_next = max(maxs, key=maxs.get) 
       # get most probable end state from previous
       results.append(most_prob_next)
       
       inital_t0 = maxs_to_inital(maxs)
       # set maxs to inital list for iteration
       maxs = {0: None, 1: None, 2: None}

    #print(results) 
       
    return results
                      

