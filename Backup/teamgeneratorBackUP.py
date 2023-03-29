import pandas as pd
import streamlit as st
import numpy as np
from scipy.optimize import linprog

# Titles
st.set_page_config(page_title="Teams Generator App")
st.title("Teams Generator App")

# Use sidebar to add instructions and improve layout
with st.sidebar:
    st.markdown("## Instructions")
    st.markdown("Welcome to the teams generator app")
    st.markdown("Created for \"Los lunes al futsal\"")

# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=0", "/export?format=csv")
    return pd.read_csv(csv_url)

df = load_data(st.secrets["public_gsheets_url"])

# Print results.
#for row in df.itertuples():
 #   st.write(f"{row.name} has a :{row.pet}:")
if st.checkbox('Show all players'):
    st.subheader('List of players')
    st.write(df)

# Get the values from the first column of the DataFrame
options = df.iloc[:, 0].unique()

# Create a multiselect widget and get the selected values
st.subheader('Select today\'s players')
selected_values = st.multiselect("Players", options)

#st.write(f"You selected: {selected_values}")

# Create a new DataFrame containing only the selected players
pdfiltered = df[df.iloc[:, 0].isin(selected_values)]

# Show table of players selected 
#if len(pdfiltered)>0:
#    st.subheader('Payers Selected')
#    st.write(pdfiltered)

# Add a submit button to generate the 2 teams
if st.button("Submit"):

    # --------------- GENERATE TEAMS -------------------------

    # Generate two equal teams based on the total points. 
    # Both Teams will have the same number of players or the difference will be 1 player.
    # Both teams will have the same total points or the difference will be the minimum possible
    # Both teams will have the same points by skill or the difference will be the minimum possible. 
    # There are 5 skills rated frorm 1 to 5 (1 is the lowest and 5 is the highest). Each skill rates are saved in columns 2 to 6.
    # The data structure is the first column is Name, the folowing are the skills: Speed,Skill ,Passing,Physical,Shooting
    # A summary of total points by team and by skill is shown at the end of the code.
    # This is a streamlit app.


    # Create a new column for Total points
    pdfiltered['Total'] = pdfiltered.iloc[:, 1:].sum(axis=1)

    # Sort dataframe by total points
    pdfiltered = pdfiltered.sort_values(by=['Total'], ascending=False)

    # Calculate target total points for each team
    target_points = pdfiltered['Total'].sum() // 2

    # Initialize team variables
    team1 = []
    team2 = []
    total_points_team1 = 0
    total_points_team2 = 0

    # Loop through dataframe and add players to teams
    for index, row in pdfiltered.iterrows():
        player_points = row['Total']
        skill_points = row.iloc[1:6].tolist()

        if len(team1) == len(team2):
            if total_points_team1 < total_points_team2:
                team1.append(row['Name'])
                total_points_team1 += player_points
            else:
                team2.append(row['Name'])
                total_points_team2 += player_points
        elif len(team1) > len(team2):
            team2.append(row['Name'])
            total_points_team2 += player_points
        else:
            team1.append(row['Name'])
            total_points_team1 += player_points

        # Check if difference between total points is less than or equal to minimum possible difference
        if abs(total_points_team1 - total_points_team2) <= min(abs(target_points - total_points_team1), abs(target_points - total_points_team2)):
            break

    # Print teams and summary
    print("Team 1:")
    print(team1)
    print("Total Points: ", total_points_team1)
    print("Points by Skill: ", pdfiltered.loc[pdfiltered['Name'].isin(team1)].iloc[:,1:6].sum().tolist())

    print("\nTeam 2:")
    print(team2)
    print("Total Points: ", total_points_team2)
    print("Points by Skill: ", pdfiltered.loc[pdfiltered['Name'].isin(team2)].iloc[:,1:6].sum().tolist())


    st.write(team1)
    st.write(team2)





    # --------------- GENERATE TEAMS -------------------------



    #st.write(f"Teams:")

    # Randomly assign each row to either the blue team or the red team
    # pdfiltered["team"] = np.random.choice(["blue", "red"], size=len(pdfiltered))

    # Split pdfiltered into two DataFrames for each team
 #   blue_team = pdfiltered[pdfiltered["team"] == "blue"]
 #   red_team = pdfiltered[pdfiltered["team"] == "red"]

 #   st.write(f"Teams:")

    # Create two columns to display the teams side-by-side
#    col1, col2 = st.columns(2)
#
#   with col1:
#        st.markdown(f"<h3 style='color: white; background-color: #007bff; padding: 10px;'>Blue Team</h3>", unsafe_allow_html=True)
#        for name in blue_team.iloc[:, 0]:
#            st.markdown(f"<img src='https://img.icons8.com/emoji/24/000000/man-playing-handball--v1.png'/> {name}", unsafe_allow_html=True)
#
#    with col2:
#        st.markdown(f"<h3 style='color: white; background-color: #dc3545; padding: 10px;'>Red Team</h3>", unsafe_allow_html=True)
#        for name in red_team.iloc[:, 0]:
#            st.markdown(f"<img src='https://img.icons8.com/emoji/24/000000/man-playing-handball--v1.png'/> {name}", unsafe_allow_html=True)