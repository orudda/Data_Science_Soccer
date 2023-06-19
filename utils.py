import os
import sys

import math

import pandas as pd
import json
pd.set_option('display.max_columns', None)
import matplotlib.pyplot as plt

import socceraction.spadl as spadl
import socceraction.spadl.wyscout as wyscout
import plotly.graph_objects as go
import streamlit as st
import matplotsoccer
from scipy.ndimage import gaussian_filter
from mplsoccer import Pitch, Sbopen, VerticalPitch
from scipy.spatial.distance import pdist, squareform
import numpy as np

class Utils:
    def __init__(self):
        
        self.df_teams = self.loadData('files/teams.json')
        self.df_events = self.loadData('files/events_England.json')
        self.df_matches = self.loadData('files/matches_England.json')
        self.df_passes = self.loadData('files/passes.json')
        self.df_players = self.loadData('files/players.json')
        self.df_spadl = self.loadData('files/spadl.json')
        self.df_merge = self.df_teams_events()
        self.num_subsamples=10

        self.final_position = ['Manchester City', 'Manchester United', 'Tottenham Hotspur', 'Liverpool', 'Chelsea', 
                'Arsenal', 'Burnley', 'Everton', 'Leicester City', 'Newcastle United', 'Crystal Palace',
                'AFC Bournemouth', 'West Ham United', 'Watford', 'Brighton & Hove Albion', 'Huddersfield Town', 
                'Southampton', 'Swansea City', 'Stoke City', 'West Bromwich Albion']
        self.passes = pd.DataFrame(self.df_spadl.loc[(self.df_spadl.type_name == 'pass')])

    def loadData(self, dataname):
        path = os.path.join(dataname)
        with open(path) as f:
            data = json.load(f)

        return pd.DataFrame(data)
    
    def df_teams_events(self):
        self.df_teams['officialName'] = self.df_teams['officialName'].str.decode('unicode-escape')
        df_merge = pd.merge(self.df_events, self.df_teams, left_on='teamId', right_on='wyId', how='left')
        return df_merge
    
    def plotBarChart(self, eventList, labelname):
        df_filtered = self.df_merge[self.df_merge['subEventName'].isin(eventList)]

        df_events = pd.pivot_table(df_filtered, index='name', columns='subEventName', aggfunc='size', fill_value=0)

        df_events['total'] = df_events.sum(axis=1)
        df_events['mean'] = df_events['total'] // 38

        df_events = df_events.reset_index()
        result = df_events[['name', 'total', 'mean']].copy()

        # Sorting by final table
        result.name = result.name.astype("category")
        result.name = result.name.cat.set_categories(self.final_position)

        result = result.sort_values(["name"])[['name', 'total', 'mean']]
        result = result[::-1]
        
        # Criação do gráfico de barras
        fig = go.Figure(data=go.Bar(x=result['mean'], y=result['name'], orientation='h'))

        # Configurações do layout
        fig.update_layout(xaxis_title='Number of '+ labelname,
                        yaxis_title='Team',
                        autosize=False,
                        width=1000,
                        height=700)

        # Exibição do gráfico
        st.plotly_chart(fig)

    def plotHeat(self, x, y, description):
        hm = matplotsoccer.count(x, y, n = 25, m = 25)
        hm = gaussian_filter(hm, 1)

        matplotsoccer.heatmap(matrix = hm, cmap="hot", linecolor="white", cbar=True, show=False, figsize=8)
        plt.title(description)
        st.pyplot(plt)

    def plotPasMap(self, team, gameId):
        # Mapa de Passes Primeiro jogo Man City
        df_passes = self.passes[(self.passes["name"] == team) & (self.passes["result_name"] == "success") & (self.passes['game_id'] == gameId)].copy()

        pitch = Pitch(line_color='black')
        fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
        pitch.arrows(df_passes.start_x, df_passes.start_y, df_passes.end_x, df_passes.end_y, color = "blue", ax=ax['pitch'])

        pitch.scatter(df_passes.start_x, df_passes.start_y, alpha = 0.2, s = 500, color = "blue", ax=ax['pitch'])
        fig.suptitle("{} Passes in the Game {}- 2017-18 PL Season". format(team, gameId), fontsize = 25)

        st.pyplot(plt)

    def createSubsamples(self):
        teams_subsamples_passes = {}
        team_passes_groups = self.passes.groupby('name')

        for team in (self.final_position):
            subsamples = []  # List to store the subsamples

            for _ in range(self.num_subsamples):
                subsample = team_passes_groups.get_group(team)[['start_x', 'start_y', 'end_x', 'end_y', 'name']]\
                            .sample(n=len(team_passes_groups.get_group(team)) // 10)

                subsamples.append(subsample)
            
            teams_subsamples_passes[team] = subsamples
        return teams_subsamples_passes

    def creatHeatSample(self):
        df_list = []
        teams = []
        teams_subsamples_passes = self.createSubsamples()

        for team in (self.final_position):
            for i in range(self.num_subsamples):
                hm = matplotsoccer.count(teams_subsamples_passes[team][i].start_x, teams_subsamples_passes[team][i].start_y, n = 25, m = 25)
                hm = gaussian_filter(hm, 1)

                df_list.append(hm.flatten())    # Converting (25,25) heatmaps to 1D array of (625,)
                teams.append(team)
        return df_list,teams
    
    def plotEuclidian(self):
        df_list,teams = self.creatHeatSample()
        distances = pdist(df_list, metric='euclidean')
        dist_matrix = squareform(distances)
        dist_df = pd.DataFrame(dist_matrix, index=teams, columns=teams)
        dist_df /= np.max(dist_df.values)

        df_distance_mean_row = []

        for index, row in dist_df.iterrows():
            tmp = []
            j = 0

            for i in range(9, 200, 10):
                tmp.append(np.mean(row.values[j:i]))
                j += 10
            
            df_distance_mean_row.append(tmp)
        
        df_distance_mean_col = pd.DataFrame(df_distance_mean_row, index=teams, columns=self.final_position)

        df_distance_mean = []

        for (index, col) in df_distance_mean_col.items():
            tmp = []
            j = 0

            for i in range(9, 200, 10):
                tmp.append(np.mean(col.values[j:i]))
                j += 10
            
            df_distance_mean.append(tmp)

        fig, ax = plt.subplots(figsize=(12,6))
        im = plt.imshow(df_distance_mean, cmap='hot', interpolation='nearest')
        fig.tight_layout()

        plt.colorbar()
        plt.xticks(np.arange(len(df_distance_mean)), df_distance_mean_col.columns, rotation=90)
        plt.yticks(np.arange(len(df_distance_mean)), df_distance_mean_col.columns)

        plt.title('Euclidean Distance Between Pass Heatmaps')
        st.pyplot(plt)


        


    
    

