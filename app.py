import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import lockdown as ld
# import matplotlib.pyplot as plt

@st.cache
def make_figure(results, title=None):
    median = np.median(results)
    
    fig = make_subplots()

    fig.add_trace(go.Histogram(x=results, nbinsx=40))

    fig.update_layout(
        width=900, height=600,
                xaxis_title="Days in lockdown",
    font = {"size": 10},
    title=title
    )

    return fig

@st.cache
def get_results(probability_day_outbreak=.01, snap_lockdown_time=3,
         probability_lockdown_extension=0.5,
         reduce_in_lockdown=False,
         vaccines=False,
         vaccine_decay=0
         ):
    return ld.sims(N=2000,probability_day_outbreak=probability_day_outbreak, snap_lockdown_time=snap_lockdown_time,
         probability_lockdown_extension=probability_lockdown_extension,
         reduce_in_lockdown=reduce_in_lockdown,
         vaccines=vaccines,
         vaccine_decay=vaccine_decay
         )
            
st.title('Lockdown simulator')

st.sidebar.markdown("## What are the chances of a lockdown?")
probability_day_outbreak = st.sidebar.slider('Chance of new outbreak per day (%)', value=5, min_value=1, max_value=50, step=1)

discount = st.sidebar.checkbox("Reduce outbreak chance during lockdown?", value=True)

snap_lockdown_time = st.sidebar.slider('Snap lockdown initial time (days)', value=7, min_value=3, max_value=21, step=1) 
probability_lockdown_extension = st.sidebar.slider('Chance lockdown extended at end (%)', value=40, min_value=5, max_value=90, step=5) 

vaccination = st.sidebar.checkbox("Vaccination reduces outbreak chance?")
vaccination_rate = st.sidebar.slider("Time to zero outbreak chance (months)", value=12, min_value=3, max_value=36, step=1)

st.sidebar.markdown("""Using these values, we perform 2000 simulated years and count the 
number of days spent in lockdown for each. The figure to the right is a histogram of number of
days spent in lockdown.

We assume that when a new breakout occurs during lockdown,
the lockdown is extended for 7 days; and when we get to the end of each lockdown, if it's extended (due to continued
community transmission) it's extended for 3 days. You can modify these values below.""")

lockdown_outbreak = st.sidebar.slider('Add to lockdown with new outbreak (days)', value=7, min_value=0, max_value=21, step=1) 
lockdown_failed = st.sidebar.slider('Extend lockdowns by (days)', value=3, min_value=1, max_value=21, step=1) 


results = get_results(probability_day_outbreak=probability_day_outbreak/100.0, 
        snap_lockdown_time=snap_lockdown_time,
        probability_lockdown_extension=probability_lockdown_extension/100.0,
        reduce_in_lockdown=discount, 
        vaccines=vaccination, 
        vaccine_decay=vaccination_rate)

fig = make_figure(results[0], title=f"Median days locked down: {int(np.median(results[0]))} days, median lockdowns: {int(np.median(results[1]))}")
st.plotly_chart(fig)






