import os
import sys

import math

import pandas as pd
import json
pd.set_option('display.max_columns', None)

import socceraction.spadl as spadl
import socceraction.spadl.wyscout as wyscout
import plotly.graph_objects as go
import streamlit as st

class Utils:
    def __init__(self):
        
        with open('files/teams.json', 'r') as f:
            data = json.load(f)

        self.df_teams = pd.DataFrame(data)

        with open('files/events_England_.json', 'r') as f:
            data = json.load(f)

        self.df_events = pd.DataFrame(data)
    
    def dfMergedName(self):
        return  pd.merge(self.df_events, self.df_teams, left_on='teamId', right_on='wyId', how='left')
    
    def countingEvents(self,listEvents):
        df = self.dfMergedName()
        df_filtered = df[df['subEventName'].isin(listEvents)]
        df_total_events = pd.pivot_table(df_filtered, index='name', columns='subEventName', aggfunc='size', fill_value=0)
        
        return df_total_events
    
    def sumPasses(self, df):
        return df.sum(axis=1)
    
    def plotChart(self,title, x_title, y_title, x_df, y_df):
        # Criação do gráfico de barras
        fig = go.Figure(data=go.Bar(x=x_df, y=y_df, orientation='h'))

        # Configurações do layout
        fig.update_layout(title=title,
        				autosize=False,
         				width=1000,
   						height=700,
                        xaxis_title=x_title,
                        yaxis_title=y_title)

        # Exibição do gráfico
        st.plotly_chart(fig)

