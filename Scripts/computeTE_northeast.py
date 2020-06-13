# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:25:13 2020

@author: cathe
"""
import numpy as np
import pandas as pd
import os
from jpype import startJVM, shutdownJVM, JPackage
import json

def get_min_date(direc):
    mindate = float('-inf')
    for filename in os.listdir(direc):
        state_data = pd.read_csv(direc+filename, usecols=['date'])
        if state_data.min().date > mindate:
            mindate = state_data.min().date
            numrows = state_data.loc[state_data['date'] == mindate].index[0]
    return mindate, numrows+1


def check_dates(direc, mindate, numrows):
    for filename in os.listdir(direc):
        state_data = pd.read_csv(direc+filename, usecols=['date'], nrows=numrows)
        if not state_data.min().date == mindate:
            return False
            #print('{} has different dates'.format(filename.split('.')[0]))  
    return True


def load_data(direc):
    region_data = {}
    mindate, numrows = get_min_date(direc)
    if not check_dates(direc, mindate, numrows):
        raise ValueError('Dates are incorrect')
    population_data = pd.read_csv('../Data/state_population_data.csv').set_index('NAME')['POPESTIMATE2019'].to_dict()
    abbreviations = pd.read_csv('../Data/state_abbreviations.csv').set_index('Code')['State'].to_dict()
    total_pop = 0
    infected = []
    for filename in os.listdir(direc):
        state = abbreviations[(filename.split('.')[0]).upper()]
        population = population_data[state]
        total_pop += population
        #cols = ['date', 'positive', 'negative'] # Thinking of how to incorporate negative tests
        cols = ['date', 'positive']
        state_data = pd.read_csv(direc+filename, usecols=cols, nrows=numrows)
        infected.append(list(state_data['positive']))
        region_data[filename.split('.')[0].upper()] = list(state_data['positive'].div(population))
    infected_in_region = [sum(i) for i in zip(*infected)]
    region_data['_Global_Population_'] = [i/total_pop for i in infected_in_region]
    return region_data


def compute_TE(data, TE_type, state):
    state_data = data[state]
    region_data = data['_Global_Population_']
    
    if TE_type == 'TD':
        source = region_data
        destination = state_data
    elif TE_type == 'BU':
        source = state_data
        destination = region_data
    else:
        raise ValueError('TE_type must be TD or BU')
     
    # 1. Construct the calculator:
    calcClass = JPackage("infodynamics.measures.continuous.kernel").TransferEntropyCalculatorKernel
    calc = calcClass()
    # 2. Set any properties to non-default values:
    calc.setProperty("k_HISTORY", "2")
    # 3. Initialise the calculator for (re-)use:
    calc.initialise()
    # 4. Supply the sample data:
    calc.setObservations(source, destination)
    # 5. Compute the estimate:
    result = calc.computeAverageLocalOfObservations()
    
    print("State: %s with %s-TE = %.4f bits" %
        (state, TE_type, result))
    return result
    #shutdownJVM()


def get_TE(direc, data, TE_type):
    # TE_type is either 'BU' or 'TD'
    entropy = {}
    for filename in os.listdir(direc):
        entropy[filename.split('.')[0].upper()] = compute_TE(data, TE_type,
                filename.split('.')[0].upper())
    jsonfile = json.dumps(entropy)
    f = open('../Data/' + TE_type + 'dict.json', 'w')
    f.write(jsonfile)
    f.close()


# Add JIDT jar library to the path
jarLocation = "C:/Users/cathe/Documents/Courses/CS523/infodynamics-dist-1.4/infodynamics.jar"
# Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
JVMpath = "C:/Program Files/Java/jdk-9.0.1/bin/server/jvm.dll"
startJVM(JVMpath, '-ea', '-Djava.class.path='+jarLocation, convertStrings=False)
   
direc = '../Data/covidtracking_northeast/'
NE_data = load_data(direc)
get_TE(direc, NE_data, 'TD')
get_TE(direc, NE_data, 'BU')
