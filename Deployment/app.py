%%writefile app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Movie Strategy Analyzer", layout="wide")
st.title("🎬 Movie Strategic Quadrant Predictor")

# Sidebar Inputs
title = st.sidebar.text_input("Movie Title", "New Movie")
distributor = st.sidebar.selectbox("Distributor", ["cinema", "streaming"])
runtime = st.sidebar.number_input("Run Time (mins)", value=100)
avg_rating = st.sidebar.slider("IMDb Rating", 1.0, 10.0, 6.5)
num_votes = st.sidebar.number_input("Num Votes", value=1000)
is_original = st.sidebar.checkbox("Is Original?", value=True)
is_franchise = st.sidebar.checkbox("Is Franchise?", value=False)

# Constants (Match your dataset)
MAX_VOTES = 1500000 
MAX_RUNTIME = 250
combined = "new" if is_original and not is_franchise else "old"

# Indices
comm_weight = 1.8 if combined == "old" else 0.8
conv_weight = 1.8 if combined == "new" else 0.8

comm_score = comm_weight * (num_votes / MAX_VOTES) * (runtime / MAX_RUNTIME)
conv_score = conv_weight * (avg_rating / 10) * (1 - (runtime / MAX_RUNTIME))

# Determine Quadrant
if comm_score >= 0.03 and conv_score >= 0.5:
    quadrant = "Scenario 4: Hybrid Logic"
elif comm_score >= 0.03 and conv_score < 0.5:
    quadrant = "Scenario 1: Strong Commitment"
elif comm_score < 0.03 and conv_score >= 0.5:
    quadrant = "Scenario 3: Strong Convenience"
else:
    quadrant = "Scenario 2: Weak Commitment/Convenience"

st.metric("Predicted Quadrant", quadrant)

# Simple Plot
plot_df = pd.DataFrame({'x': [comm_score], 'y': [conv_score], 'Label': [title]})
fig = px.scatter(plot_df, x='x', y='y', text='Label', range_x=[0, 0.2], range_y=[0, 2])
fig.add_vline(x=0.03, line_dash="dash")
fig.add_hline(y=0.5, line_dash="dash")
st.plotly_chart(fig)
