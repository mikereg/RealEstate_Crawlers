#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 19:04:02 2023

@author: michaelreginiano
"""
import pandas as pd
import ast

from collections import Counter
    
df = pd.read_csv('QLC Rent - 2023-10-29.csv')

features = df['Features']
parsed_lists = []

# Parse the strings into actual lists (handle exceptions)
for feat in features:
    try:
        parsed_lists.append(ast.literal_eval(feat))
    except (SyntaxError, ValueError):
        print(f"Error parsing string: {feat}")

# Flatten the Series
flattened_list = sum(parsed_lists, [])

feat_freq = dict(Counter(flattened_list))

Pythonfeat_freq_sorted = sorted(feat_freq.items(),key= lambda item: item[1], reverse=True)