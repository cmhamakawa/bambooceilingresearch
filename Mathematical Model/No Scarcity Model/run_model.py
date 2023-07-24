#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 09:48:36 2022

@author: christinehamakawa
"""

import pandas as pd
import ast
import BambooCeilingModelSimulationSet as simulation_set
import os
import shutil

# this is what we run --> bamboo ceiling simulation set --> bamboo ceiling simulation --> bamboo ceiling functions

# reading dataframe with rows containing parameters
# INPUTS: SHEET NAME INDEX
run_all = False
parameter_title = 'parameters_w_50'

parameter_sheet_title = parameter_title + '.xlsx'
xls = pd.ExcelFile(parameter_sheet_title)
sheet_names = xls.sheet_names

if run_all is True:
    sheet_name_indices = list(range(len(sheet_names)))
else:
    sheet_name_indices = [0, 1, 2, 3, 4]
    
    
if os.path.isdir(parameter_title):
     os.chdir(parameter_title)
else:
     os.makedirs(parameter_title)
     os.chdir(parameter_title)
og_directory = os.getcwd()
print(og_directory)


for sheet_name_index in sheet_name_indices:                                                                                              
    df = pd.read_excel(xls, sheet_name=sheet_name_index)
    curr_sheet_name = sheet_names[sheet_name_index]
    n_set_of_parameters = df.shape[0]
    if os.path.isdir(curr_sheet_name):
        shutil.rmtree(curr_sheet_name)
        os.makedirs(curr_sheet_name)
        os.chdir(curr_sheet_name)
    else:
        os.makedirs(curr_sheet_name)
        os.chdir(curr_sheet_name)
    for i in range(n_set_of_parameters):
        temp = df.iloc[i,1:]
        temp2 = temp.tolist()
        # adding parameters
        # unpacking
        g1_percentage, g1_assertiveness, g2_assertiveness, Beta, sd, num_start, num_incoming, group_parameters, num_levels, t, num_simulations, name_file = temp2
        g1_assertiveness = ast.literal_eval(g1_assertiveness)
        g2_assertiveness = ast.literal_eval(g2_assertiveness)
        group_parameters = ast.literal_eval(group_parameters)
        sd = ast.literal_eval(sd)
        simulation_set.Set_of_Parameters_Simulations(g1_percentage,
                                  g1_assertiveness,
                                  g2_assertiveness,
                                  Beta,
                                  sd,
                                  num_start,
                                  num_incoming,
                                  group_parameters,
                                  num_levels,
                                  t, num_simulations, name_file)
        
    os.chdir(og_directory)
    print(curr_sheet_name)
    print("Reading one sheet DONE")