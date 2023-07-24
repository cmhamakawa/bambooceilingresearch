#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 20:31:35 2022

@author: christinehamakawa
"""

import random
import itertools
import numpy as np
import math

# IMPORTANT:  groups keep track of the INDEX of the invidual.  These groups are lists.
# The "og group" or "employees" group is a dictionary.
# The individual's information in a group can be accessed by indexing the employees/og group.

# creates initial group of employees
# g1_percentage:  percentage of group 1 individuals in initial group
# total_num:  total num of employees
# a0:  [tuple] internal assertiveness [0], perceived assertiveness of group 1 [1]
# a1:  [tuple] internal assertiveness [0], perceived assertiveness of group 2 [1]
# i is the number to start the key at
# j is the starting index
# sd is standard deviation:  sd[0] is standard deviation for group 1, sd[1] is for group 2

## may need to fix
def create_group(g1_percentage, total_num, a0, a1, j, sd = (.1, .1), start_at_0 = True):
    employees = {}
    num_g1 = g1_percentage * total_num # Number of group 1 individuals in this group
    num_g1 = int(num_g1)
    initial_start = True
    time_pos = 0
    for i in range(j,j + total_num):
        if i < (j+num_g1):
            group = 0 # 0 indicates group 1
            a = random.normalvariate(a0[0], sd[0]) # assertiveness
            alpha = random.normalvariate(a0[1], sd[0]) # perceived assertivness
        else:
            group = 1 # 1 indicates group 2
            a = random.normalvariate(a1[0], sd[1]) # assertiveness
            alpha = random.normalvariate(a1[1], sd[1]) # perceived assertiveness
        # updates dictionary with new individual
        # individual -> [group, assertiveness, perceived assertiveness, time to reach last level, time spent in one position
        # still at company, at last level, started at bottom level]
        # True:  employee still in company
        if start_at_0 == False: # part of pre-filled in individuals
            initial_start = False
            time_pos = random.randint(0, 5) # assume they have been in position 0-5 years
        employees[i] = [group, a, alpha, 0, time_pos, True, False, initial_start]
    return employees # employees consists of all individuals


# P1 probability (moving from L0 to C1)
# a:  assertiveness of individual
def P1(a):
    #print("internal")
    output = a
    return output

# P2 probability (moving from C1 to L1)
# beta:  [0, 1] -- how much assertivenes means to hirer
# alpha:  perceived assertiveness of specific individual
# candidates:  employees being considered for promotion
# employees:  entire group (dictionary)
def P2(beta, alpha, candidates, employees, n):
    #print("perceived")
    num = (1 - beta) + (beta*alpha)# calculates numerator
    #den = 0
    # calculates denominator
    #for i in candidates:
        #den += (1 - beta) + beta*((employees[i])[2])
    return num

# TO DO REPLACEMENET
# HAVE NUMBER TRACKING NUMBER OF PEOPLE THAT LEAVE (promoted or just plain leave)
# 



# updates next_group with individuals that have "advanced" from previous group
# prev_g:  Group of individuals that could potentially move to next group
# og_g:  original group; ALL individuals (dictionary)
# a_alpha:  {1, 2} -- index of individual's list (determines probability functions)
# last Lev Index:  whether or not the current group is the last group (boolean)
# next_g:  next group waiting to add promoted invdividuals
def update_next_group(prev_g, og_g, a_alpha, next_g, lastLevIndex, beta = 1, num_promoted = 2):
    new_add_ons = []
    group_leaving = []
    # NEW VARIABLE:
    # promotion_limit = promo_limit # hardcoded - add variability?
    last_group_leaving = []# we first add those retiring, then extend to those promoted
    
    if lastLevIndex:
        for i in next_g[0]:
            #og_g[i][3] += 1 
            og_g[i][6] = True # MAY NOT NEED
            og_g[i][4] += 1 # add one time stamp to time spent in one position
            input = (1 / og_g[i][4])
            prob_leave1 = .25 - math.tanh(input)
            r2 = random.uniform(0, 1)
            if (r2 < prob_leave1):
                last_group_leaving.append(i)
                og_g[i][5] = False
        for i in last_group_leaving:
            next_g[0].remove(i)
        # num_leave = len(last_group_leaving) - doesn't matter because no scarcity
        
    for i in prev_g[0]:
        if a_alpha == 1:
            P = P1((og_g[i])[1])
        else:
            P = P2(beta, (og_g[i])[2], prev_g[0], og_g, len(prev_g[0]))
        r = random.uniform(0, 1) # generates random number from 0 to 1
        if (r < P):
            new_add_ons.append(i) # INDEX of advancing individual is stored (key, but not value)
            og_g[i][4] = 0 # reset time spent at one position
        else:
            og_g[i][4] += 1 # add one time stamp to time spent in one position
            # FIGURE OUT EQUATION FOR LEAVING
            random_leave = 0#random.normalvariate(.7, .01) # HARDCODED
            input = (1 / og_g[i][4])
            prob_leave =.25 - math.tanh(input) #1 - (inverse_time) #* random_leave)
            r1 = random.uniform(0, 1)
            if (r1 < prob_leave):
                group_leaving.append(i)
                og_g[i][5] = False
        og_g[i][3] += 1 # add one time stamp to time it takes to reach last level
   
    # ADD LIMIT ON PROMOTIONS BY ONLY TAKING THOSE WHO LEAVE
# =============================================================================
#     if lastLevIndex:
#         number_selected = num_leave 
#         new_num_left = num_leave + len(group_leaving)
#     elif a_alpha == 1:
#         number_selected = len(new_add_ons)
#         new_num_left = num_promoted + len(group_leaving) # num_promoted passed in
#     else:
#         number_selected = num_promoted
#         new_num_left = num_promoted + len(group_leaving)
#     random_indices = random.sample(range(0,len(new_add_ons)), number_selected)
#     temp_add_ons = np.array(new_add_ons)
#     new_add_ons = list(temp_add_ons[random_indices])
# =============================================================================

    # group leaving is those "leaving the group/level"
    group_leaving.extend(new_add_ons) # adding those promoted to those retiring
    for i in group_leaving:
        prev_g[0].remove(i)# removes individual from previous group
    next_g[1] = new_add_ons
    # merge previous group's groups together
    prev_g[0] = list(itertools.chain(*prev_g))
    prev_g[1] = []
    if lastLevIndex:
        next_g[0] = list(itertools.chain(*next_g))
        next_g[1] = []
    return 0
        
# counts number of group 1 individuals in the group and group 2 individuals
# returns list [number of group 1, number of group 2]
def percenta(curr_group, og_group):
    groups = [og_group[i][0] for i in curr_group[0]]
    group1 = groups.count(0)
    if len(curr_group[0]) != 0:
        return group1 / len(curr_group[0])
    return 0

# even numbers c's, odd numbers l's
def allgroups(num_groups, group_parameters):
        
    levels = []
    for i in range(0, num_groups+1):
        levels.append([[],[]]) # new two items cuz [1] contains new add ons - don't want them promoted twice
    temp = [i for i in range(group_parameters)]
    levels[0] = [temp, []]
    #for i in range(length(group_parameters)):
        
    return levels



# alpha  = 1: track number of people leaving from previous group (L_)
# alpha = 2: use num_promoted (value should be passed through?)


    
