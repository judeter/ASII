"""
Author: Justin Deterding
Created: Mon Apr 20 08:26:10 2020
Description:
"""

import pandas as pd

mobility = pd.read_csv('Global_Mobility_Report.csv')

col_heads = list(mobility.columns.values)
print('Headers:')
for head in col_heads:
    print(' \t', head)
    
us_mobility = mobility[mobility['country_region']=='United States']

nm_mobility = us_mobility[us_mobility['sub_region_1'] == 'New Mexico']

nm_mean_by_date = nm_mobility.groupby('date').mean()
nm_std_by_date = nm_mobility.groupby('date').std()

nm_mean_by_date.plot(subplots=True, figsize=(6, 18))
