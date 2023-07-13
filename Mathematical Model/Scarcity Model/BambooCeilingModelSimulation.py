#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import BambooCeilingModelFunctions as functions
import itertools
import pandas as pd
# add sd
# parameter for this function would be n_trials, total_n, percent_Asian, Asian_a, Non_Asian_a, Beta
# make this a funtion, return a list with 
# L0 percentage, C1 percentage, L1 percentage,....etc
# in other file, have column name contain parameter information
# in other file, have row name be L0, C1, L1, etc.
# k is number of individuals



def bamboo_ceiling_simulation(asian_percentage,
                              asian_assertiveness,
                              nonAsian_assertiveness,
                              Beta,
                              sd,
                              num_start,
                              num_incoming,
                              group_parameters,
                              num_levels,
                              t):
    
    colnames = [""] * (2*num_levels+1)
    for i in range(0,2*num_levels+1):
        temp = int(i/2)
        if i % 2 == 0:
            colnames[i] = "L_" + str(temp)
        else:
            colnames[i] = "C_" + str(temp)
    df = pd.DataFrame(columns=colnames)
    
    
    all_levels = functions.allgroups(2*num_levels, num_start)
    initial_group = functions.create_group(asian_percentage, num_start, asian_assertiveness, nonAsian_assertiveness, 0, sd = (.1, .1))
    starting_index = num_start
    
    for g in range(len(group_parameters)):
        level = group_parameters[g][0]
        n = group_parameters[g][1]
        percentage = group_parameters[g][2]
        num_asian = int(percentage*n)
        new_group = functions.create_group(percentage, n, asian_assertiveness, nonAsian_assertiveness, starting_index, (.1, .1), False)
        initial_group.update(new_group)
        (all_levels[level][0]).extend([i for i in range(starting_index, starting_index+n)])
        starting_index+=n
    
    end_avg = [0]*(2*num_levels+1) # see end of code (output)
    end_count = [0]*(2*num_levels+1)
    for j in range(0,t):
        end_avg = [0]*(2*num_levels+1) # see end of code (output)
        end_count = [0]*(2*num_levels+1)
        num_promoted = 0 # temp value - helps us set up for recursion
        if j > 1:
            new_group = functions.create_group(asian_percentage, num_incoming, asian_assertiveness, nonAsian_assertiveness, starting_index, sd)
            initial_group.update(new_group)
            (all_levels[0][0]).extend([i for i in range(starting_index, starting_index+num_incoming)]) # add individuals to lowest level group (initial group)
            starting_index +=num_incoming # denotes index to start numbering incoming individuals at
        if j >= 1:
            for k in range(2*num_levels,0,-1): # reverse direction
                lastLevIndex = False
                if k == 2*num_levels:
                    lastLevIndex = True
                if k % 2 == 0: # even numbers denote c so we use the alpha probability (2)
                    num_promoted = functions.update_next_group(all_levels[k-1], initial_group, 2, all_levels[k], lastLevIndex, Beta, num_promoted)
                else:
                    num_promoted = functions.update_next_group(all_levels[k-1], initial_group, 1, all_levels[k], lastLevIndex, Beta, num_promoted)
                
        for i in range(0, 2*num_levels+1):
            end_count[i] = end_count[i] + len(all_levels[i][0])
            end_avg[i] = functions.percenta(all_levels[i], initial_group)
        temp = pd.Series(end_avg, index=colnames)
        df = df.append(temp,ignore_index=True)
    # merge all levels so that we can calculate percentage (for percenta function)
    for i in range(0, 2*num_levels+1):
        all_levels[i][0] = list(itertools.chain(*all_levels[i]))
        all_levels[i][1] = []
    for i in range(0, 2*num_levels+1):
        #end_count[i] = end_count[i] + len(all_levels[i][0])
        end_avg[i] = functions.percenta(all_levels[i], initial_group)
    people_data = pd.DataFrame.from_dict(initial_group, orient='index')
    people_data.columns = ['group', 'internal', 'perceived', 'time_end', 'time_pos',
                                'in_company', 'reached_end', 'started_at_0']
    needed_data = people_data[['group', 'time_end', 'reached_end', 'started_at_0']]
    needed_data = needed_data[needed_data['reached_end'] == True]
    needed_data = needed_data[needed_data['started_at_0'] == True]
    needed_data = needed_data.drop(columns=['reached_end', 'started_at_0'])
    return df, needed_data
# this is 1 simulation
# returns percentage at end of t iterations (only at end, we don't see in between)
