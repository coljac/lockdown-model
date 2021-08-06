import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import lockdown as ld
# import matplotlib.pyplot as plt

@st.cache
def make_figure(results, offset=True):
    median = np.median(results)
    
    fig = make_subplots()

    fig.add_trace(go.Histogram(x=results, nbinsx=40))
                            # y=[z['principle'] for z in results],
                    # hovertemplate = '%{x:.1f} years<br>\nPrinciple: %{y:$,.0f}<extra></extra>',
                    # mode='lines+markers',
                    # name='Principle remaining'))
    # fig.add_trace(go.Scatter(x=[z['month']/12 for z in results], 
                            # y=[z['interest_paid'] for z in results],
                    # hovertemplate = '%{x:.1f} years<br>\nInterest: %{y:$,.0f}<extra></extra>',
                    # mode='lines+markers',
                    # name='Interest paid'))
    # if offset:
        # fig.add_trace(go.Scatter(x=[z['month']/12 for z in results], 
                            # y=[z['offset'] for z in results],
                    # mode='lines+markers',
                    # hovertemplate = '%{x:.1f} years<br>\nOffset: %{y:$,.0f}<extra></extra>',
                    # name='Offset account balance'))

    fig.update_layout(
        width=900, height=600,
                xaxis_title="Days in lockdown",
    # yaxis_title="Loan value",
    font = {"size": 10},
    title=f"Median: {int(median)} days",
    # legend=dict(
        # yanchor="top",
        # y=0.99,
        # xanchor="left",
        # x=0.6
    )

    return fig

@st.cache
def get_results(probability_day_outbreak=.01, snap_lockdown_time=3,
         probability_lockdown_extension=0.5):
    return ld.sims(N=5000,probability_day_outbreak=probability_day_outbreak, snap_lockdown_time=snap_lockdown_time,
         probability_lockdown_extension=probability_lockdown_extension)
            
st.title('Lockdown simulator')

st.sidebar.markdown("## What are the chances of a lockdown?")
probability_day_outbreak = st.sidebar.slider('Chance of new outbreak per day', value=0.05, min_value=0.01, max_value=.5, step=.01)

snap_lockdown_time = st.sidebar.slider('Snap lockdown initial time', value=7, min_value=3, max_value=21, step=1) 
probability_lockdown_extension = st.sidebar.slider('Chance lockdown extended', value=.4, min_value=.1, max_value=0.9, step=.1) 

results = get_results(probability_day_outbreak=probability_day_outbreak, snap_lockdown_time=snap_lockdown_time, probability_lockdown_extension=probability_lockdown_extension)

fig = make_figure(results)

st.plotly_chart(fig)






