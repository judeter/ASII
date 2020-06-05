# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 16:07:16 2020

@author: cathe
"""
import pandas as pd

# Only northeast states
state_abbreviations = {'ct', 'de', 'me', 'md', 'ma', 'nh', 'nj', 'ny', 'pa',
                       'ri', 'vt', 'dc'}

for state in state_abbreviations:
    filename = 'https://covidtracking.com/api/v1/states/'+state+'/daily.csv'
    data = pd.read_csv(filename)
    data.to_csv('../Data/covidtracking_northeast/'+state+'.csv')
