import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image 

# Load the dataset with st.cache_data
@st.cache_data
def load_data():
    return pd.read_csv('ipl_dataset.csv')

# Load data
data = load_data()

ipl_logo = Image.open('ipl_logo.jpg') 

# Sidebar layout
st.sidebar.title("IPL Analysis Dashboard")
option = st.sidebar.selectbox("Choose Analysis", 
                              ["Player Stats", "Match Stats", "Best Bowler", "Best All-Rounder", "Team Performance"])

# Page Title
st.title("IPL Cricket Analysis Dashboard")

# Player Stats Analysis
if option == "Player Stats":
    st.subheader("Player-Wise Statistics")

    player_name = st.sidebar.selectbox("Select Player", data['Player'].unique())

    player_data = data[data['Player'] == player_name]
    
    st.write(f"Statistics for **{player_name}**:")
    st.write(player_data[['Season', 'Team', 'MatchID', 'Runs', 'Wickets', 'Strike Rate', 'Economy Rate', 'Overs Bowled', 'AllRounder Score']])

    # Visualization: Runs & Wickets across seasons
    fig, ax = plt.subplots(1, 2, figsize=(14, 5))
    
    sns.barplot(x="Season", y="Runs", data=player_data, ax=ax[0], palette="Blues_d")
    ax[0].set_title(f"Runs per Season for {player_name}")
    
    sns.barplot(x="Season", y="Wickets", data=player_data, ax=ax[1], palette="Greens_d")
    ax[1].set_title(f"Wickets per Season for {player_name}")
    
    st.pyplot(fig)

# Match Stats Analysis
elif option == "Match Stats":
    st.subheader("Match-Wise Team Statistics")

    match_id = st.sidebar.selectbox("Select Match ID", data['MatchID'].unique())
    
    match_data = data[data['MatchID'] == match_id]
    st.write(f"Statistics for **Match ID {match_id}**:")
    st.write(match_data[['Team', 'Player', 'Runs', 'Wickets', 'Strike Rate', 'Economy Rate', 'Overs Bowled']])

    # Visualization: Team Runs Comparison
    fig = px.pie(match_data, names='Team', values='Runs', title=f'Runs Distribution in Match {match_id}')
    st.plotly_chart(fig)

# Best Bowler Analysis
elif option == "Best Bowler":
    st.subheader("Best Bowler of IPL")

    # Aggregating best bowler stats
    best_bowler = data.groupby('Player').agg({'Wickets': 'sum', 'Economy Rate': 'mean'}).reset_index()
    best_bowler = best_bowler.sort_values(by='Wickets', ascending=False).head(1)

    st.write(f"The best bowler in IPL is **{best_bowler.iloc[0]['Player']}** with **{best_bowler.iloc[0]['Wickets']}** wickets.")

    # Visualization: Wickets by top bowler across seasons
    bowler_data = data[data['Player'] == best_bowler.iloc[0]['Player']]
    fig = px.bar(bowler_data, x='Season', y='Wickets', title=f'Wickets across Seasons for {best_bowler.iloc[0]["Player"]}')
    st.plotly_chart(fig)

# Best All-Rounder Analysis
elif option == "Best All-Rounder":
    st.subheader("Best All-Rounder of IPL")

    # Aggregating best all-rounder stats
    best_allrounder = data.groupby('Player').agg({'Runs': 'sum', 'Wickets': 'sum'}).reset_index()
    best_allrounder['AllRounderScore'] = best_allrounder['Runs'] + best_allrounder['Wickets'] * 20
    best_allrounder = best_allrounder.sort_values(by='AllRounderScore', ascending=False).head(1)

    st.write(f"The best all-rounder in IPL is **{best_allrounder.iloc[0]['Player']}** with **{best_allrounder.iloc[0]['AllRounderScore']}** AllRounder Score.")

    # Visualization: All-rounder performance (Runs & Wickets)
    allrounder_data = data[data['Player'] == best_allrounder.iloc[0]['Player']]
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x='Season', y='Runs', data=allrounder_data, label="Runs", marker="o")
    sns.lineplot(x='Season', y='Wickets', data=allrounder_data, label="Wickets", marker="o")
    ax.set_title(f'All-Rounder Performance for {best_allrounder.iloc[0]["Player"]}')
    st.pyplot(fig)

# Team Performance Analysis
elif option == "Team Performance":
    st.subheader("Team Performance Analysis")

    selected_team = st.sidebar.selectbox("Select Team", data['Team'].unique())

    team_data = data[data['Team'] == selected_team]

    st.write(f"Performance of **{selected_team}** over the seasons:")
    st.write(team_data[['Season', 'Player', 'Runs', 'Wickets', 'Strike Rate', 'Economy Rate']])

    # Visualization: Team performance per season (Total Runs & Wickets)
    team_performance = team_data.groupby('Season').agg({'Runs': 'sum', 'Wickets': 'sum'}).reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='Season', y='Runs', data=team_performance, palette="Blues_d", label="Runs")
    ax2 = ax.twinx()
    sns.lineplot(x='Season', y='Wickets', data=team_performance, ax=ax2, color="green", marker="o", label="Wickets")
    ax.set_title(f'Performance of {selected_team} (Runs & Wickets) across Seasons')
    ax.set_ylabel('Total Runs')
    ax2.set_ylabel('Total Wickets')

    st.pyplot(fig)
