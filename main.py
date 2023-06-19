import os
import sys
import plotly.graph_objects as go

import math

import pandas as pd
import json
pd.set_option('display.max_columns', None)

from io import BytesIO
from pathlib import Path

import socceraction.spadl as spadl
import socceraction.spadl.wyscout as wyscout

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from utils import Utils

# Configurações de página
st.set_page_config(
    page_title="Ciência de Dados Aplicada ao Futebol",
    page_icon="🎓",
    layout="wide"
)

# Título e cabeçalho
st.title("Ciência de Dados Aplicada ao Futebol")

# Menu de navegação
menu_options = ["Home", "Contributions", "Data", "Visualizations"]
selected_option = st.sidebar.selectbox("Navegação", menu_options)

#Contribuintes
owners = ["Caio Maciel", "Othávio Ruddá"]

utils = Utils()

# Página inicial
if selected_option == "Home":
    st.header("Modelar Inferências Utilizando a Localização dos Passes no Futebol")
    st.write("Aqui você encontrará informações sobre o desenvolvimento do nosso trabalho.")

    st.subheader("Contributors:")
    for i in owners:
        st.write(i)

    st.subheader("Summary")
    for i in menu_options:
        st.write("\t     -"+i)


elif selected_option == "Contributions":
    st.header("Contribuições")
    st.write("Nessa página descrevemos as contribuições de cada aluno")

   
    contributions = {
        "Contribuinte": owners,
        # "contribuição": owners,
        "Work done": [".",
                      ".",]
    }
    cursos_df = pd.DataFrame(contributions)
    cursos_df = cursos_df.reset_index(drop=True)
    st.dataframe(cursos_df)

# Página de contato
elif selected_option == "Data":
    st.header("Data")
    text = "Data from Wyscout 2017-18 Season"
    st.write(text)
    st.header("Teams")
    st.dataframe(utils.df_teams.head())
    st.header("Events")
    st.dataframe(utils.df_events.head())

# Página de dados manual
elif selected_option == "Visualizations":
    st.header("Passes Information")
    listEvents = ['Head pass', 'Simple pass', 'High pass', 'Smart pass', 'Hand pass']
    df = utils.countingEvents(listEvents)
    df['total'] = df.sum(axis=1)
    df = df.sort_values('name', ascending=True)
    df['mean'] = df['total'] // 38
    st.dataframe(df)

    st.header("Passes Plot")
    df = df.sort_values('name', ascending=False)
    utils.plotChart(title='',x_title='Passes',y_title='Teams',x_df=df['mean']	,y_df=df.index)
    
    st.header("Shots Plot")
    listEvents = ['Free kick shot', 'Shot']
    df = utils.countingEvents(listEvents)
    df['total'] = df.sum(axis=1)
    df = df.sort_values('name', ascending=False)
    df['mean'] = df['total'] // 38
    utils.plotChart(title='', x_title='Shots', y_title='Teams', x_df=df['mean'], y_df=df.index)

