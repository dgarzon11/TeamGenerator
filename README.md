# Squadmateo - Team Generator App

Squadmateo is a Streamlit-based web application designed to generate balanced teams for games or sports. Utilizing a genetic algorithm, the app aims to create teams that are equal in skill level and total points, ensuring fair and competitive play.

## Features

- **Team Generation with Genetic Algorithm**: Leverages a genetic algorithm to balance teams based on players' skills and total points.
- **Interactive Player Selection**: Users can select players for team generation through an intuitive interface.
- **Real-time Team Visualization**: Displays the generated teams along with their skill distributions and total points.
- **Customizable Algorithm Parameters**: Allows adjustment of genetic algorithm parameters like population size, number of generations, crossover probability, and mutation probability.

## Installation

### Prerequisites

- Python 3
- Required Python libraries: pandas, streamlit, numpy, deap, altair, Pillow
- A dataset of players with their skill ratings in CSV format

### Setup and Running

#### Clone the Repository:
```bash
git clone https://github.com/your-username/squadmateo.git
```
#### Install Dependencies:
```bash
pip install -r requirements.txt
```
#### Set up the Data Source:
Place your players' data CSV file in the project directory or set up a public Google Sheets URL.
If using Google Sheets, add your public sheets URL to st.secrets["public_gsheets_url"] in Streamlit's secrets management.

#### Run the App:
```bash
streamlit run app.py
```
### Usage
After launching the app, use the sidebar to navigate through different sections. In the 'Select Players' section, choose the players who will participate. Click 'GENERATE' to create balanced teams based on the selected players.

### Customization
The genetic algorithm parameters can be adjusted within the code to fine-tune the team generation process.

### License
This project is open source and available under the MIT License.
