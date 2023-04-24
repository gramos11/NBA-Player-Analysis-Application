# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 21:49:22 2023

@author: Graduate
"""

import pandas as pd
from radar_plotter import radar_plotter, radar_plotter_comp
from app_funcs import player_search
import streamlit as st
import os

ROSTER_FILE = "roster.csv"
if os.path.exists(ROSTER_FILE):
    roster_df = pd.read_csv(ROSTER_FILE)
else:
    roster_df = pd.DataFrame(columns=["Name", "Wins Produced"])


search_options = ['Player Analysis', 'Roster Analysis']
search_choice = st.sidebar.selectbox("Options", search_options)

if search_choice == 'Player Analysis':
    player_name = st.text_input("Enter the name of a basketball player:")

    if player_name:
        wp = player_search(player_name)
        st.write('Wins Produced in 2022-23: ', wp)
        player_name_2 = st.text_input("Compare to another player: ")
        radar_plot = radar_plotter(player_name)
        st.pyplot(radar_plot)
        
        if player_name_2:
            radar_plot_comp = radar_plotter_comp(player_name, player_name_2)
            st.pyplot(radar_plot_comp)
                
        if st.button('Add player to roster'):
            roster_add = {'Name': player_name, 'Wins Produced': wp}
            roster_df = roster_df.append(roster_add, ignore_index=True)
            roster_df.to_csv(ROSTER_FILE, index=False)
            st.write(roster_df)
            
if search_choice == 'Roster Analysis':
    
    if st.button('Clear Roster'):
        os.remove(ROSTER_FILE)
        ########################################################################
        ####        Right now I am only adding the wins produced data. Depending on what
        ####        data we need to use for our models, this will be the area in which we
        ####        make use of said data.
        roster_df = pd.DataFrame(columns=["Name", "Wins Produced"])
    st.table(roster_df)
        
    
        
        
        
    
