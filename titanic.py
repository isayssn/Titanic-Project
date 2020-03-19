# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 12:57:46 2019

@author: ISA YASASİN
"""
#1. Obtain and review raw data
import pandas as pd

data = pd.read_csv("cardioActivities.csv")
data.head()
print(data.info())
data = pd.read_csv("cardioActivities.csv", index_col="Date", parse_dates=True)
print(data.info())

#2. Data preprocessing
cols_to_drop = ['Friend\'s Tagged','Route Name','GPX File','Activity Id','Calories Burned', 'Notes']
data.drop(columns=cols_to_drop, axis=1, inplace=True)
print(data.head())
print(data)

data["Type"].value_counts()

data["Type"] = data["Type"].str.replace("Other", "Unicycling")
data[data["Type"] == "Unicycling"] 

data[data["Type"]=="Walking"]['Average Heart Rate (bpm)'].value_counts()

#3. Dealing with missing values
avg_hr_run = data[data["Type"]=="Running"]['Average Heart Rate (bpm)'].mean()
avg_hr_cycle = int(data[data["Type"]=="Cycling"]['Average Heart Rate (bpm)'].mean())

df_run = data[data["Type"] == "Running"]
df_walk = data[data["Type"] == "Walking"]
df_cycle = data[data["Type"] == "Cycling"]

df_run['Average Heart Rate (bpm)'].fillna(int(avg_hr_run), inplace = True)
df_walk['Average Heart Rate (bpm)'].fillna(110, inplace = True)
df_cycle['Average Heart Rate (bpm)'].fillna(int(avg_hr_cycle), inplace = True)

df_cycle
avg_hr_cycle
df_run.isnull().sum()

#4. Plot running data
import matplotlib.pyplot as plt
#runs_subset_2013_2018 = df_run['2018':'2013']
#runs_subset_2013_2018.plot(subplots=True,
#                           sharex=False,
#                           figsize=(12,16),
#                           linestyle='none',
#                           marker='o',
#                           markersize=3,
#                          )
#
#plt.show()

#5. Running statistics
runs_subset_2015_2018 = df_run["2018":"2015"]
print('How my average run looks in last 4 years:')
annualy_mean = runs_subset_2015_2018.resample("A").mean()
print(annualy_mean)

print('Weekly averages of last 4 years:')
weekly_mean = runs_subset_2015_2018.resample("W").mean().mean()
print(weekly_mean)

print('How many trainings per week I had on average:')
weekly_count = runs_subset_2015_2018["Distance (km)"].resample("W").count().mean()
print(weekly_count)

#6. Visualization with averages
runs_subset_2015_2018 = df_run['2018':'2015']
runs_distance = runs_subset_2015_2018['Distance (km)']
runs_hr = runs_subset_2015_2018['Average Heart Rate (bpm)']


#fig, (ax1, ax2) =plt.subplots(2, 1, sharex=True, figsize=(10,8))
#
#runs_distance.plot(ax=ax1)
#ax1.set(ylabel='Distance (km)', title='Historical data with averages')
#ax1.axhline(runs_distance.mean(), color='blue', linewidth=1, linestyle='-.')
#
#runs_hr.plot(ax=ax2, color='gray')
#ax2.set(xlabel='Date', ylabel='Average Heart Rate (bpm)')
#ax2.axhline(runs_hr.mean(), color='blue', linewidth=1, linestyle='-.')
#
#plt.show()


#7. Did I reach my goals?
df_run_dist_annual = df_run['2018':'2013']['Distance (km)'].resample('A').sum()

#fig = plt.figure(figsize=(8,5))

#ax = df_run_dist_annual.plot(marker='*', markersize=14, linewidth=0, color='blue')
#ax.set(ylim=[0, 1210], 
#       xlim=['2012','2019'],
#       ylabel='Distance (km)',
#       xlabel='Years',
#       title='Annual totals for distance')
#
#ax.axhspan(1000, 1210, color='green', alpha=0.4)
#ax.axhspan(800, 1000, color='yellow', alpha=0.3)
#ax.axhspan(1,800, color='red', alpha=0.2)
#
#plt.show()


#8. Am I progressing?
import statsmodels.api as sm

df_run_dist_wkly = df_run['2018':'2013']['Distance (km)'].resample('W').fillna(method = 'bfill')
decomposed = sm.tsa.seasonal_decompose(df_run_dist_wkly, extrapolate_trend=1, freq=52)
#
#fig = plt.figure(figsize=(12,5))
#
#ax = decomposed.trend.plot(label='Trend', linewidth=2)
#ax = decomposed.observed.plot(label='Observed', linewidth=0.5)
#
#ax.legend()
#ax.set_title('Running distance trend')

#plt.show()

#9. Training intensity
hr_zones = [100, 125, 133, 142, 151, 173]
zone_names = ['Easy', 'Moderate', 'Hard', 'Very hard', 'Maximal']
zone_colors = ['green', 'yellow', 'orange', 'tomato', 'red']
df_run_hr_all = df_run['2018':'2015-03']['Average Heart Rate (bpm)']

#fig, ax = plt.subplots(figsize=(8,5))
#
#n, bins, patches = ax.hist(df_run_hr_all, bins=hr_zones, alpha=0.5)
#for i in range(0, len(patches)):
#    patches[i].set_facecolor(zone_colors[i])
#
#ax.set(title='Distribution of HR', ylabel='Number of runs')
#ax.xaxis.set(ticks=hr_zones)
#ax.set_xticklabels(labels=zone_names, rotation=-30, ha='left')
#
#plt.show()


#10. Detailed summary report
# Concatenating three DataFrames
df_run_walk_cycle = df_run.append([df_walk, df_cycle]).sort_index(ascending=False)

dist_climb_cols, speed_col = ['Distance (km)', 'Climb (m)'], ['Average Speed (km/h)']

# Calculating total distance and climb in each type of activities
df_totals = df_run_walk_cycle.groupby('Type')[dist_climb_cols].sum()

print('Totals for different training types:')
print(df_totals)

# Calculating summary statistics for each type of activities 
df_summary = df_run_walk_cycle.groupby('Type')[dist_climb_cols + speed_col].describe()

# Combine totals with summary
for i in dist_climb_cols:
    df_summary[i, 'total'] = df_totals[i]

print('Summary statistics for different training types:')
print(df_summary.stack())



#11. Fun facts
average_shoes_lifetime = 5224 / 7

shoes_for_forrest_run = 24700 // average_shoes_lifetime

print('Forrest Gump would need {} pairs of shoes!'.format(shoes_for_forrest_run))





































