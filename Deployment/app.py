import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 1. PAGE SETUP
# ---------------------------------------------------------
st.set_page_config(page_title="Movie Strategic Quadrant Predictor", layout="wide")
st.title("🎬 Movie Strategy & Performance Analyzer")
st.markdown("Enter movie details or upload a dataset to map movies into the **Hadida Strategic Quadrants**.")

# ---------------------------------------------------------
# 2. SIDEBAR INPUTS
# ---------------------------------------------------------
st.sidebar.header("Single Movie Input")

Title = st.sidebar.text_input("Movie Title", "New Movie")
runTime = st.sidebar.number_input("Run Time (minutes)", min_value=1, value=100)
averageRating = st.sidebar.slider("Average Rating (IMDb Proxy)", 1.0, 10.0, 6.5)
numVotes = st.sidebar.number_input("Num Votes (Popularity Proxy)", min_value=0, value=1000)

#toggles
# 1. User flips the switch
is_original_toggle = st.sidebar.toggle("Is the movie an Original?", value=True)
# 2. Convert the True/False into your dataset's words
Original = "Original" if is_original_toggle else "Non-Original"
# 3. Use this label for your calculations
st.sidebar.write(f"Selection: **{Original}**")

# 1. User flips the switch
is_franchise_toggle = st.sidebar.toggle("Is the movie a Franchise?", value=True)
# 2. Convert the True/False into your dataset's words
Franchise = "Franchise" if is_franchise_toggle else "Non-Franchise"
# 3. Use this label for your calculations
st.sidebar.write(f"Selection: **{Franchise}**")

# ---------------------------------------------------------
# 3. CONSTANTS
# ---------------------------------------------------------
MAX_VOTES_cinema = 1491584
MAX_RUNTIME_cinema = 162

MAX_VOTES_streaming = 128373
MAX_RUNTIME_streaming = 95

# ---------------------------------------------------------
# 4. SCORE CALCULATION FUNCTION
# ---------------------------------------------------------
def compute_scores(row):
    combined = "new" if row["Original"] and not row["Franchise"] else "old"
    commitment_weight = 1.8 if combined == "old" else 0.8
    convenience_weight = 1.8 if combined == "new" else 0.8

    commitment = commitment_weight * (row["numVotes"] / MAX_VOTES_cinema) * (row["runTime"] / MAX_RUNTIME_cinema)
    convenience = convenience_weight * (row["averageRating"] / 10) * (1 - (row["runTime"] / MAX_RUNTIME_streaming))

    if commitment >= 0.03 and convenience >= 0.5:
        quadrant = "Scenario 4: Hybrid Logic"
    elif commitment >= 0.03 and convenience < 0.5:
        quadrant = "Scenario 1: Strong Commitment"
    elif commitment < 0.03 and convenience >= 0.5:
        quadrant = "Scenario 3: Strong Convenience"
    else:
        quadrant = "Scenario 2: Weak Commitment/Convenience"

    return pd.Series([commitment, convenience, quadrant, combined])

# ---------------------------------------------------------
# 5. SINGLE MOVIE DATAFRAME
# ---------------------------------------------------------
single_df = pd.DataFrame([{
    "Title": Title,
    "runtime": runTime,
    "avg_rating": averageRating,
    "num_votes": numVotes,
    "is_original": Original,
    "is_franchise": Franchise
}])

single_df[["Commitment", "Convenience", "Quadrant", "LogicType"]] = single_df.apply(compute_scores, axis=1)

# ---------------------------------------------------------
# 6. OPTIONAL CSV UPLOAD
# ---------------------------------------------------------
st.sidebar.header("Upload Movie Dataset (Optional)")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

multi_df = None
if uploaded_file:
    multi_df = pd.read_csv(uploaded_file)

    # Ensure required columns exist
    required_cols = {"Title", "runTime", "averageRating", "numVotes", "Original", "Franchise"}
    if not required_cols.issubset(multi_df.columns):
        st.error(f"CSV must contain columns: {required_cols}")
        multi_df = None
    else:
        multi_df[["Commitment", "Convenience", "Quadrant", "LogicType"]] = multi_df.apply(compute_scores, axis=1)

# ---------------------------------------------------------
# 7. COMBINE DATA FOR PLOTTING
# ---------------------------------------------------------
plot_data = single_df.copy()
if multi_df is not None:
    plot_data = pd.concat([plot_data, multi_df], ignore_index=True)

# ---------------------------------------------------------
# 8. DISPLAY RESULTS
# ---------------------------------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Single Movie Analysis")
    st.metric("Strategic Quadrant", single_df["Quadrant"].iloc[0])
    st.write(f"**Commitment Score:** {single_df['Commitment'].iloc[0]:.4f}")
    st.write(f"**Convenience Score:** {single_df['Convenience'].iloc[0]:.4f}")
    st.write(f"**Logic Type:** {single_df['LogicType'].iloc[0].capitalize()}")

    if multi_df is not None:
        st.subheader("Uploaded Dataset")
        st.dataframe(multi_df)

with col2:
    st.subheader("Strategic Quadrant Plot")

    fig = px.scatter(
        plot_data,
        x="Commitment",
        y="Convenience",
        color="Quadrant",
        text="Title",
        range_x=[0, 0.2],
        range_y=[0, 2.0],
        title="Hadida Strategic Mapping (Single + Multiple Movies)"
    )

    fig.add_vline(x=0.03, line_dash="dash", line_color="gray")
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray")

    st.plotly_chart(fig, use_container_width=True)

st.success(f"Successfully categorized '{Title}' into **{single_df['Quadrant'].iloc[0]}**!")
