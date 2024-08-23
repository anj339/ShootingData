# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 10:53:09 2024

@author: anjou
"""

import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt 
import numpy as np 

# Load the dataset
nba = pd.read_csv("nba_players_shooting.csv", index_col=0)

# Calculate shooting percentage for each player in each range
shooting_percentage = nba.groupby(['SHOOTER', 'RANGE'])['SCORE'].apply(lambda x: (x == 'MADE').mean()).reset_index()

# Find the range with the highest shooting percentage for each player
best_range = shooting_percentage.loc[shooting_percentage.groupby('SHOOTER')['SCORE'].idxmax()]
print(best_range)


# Filter only made shots
made_shots = nba[nba['SCORE'] == 'MADE']

# Create a scatter plot
plt.figure(figsize=(10, 6))
for shooter in made_shots['SHOOTER'].unique():
    player_shots = made_shots[made_shots['SHOOTER'] == shooter]
    plt.scatter(player_shots['X'], player_shots['Y'], label=shooter)

plt.title('Shots Made by Players')
plt.xlabel('Horizontal Distance (ft)')
plt.ylabel('Vertical Distance (ft)')
plt.legend()
plt.show()


# Calculate the distance from the basket
nba['DISTANCE'] = (nba['X']**2 + nba['Y']**2)**0.5

# Calculate shooting percentage by distance
distance_shooting_percentage = nba.groupby('DISTANCE')['SCORE'].apply(lambda x: (x == 'MADE').mean()).reset_index()

# Create a line plot
plt.figure(figsize=(10, 6))
plt.plot(distance_shooting_percentage['DISTANCE'], distance_shooting_percentage['SCORE'], marker='o')
plt.title('Shooting Percentage by Distance')
plt.xlabel('Distance from Basket (ft)')
plt.ylabel('Shooting Percentage')
plt.show()

# Calculate the number of made shots and total shot attempts for each player
fg_stats = nba.groupby('SHOOTER')['SCORE'].value_counts().unstack().fillna(0)
fg_stats['FG%'] = (fg_stats['MADE'] / (fg_stats['MADE'] + fg_stats['MISSED'])) * 100

# Display the FG% for each player
print(fg_stats[['MADE', 'MISSED', 'FG%']])


# Create a new column for shot success (1 for MADE, 0 for MISSED)
nba['SUCCESS'] = nba['SCORE'].apply(lambda x: 1 if x == 'MADE' else 0)

# Calculate the success rate for each shot location
heatmap_data = nba.groupby(['X', 'Y'])['SUCCESS'].mean().reset_index()

# Pivot the data to create a matrix for the heat map
heatmap_matrix = heatmap_data.pivot('Y', 'X', 'SUCCESS')

import seaborn as sns
import matplotlib.pyplot as plt

# Create the heat map
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_matrix, annot=True, cmap='coolwarm', cbar_kws={'label': 'Success Rate'})
plt.title('Heat Map of Shot Locations and Success Rates')
plt.xlabel('Horizontal Distance (ft)')
plt.ylabel('Vertical Distance (ft)')
plt.show()