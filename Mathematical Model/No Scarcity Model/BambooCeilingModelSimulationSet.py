#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 01:09:39 2022

@author: christinehamakawa
"""

import BambooCeilingModelSimulation as simulation
import pandas as pd

def Set_of_Parameters_Simulations(g1_percentage,
                              g1_assertiveness,
                              g2_assertiveness,
                              Beta,
                              sd,
                              num_start,
                              num_incoming,
                              group_parameters,
                              num_levels,
                              t, num_simulations, file_name):
    name = file_name + ".xlsx"
    first_sim_name = file_name + "_firstrun.xlsx"
    
    for i in range(num_simulations):
        result, time_data = simulation.bamboo_ceiling_simulation(g1_percentage,
                        g1_assertiveness,
                        g2_assertiveness,
                        Beta,
                        sd,
                        num_start,
                        num_incoming,
                        group_parameters,
                        num_levels,t)
        firstCol = result.iloc[:,0]
        lastCol = result.iloc[:,2*num_levels]
        middleCol = result.iloc[:,num_levels]
        timeName = "Time_Exec"
        
        if i == 0:
            firstLeveldf = firstCol
            lastLeveldf = lastCol
            middleLeveldf = middleCol
            time_df = time_data
            result.to_excel(first_sim_name)
        else:
            firstLeveldf = pd.concat([firstLeveldf,firstCol], axis = 1)
            middleLeveldf = pd.concat([middleLeveldf,middleCol], axis = 1)
            lastLeveldf = pd.concat([lastLeveldf,lastCol], axis = 1)
            time_df = pd.concat([time_df,time_data], axis = 0)
    

    writer = pd.ExcelWriter(name, engine = 'xlsxwriter')
    lastLeveldf.to_excel(writer, sheet_name = lastCol.name)
    middleLeveldf.to_excel(writer, sheet_name = middleCol.name)
    firstLeveldf.to_excel(writer, sheet_name = firstCol.name)
    time_df.to_excel(writer, sheet_name = timeName)
    writer.save()
    writer.close()
    
    print("simulations done")

            
        