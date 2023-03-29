import pandas as pd
import streamlit as st
import numpy as np
import random
from deap import base, creator, tools
import altair as alt

# Titles
st.set_page_config(
    page_title="Teams Generator App",
    initial_sidebar_state="collapsed",
    page_icon="⚽"
    )
st.title("Teams Generator App")



# Use sidebar to add instructions and improve layout
with st.sidebar:
    st.markdown("# About")
    st.markdown("Welcome to the teams generator app")
    st.markdown("Created for \"Los lunes al futsal\"")
    st.write("The genetic algorithm is a search heuristic that is inspired by Charles Darwin's theory of natural selection. It is commonly used to generate high-quality solutions to optimization and search problems by relying on bio-inspired operators such as mutation, crossover and selection.")
    st.write("The algorithm works by creating a population of candidate solutions, then evaluating their fitness. The fitter solutions are more likely to be selected for reproduction. The reproduction process creates offspring by combining the genetic material of multiple parent solutions. The offspring are then mutated to introduce new genetic material into the population. The process is repeated until a satisfactory solution is found.")    
        

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
if st.checkbox('Show players data'):
    st.subheader('List of players')
    st.write(df)

# Get the values from the first column of the DataFrame
options = df.iloc[:, 0].unique()

# Create a multiselect widget and get the selected values, default is all players
st.subheader('Select today\'s players')
selected_values = st.multiselect("Players", options, options, label_visibility="collapsed")

# Show number of players selected
st.write("Number of players selected:", len(selected_values))

# Show table of players selected 
#if len(pdfiltered)>0:
#    st.subheader('Payers Selected')
#    st.write(pdfiltered)

# Add a submit button generate teams
if st.button("Generate Teams"):

    st.markdown("""---""")
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

    # Create a new DataFrame containing only rows where the value in the first column is in selected_values
    pdfiltered = df[df.iloc[:, 0].isin(selected_values)]

  
    with st.spinner('Generating teams...'):
        #calculate total points by player
        pdfiltered['TotalPoints'] = pdfiltered.iloc[:, 1:6].sum(axis=1)

        # Define the fitness function
        def evaluate(individual):
            # Split the players into two teams based on the individual's binary representation
            team1 = pdfiltered.iloc[[i for i in range(len(individual)) if individual[i] == 0]]
            team2 = pdfiltered.iloc[[i for i in range(len(individual)) if individual[i] == 1]]

            # Calculate the difference in total points between the two teams
            diff_total_points = abs(sum(team1['TotalPoints']) - sum(team2['TotalPoints']))

            # Calculate the difference in total points by skill between the two teams
            diff_skill_points = sum([abs(sum(team1[skill]) - sum(team2[skill])) for skill in ['Speed', 'Skill', 'Passing', 'Physical', 'Shooting']])

            # Return a tuple containing both differences (the fitness function will try to minimize these values)
            return (diff_total_points, diff_skill_points)

        # Set up the genetic algorithm
        creator.create('FitnessMin', base.Fitness, weights=(-1.0,-1.0))
        creator.create('Individual', list, fitness=creator.FitnessMin)

        toolbox = base.Toolbox()
        toolbox.register('attr_bool', random.randint, 0, 1)
        toolbox.register('individual', tools.initRepeat, creator.Individual,
                        toolbox.attr_bool, n=len(pdfiltered))
        toolbox.register('population', tools.initRepeat, list,
                        toolbox.individual)
        toolbox.register('evaluate', evaluate)
        toolbox.register('mate', tools.cxTwoPoint)
        toolbox.register('mutate', tools.mutFlipBit,
                        indpb=0.05) 
        toolbox.register('select',
                        tools.selTournament,
                        tournsize=3)

        # Set up parameters for the genetic algorithm
        pop_size = 50 
        num_generations = 100 
        cx_prob = 0.5 
        mut_prob = 0.2 

        # Create initial population
        pop = toolbox.population(n=pop_size)

        # Evaluate initial population
        fitnesses = list(map(toolbox.evaluate,pop))
        for ind ,fit in zip(pop ,fitnesses):
            ind.fitness.values=fit

        for g in range(num_generations):
            # Select parents for reproduction
            offspring=toolbox.select(pop,len(pop))
            
            # Clone selected individuals 
            offspring=list(map(toolbox.clone ,offspring))

            
            # Apply crossover and mutation to offspring
            
            # Crossover
            
            for child1 ,child2 in zip(offspring[::2],offspring[1::2]):
                if random.random()<cx_prob:
                    toolbox.mate(child1 ,child2)
                    del child1.fitness.values 
                    del child2.fitness.values
                    
                    
            # Mutation
            
            for mutant in offspring:
                if random.random()<mut_prob:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values
                    
                    
            # Evaluate new individuals
            
            invalid_ind=[ind for ind in offspring if not ind.fitness.valid]
            fitnesses=map(toolbox.evaluate ,invalid_ind)
            for ind ,fit in zip(invalid_ind ,fitnesses):
                ind.fitness.values=fit
            
            
            # Replace population with new offspring
            
            pop[:]=offspring

        best_individuals=tools.selBest(pop,k=3)

        for bi in best_individuals:
            
            team1=pd.DataFrame(columns=['Name','Speed','Skill','Passing','Physical','Shooting'])
            team2=pd.DataFrame(columns=['Name','Speed','Skill','Passing','Physical','Shooting'])
            
            
            for i,val in enumerate(bi):
                player_row=pd.Series(pdfiltered.iloc[i])
                if val==0:
                    team1=team1.append(player_row ,ignore_index=True)
                else:
                    team2=team2.append(player_row ,ignore_index=True)


        # Create two columns to display the teams side-by-side
        team1_total_points=sum(team1['TotalPoints'])
        team2_total_points=sum(team2['TotalPoints'])



        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"<h3 style='color: white; background-color: #007bff; padding: 10px;'>Blue Team</h3>", unsafe_allow_html=True)
            st.write(len(team1)," players")
            st.metric(label="Team Points", value=team1_total_points, delta=team1_total_points-team2_total_points)
            for name in team1.iloc[:, 0]:
                st.markdown(f"<img src='https://img.icons8.com/metro/20/339AF0/user-male-circle.png'/> {name}", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<h3 style='color: white; background-color: #dc3545; padding: 10px;'>Red Team</h3>", unsafe_allow_html=True)
            st.write(len(team2)," players")
            st.metric(label="Team Points", value=team2_total_points, delta=team2_total_points-team1_total_points)
            for name in team2.iloc[:, 0]:
                st.markdown(f"<img src='https://img.icons8.com/metro/20/FA5252/user-male-circle.png'/> {name}", unsafe_allow_html=True)

    
        team1["team"] = "blue"
        team2["team"] = "red"
        teams=pd.concat([team1 ,team2])


        # Remove the TotalPoints column
        teams = teams.drop(columns=["TotalPoints"])



        # Group the data by team and attribute
        teams_grouped = teams.groupby(['team']).sum()

        # Melt the data to long format
        teams_melted = teams_grouped.reset_index().melt(id_vars=['team'])

        # Create the chart
        st.markdown("""---""")
        chart = alt.Chart(teams_melted).mark_bar().encode(
            y=alt.Y('team:N', axis=alt.Axis(title=None)),
            x=alt.X('value:Q', axis=None),
            color=alt.Color('team:N', legend=None, scale=alt.Scale(domain=['red', 'blue'], range=['#FF9999', '#99CCFF'])),
            row=alt.Row('variable:N', title='')
        ).properties(
            width=400,
            height=100
        )


        # Show the chart in Streamlit
        st.altair_chart(chart, use_container_width=True)






