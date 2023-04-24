# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 18:18:37 2023

@author: Graduate
"""

from stat_funcs import per_36_stats, player_stats
import matplotlib.pyplot as plt
import numpy as np

def radar_plotter(player_name):
    stats = player_stats(player_name)
    position = stats.loc['Pos']
    percentiles = per_36_stats(player_name)
    labels = ['PTS', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'MP']
    
    # Create a polar plot
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, polar=True)
    
    # Calculate the angles for each axis of the plot
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    
    # Add the first axis to complete the circle
    angles = np.concatenate((angles, [angles[0]]))
    
    # Normalize the percentile values to be between 0 and 1
    normalized_percentiles = [p / 100 for p in percentiles]
    normalized_percentiles.append(normalized_percentiles[0])
    
    # Plot the radar chart
    ax.plot(angles, normalized_percentiles, 'o-', linewidth=2)
    ax.fill(angles, normalized_percentiles, alpha=0.25)
    
    # Set the labels for each axis
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    
    # Set the limit for the radial axis
    ax.set_ylim([0, 1])
    
    # Add a title to the plot
    plot_caption = f'{player_name} percentiles compared to \n {position} in NBA for 2022-23 season.'
    plt.title(plot_caption, fontsize=10)
    plt.suptitle(f'{player_name} per 36 Minutes', y=1.05, fontsize=18, fontweight='bold')
    
    return fig




def radar_plotter_comp(player1_name, player2_name):
    # Get stats and position for player 1
    stats1 = player_stats(player1_name)
    position1 = stats1.loc['Pos']
    percentiles1 = per_36_stats(player1_name)

    # Get stats and position for player 2
    stats2 = player_stats(player2_name)
    position2 = stats2.loc['Pos']
    percentiles2 = per_36_stats(player2_name)

    labels = ['PTS', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'MP']

    # Create a polar plot
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, polar=True)

    # Calculate the angles for each axis of the plot
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

    # Add the first axis to complete the circle
    angles = np.concatenate((angles, [angles[0]]))

    # Normalize the percentile values to be between 0 and 1 for both players
    normalized_percentiles1 = [p / 100 for p in percentiles1]
    normalized_percentiles1.append(normalized_percentiles1[0])
    normalized_percentiles2 = [p / 100 for p in percentiles2]
    normalized_percentiles2.append(normalized_percentiles2[0])

    # Plot the radar chart for player 1
    ax.plot(angles, normalized_percentiles1, 'o-', linewidth=2, label=player1_name)
    ax.fill(angles, normalized_percentiles1, alpha=0.25)

    # Plot the radar chart for player 2
    ax.plot(angles, normalized_percentiles2, 'o-', linewidth=2, label=player2_name)
    ax.fill(angles, normalized_percentiles2, alpha=0.25)

    # Set the labels for each axis
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)

    # Set the limit for the radial axis
    ax.set_ylim([0, 1])

    # Add a title to the plot
    plot_caption = f'{player1_name} and {player2_name} percentiles compared to {position1} and {position2} in NBA for 2022-23 season.'
    plt.title(plot_caption, fontsize=10)
    plt.suptitle(f'{player1_name} and {player2_name} per 36 Minutes', y=1.05, fontsize=18, fontweight='bold')

    # Add a legend to the plot
    ax.legend(loc='upper right')

    return fig