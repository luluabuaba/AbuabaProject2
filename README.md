# Religious/Spiritual Coping Activities Dashboard

## Project Overview
This project is an interactive Dash dashboard built with Python, Dash, Pandas, and Plotly.

The dashboard visualizes 2020 data showing the percentage of respondents who reported using religious or spiritual activities to self soothe after experiencing anxiety or depression severe enough to disrupt regular daily activities for two weeks or longer.

## Features
The dashboard includes:
- An checkbox to include or exclude aggregate regions/continents
- Buttons to compare top or bottom values
- A slider to choose how many entities to display
- A text input to search for a specific country or region

The dashboard also includes:
- A horizontal bar chart
- A histogram
- A world choropleth map
- A summary text output that updates based on the selected filters

## Files in This Repository
- `Project2.py` — main Dash app code, layout, and callback
- `app.py` — file used to run the app
- `dealt-with-anxiety-depression-religious-spiritual.csv` — dataset used in the dashboard
- `requirements.txt` — required Python packages
- `README.md` — project description and instructions

## Installation
Install the required packages with:

```bash
pip install -r requirements.txt
```

## Run the App
To start the dashboard, run:

```
python app.py
```

## How to Use the Dashboard
- Use the checkbox to include or exclude aggregate regions
- Use the buttons to switch between top and bottom values
- Use the slider to change how many entities are displayed
- Use the search box to find a specific country or region
- View the summary text, bar chart, histogram, and map to compare results

## Dataset Note
The dataset reports the percentage of respondents in 2020 who said they engaged in religious/spiritual activities to make themselves feel better after experiencing anxiety or depression severe enough to interfere with their regular daily activities for two weeks or longer.

## Notes
The choropleth map displays only rows with valid country codes. Aggregate regions or continents may not appear on the map.
