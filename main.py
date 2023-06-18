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
    page_title="Visualização de Dados",
    page_icon="🎓",
    layout="wide"
)

# Título e cabeçalho
st.title("Visualização de Dados")
# st.markdown("Bem-vindos ao site da Escola XYZ!")

# Menu de navegação
menu_options = ["Home", "Contribuições", "Dados", "Visualização Manual"]
selected_option = st.sidebar.selectbox("Navegação", menu_options)

#Contribuintes
owners = ["Caio Maciel", "Othávio Ruddá"]

utils = Utils()

# Página inicial
if selected_option == "Home":
    st.header("Bem-vindo ao trabalho de visualização de dados!")
    # st.write("Aqui você encontrará informações sobre nossos cursos, professores e muito mais.")

    st.subheader("Contribuintes:")
    for i in owners:
        st.write(i)

    st.subheader("Sumário")
    for i in menu_options:
        st.write("\t     -"+i)


elif selected_option == "Contribuições":
    st.header("Contribuições")
    st.write("Nessa página descrevemos as contribuições de cada aluno")

   
    contributions = {
        "Contribuinte": owners,
        # "contribuição": owners,
        "Contribuição": ["Desenvolveu a visualização 5 e participou do desenvolvimento do  design do site e do processo de deploy do sistema web.",
                         "Desenvolveu a visualização 1 e 6 e participou do processo de deploy do sistema web.",]
    }
    cursos_df = pd.DataFrame(contributions)
    cursos_df = cursos_df.reset_index(drop=True)
    st.dataframe(cursos_df)

# Página de contato
elif selected_option == "Dados":
    st.header("Dados Utilizados")
    text = "texto de dados"
    st.write(text)
    st.header("Times")
    st.dataframe(utils.df_teams.head())
    st.header("Eventos")
    st.dataframe(utils.df_events.head())


# Página de dados manual
elif selected_option == "Visualização Manual":
    st.header("Total de Passes")
    listEvents = ['Head pass', 'Simple pass', 'High pass', 'Smart pass', 'Hand pass']
    df = utils.countingEvents(listEvents)
    df['total'] = df.sum(axis=1)
    df = df.sort_values('total', ascending=False)
    df['mean'] = df['total']/38
    st.dataframe(df)

    st.header("Gráfico de Passes")
    utils.plotChart(title='Média de Passes por Time',x_title='Time',y_title='Média de Passes',x_df=df.index,y_df=df['mean'])

    listEvents = ['Free kick shot', 'Shot']
    df = utils.countingEvents(listEvents)
    st.header("Gráfico de Chutes")
    df['total'] = df.sum(axis=1)
    df = df.sort_values('total', ascending=False)
    df['mean'] = df['total']/38
    utils.plotChart(title='Média de Chutes por Time',x_title='Time',y_title='Média de Chutes',x_df=df.index,y_df=df['mean'])

