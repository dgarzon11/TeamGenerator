import pandas as pd
import streamlit as st
import numpy as np
from scipy.optimize import linprog
import pulp

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

# Create a new DataFrame containing only rows where the value in the first column is in selected_values
pdfiltered = df[df.iloc[:, 0].isin(selected_values)]

# Show table of players selected 
#if len(pdfiltered)>0:
#    st.subheader('Payers Selected')
#    st.write(pdfiltered)

# Add a submit button to go to the welcome page
if st.button("Submit"):

    # --------------- GENERATE TEAMS -------------------------

    # Generate two equal teams based on the total points. 
    # Both Teams will have the same number of players or the difference will be 1 player.
    # Both teams will have the same total points or the difference will be the minimum possible
    # Both teams will have the same points by skill or the difference will be the minimum possible. 
    # All players must be assigned to a team.
    # There are 5 skills rated frorm 1 to 5 (1 is the lowest and 5 is the highest). Each skill rates are saved in columns 2 to 6.
    # The data structure is the first column is Name, the folowing are the skills: Speed,Skill ,Passing,Physical,Shooting
    # A summary of total points by team and by skill is shown at the end of the code.
    # This is a streamlit app.


    def generate_teams(players_data):

        #sum all points of each player
        players_data['Total Points'] = players_data.iloc[:, 2:].sum(axis=1)

        # Define variables
        st.write("test1")
        st.write(players_data)
        st.write(players_data['Name'])
        
        names = pdfiltered['Name'].tolist()
        
        points = players_data.iloc[:, 2:].sum(axis=1)
        
        skills = players_data.iloc[:, 2:].values.tolist()
        
        num_players = len(names)
        num_skills = len(skills[0])
        num_teams = 2
        
        

        # Create optimization problem
        prob = pulp.LpProblem("Team Assignment", pulp.LpMinimize)
        

        # Create variables
        team_vars = pulp.LpVariable.dicts("Team", range(num_teams), cat=pulp.LpBinary)
        player_vars = pulp.LpVariable.dicts("Player", names, cat=pulp.LpBinary)
          
        st.write("test1")
        # Set objective function
        players_data.loc[:, 'Total Points'] = players_data.iloc[:, 2:].sum(axis=1)
        st.write("test2") 

        # Add constraints
        prob += pulp.lpSum([team_vars[t] for t in range(num_teams)]) == num_teams
        for i in range(num_players):
            prob += pulp.lpSum([team_vars[t] * player_vars[names[i]] for t in range(num_teams)]) == 1
        for s in range(num_skills):
            skill_vars = [pulp.lpSum([skills[i][s] * player_vars[names[i]] for i in range(num_players) if team_vars[t].value() == 1]) for t in range(num_teams)]
            prob += pulp.lpSum(skill_vars) <= max(skill_vars) - min(skill_vars) + 1

        # Solve problem
        prob.solve()

        # Print results
        team1 = [names[i] for i in range(num_players) if player_vars[names[i]].value() == 1 and team_vars[0].value() == 1]
        team2 = [names[i] for i in range(num_players) if player_vars[names[i]].value() == 1 and team_vars[1].value() == 1]
        print("Team 1:", team1)
        print("Team 2:", team2)

        # Summary of total points by team and by skill
        team_points = [sum([points[i] for i in range(num_players) if player_vars[names[i]].value() == 1 and team_vars[t].value() == 1]) for t in range(num_teams)]
        print("Team points:", team_points)

        team_skills = [[sum([skills[i][s] for i in range(num_players) if player_vars[names[i]].value() == 1 and team_vars[t].value() == 1]) for s in range(num_skills)] for t in range(num_teams)]
        print("Team skills:", team_skills)


        return team1, team2


    # Generate the two teams
    team1, team2 = generate_teams(pdfiltered)

    # Print the two teams
    st.subheader("Team 1")
    st.write(team1)

    st.subheader("Team 2")
    st.write(team2)

    # Calculate the total points and points by skill for each team
    #team1_total_points = team1["Total"].sum()
    #team2_total_points = team2["Total"].sum()

    #st.write(team1)
    #st.write(team2)
    





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