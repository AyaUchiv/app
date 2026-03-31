import streamlit as st
import pandas as pd

st.set_page_config(page_title="Movie Strategy Predictor", layout="centered")

# --- HEADER ---
st.title("🎬 Strategic Logic Predictor")
st.markdown("Based on the **Hadida et al. (2021)** Framework of Institutional Logics.")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Input Movie Characteristics")
title = st.sidebar.text_input("Movie Title", "Project X")
distributor = st.sidebar.selectbox("Distributor Type", ["cinema", "streaming"])
runtime = st.sidebar.number_input("Run Time (mins)", min_value=1, value=100)
avg_rating = st.sidebar.slider("IMDb Rating Proxy", 1.0, 10.0, 6.5)
num_votes = st.sidebar.number_input("Num Votes Proxy", min_value=0, value=1000)
is_original = st.sidebar.checkbox("Is Original Content?", value=True)
is_franchise = st.sidebar.checkbox("Is part of a Franchise?", value=False)

# --- DYNAMIC CONSTANTS ---
# We swap the "Max" values based on the distributor to ensure normalized scores
if distributor == "cinema":
    MAX_VOTES = 1491508 
    MAX_RUNTIME = 162
else:
    MAX_VOTES = 128373 
    MAX_RUNTIME = 95

# --- SYSTEM CALCULATIONS ---
# 1. Determine Logic Type
combined = "new" if is_original and not is_franchise else "old"

# 2. Assign Weights
comm_weight = 1.8 if combined == "old" else 0.8
conv_weight = 1.8 if combined == "new" else 0.8

# 3. Calculate Scores (Normalized)
comm_score = comm_weight * (num_votes / MAX_VOTES) * (runtime / MAX_RUNTIME)
conv_score = conv_weight * (avg_rating / 10) * (1 - (runtime / MAX_RUNTIME))

# 4. Determine Scenario (The Quadrant)
if comm_score >= 0.03 and conv_score >= 0.5:
    quadrant = "Scenario 4: Hybrid Logic"
    description = "A blend of both theatrical commitment and digital convenience."
elif comm_score >= 0.03 and conv_score < 0.5:
    quadrant = "Scenario 1: Strong Commitment"
    description = "Theatrical priority. Focus on blockbuster appeal and exclusivity."
elif comm_score < 0.03 and conv_score >= 0.5:
    quadrant = "Scenario 3: Strong Convenience"
    description = "Streaming dominant. Focus on low friction and niche discovery."
else:
    quadrant = "Scenario 2: Weak Commitment/Convenience"
    description = "The 'Struggling' zone. Lacks a clear strategic anchor."

# --- DISPLAY OUTPUTS ---
st.divider()
st.subheader(f"Prediction for: *{title}*")

col1, col2 = st.columns(2)
with col1:
    st.metric("Strategic Scenario", quadrant)
    st.write(f"**Primary Logic:** {combined.upper()}")

with col2:
    st.write(f"**Strategic Insight:** {description}")

st.divider()

# Detailed Technical Data (Collapsible)
with st.expander("View Technical Score Breakdown"):
    st.write(f"Normalized Commitment Score: `{comm_score:.4f}`")
    st.write(f"Normalized Convenience Score: `{conv_score:.4f}`")
    st.info("Scores are normalized against the maximum values in the selected distributor category.")
