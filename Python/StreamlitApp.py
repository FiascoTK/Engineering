import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from urllib.error import URLError

@st.cache
def ImportYearlyStats():
    StatsDF = pd.read_csv('StatsByYear.csv')
    return StatsDF

StatsDF = ImportYearlyStats()

columns = list(StatsDF.columns)
columns.remove('Year')

header_container = st.container()
stats_container = st.container()

with header_container:
    st.title("Baseball Changes Over a Century")


st.sidebar.checkbox("Show Analysis for Batting Statistic", True, key=1)
select = st.sidebar.selectbox('Choose Batting Statistics',columns)



with stats_container:

        data = StatsDF
        batting_stat = StatsDF[select]

        st.write('### Total by Year')

        baseball_stat_graph = px.line(
                            StatsDF,
                            x ='Year',
                            y = batting_stat,
                            width=1000, height=600
                            )
        st.plotly_chart(baseball_stat_graph)

        st.dataframe(StatsDF)
