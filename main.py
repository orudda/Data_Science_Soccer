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
from classification import Cla

# Configurações de página
st.set_page_config(
    page_title="Ciência de Dados Aplicada ao Futebol",
    page_icon="🎓",
    layout="wide"
)

# Título e cabeçalho
st.title("Ciência de Dados Aplicada ao Futebol")

# Menu de navegação
menu_options = ["Home", "Contributions", "Data", "Visualizations", "Classification"]
selected_option = st.sidebar.selectbox("Navegação", menu_options)

#Contribuintes
owners = ["Caio Maciel", "Othávio Ruddá"]


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

# Página de dados manual
elif selected_option == "Visualizations":
    st.header("Visualização de Dados")
    utils = Utils()
    st.dataframe(utils.passes.head(15))
    utils.plotBarChart(['Simple pass', 'High pass', 'Head pass', 'Smart pass', 'Hand pass'],'passes')
    utils.plotBarChart(['Free kick shot', 'Shot'],'shots')
    # utils.plotChart(title='', x_title='Shots', y_title='Teams', x_df=df['mean'], y_df=df.index)

    st.header("Heatmaps")

    x = utils.passes.start_x
    y = utils.passes.start_y
    utils.plotHeat(x, y, "Passes During 2017-18 PL Season")

    teams = ['Manchester City', 'Arsenal', 'Chelsea', 'West Bromwich Albion']
    for i in teams:
        x = utils.passes[utils.passes['name'] == i].start_x
        y = utils.passes[utils.passes['name'] == i].start_y
        utils.plotHeat(x, y, i+" Passes During 2017-18 PL Season")
    
    utils.plotPasMap(teams[0],2499720)#id do jogo
    utils.plotPasMap(teams[3],2499728)#id do jogo
    utils.plotEuclidian()

elif selected_option == "Classification":
    c=Cla()
