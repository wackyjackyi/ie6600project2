from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import altair as alt
import pydeck as pdk

st.title('Project 2: Cooks in the U.S. Workforce: Trends, Challenges, and Opportunities \nBy Qingyi Ji')
st.markdown("""
The project explores the role of cooks in the U.S. workforce by analyzing trends, 
            workforce demographics, and industry-specific insights. 
            I utilized data from DataUSA and visualized it through interactive charts 
            to provide a comprehensive view of employment patterns, workforce composition, and industry distribution. 
""")

# 1. Line Chart: Employment Over Time
url = "https://raw.githubusercontent.com/wackyjackyi/ie6600data/refs/heads/main/ie6600p2/Employment%20Over%20Time.csv"
@st.cache_data
def load_data():
    return pd.read_csv(url)

data = load_data()

st.title("Employment Over Time")

fig = px.line(
    data,
    x="Year",
    y=["Male Population", "Female Population"],
    labels={"value": "Population", "Year": "Year", "variable": "Gender"},
    title="Populations by Gender Over Time",
    color_discrete_map={"Male Population": "lightblue", "Female Population": "pink"}
)

fig.update_layout(
    hovermode="x unified",
    legend_title_text="Gender",
)

st.plotly_chart(fig)

st.markdown("""
The chart shows the population trends of male and female workers over the years from 2014 to 2022.
Both male and female population showed a steady increase until peaking around 2018. 
            After 2018, there is a noticeable decline in the both workforces, which continues through 2022.
            The male workforce remains consistently larger than the female workforce over the entire timeline.
The gap between the male and female populations is significant but narrows slightly in recent years 
            due to the more rapid decline in the male workforce.
Both genders exhibited a peak around 2018, indicating a potential period of maximum employment for cooks.
After 2018, the decline in workforce size could suggest external factors such as economic shifts, 
            industry challenges, or the impact of events like the COVID-19 pandemic.
""")

# 2. Map: Employment by Location
url = "https://raw.githubusercontent.com/wackyjackyi/ie6600data/refs/heads/main/ie6600p2/Employment_By_Location.csv"
@st.cache_data
def load_map_data():
    data = pd.read_csv(url)
    data = data.dropna(subset=['Latitude', 'Longitude'])
    data['Latitude'] = data['Latitude'].astype(float)
    data['Longitude'] = data['Longitude'].astype(float)
    return data

data = load_map_data()

st.title("Employment by Location")

# Filter data by selected year
year_filter = st.selectbox("Select a Year:", options=sorted(data['Year'].unique()))
data = data[data['Year'] == year_filter]

# Filter data by selected State
state_filter = st.selectbox("Select a State:", options=['All'] + sorted(data['State'].unique()))
if state_filter != 'All':
    data = data[data['State'] == state_filter]

data['Average Wage'] = data['Average Wage'].round(2)

# Interactive map with Pydeck
scale_factor = 5
data['Radius'] = data['Average Wage'] * scale_factor

st.pydeck_chart(
    pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=39.8283,
            longitude=-98.5795,
            zoom=4,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=data,
                get_position='[Longitude, Latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius='Radius',  # Use the scaled Radius column
                pickable=True,
            )
        ],
        tooltip={
            "html": "<b>State:</b> {State}<br><b>Average Wage:</b> ${Average Wage}",
            "style": {"color": "white"}
        }
    )
)

st.markdown("""
This map visualizes the average wages of cooks in the United States, categorized by state from 2014 to 2022.
             Larger plot means higher average wage in the state.
            Higher Wages are concentrated in states with higher costs of living (e.g., Hawaii, District of Columbia, Massachusetts).
These regions may also have a strong demand for skilled cooks due to tourism, urban density, and thriving restaurant industries.
Lower Wages are found in states with lower costs of living, particularly in rural or less urbanized areas.
These states likely face lower demand and operate within smaller cuisine markets.
            Cooks looking for higher wages may consider states like Hawaii, D.C., or Massachusetts.
On the other hand, cooks in lower-wage states may find fewer opportunities for competitive pay, 
            though the lower cost of living may balance the earnings.

""")

# 3. Stacked bar chart: Workforce by gender
url_bar = "https://raw.githubusercontent.com/wackyjackyi/ie6600data/refs/heads/main/ie6600p2/workforce_by_gender.csv"
@st.cache_data
def load_data_bar():
    data = pd.read_csv(url_bar)
    data['Year'] = data['Year'].astype(int)
    data['fmale'] = data['fmale'].astype(int)
    data['pmale'] = data['pmale'].astype(int)
    data['ffemale'] = data['ffemale'].astype(int)
    data['pfemale'] = data['pfemale'].astype(int)
    return data

data_bar = load_data_bar()

st.title("Workforce by Gender and Employment Type")

# Year slider with unique key
min_year_bar = data_bar['Year'].min()
max_year_bar = data_bar['Year'].max()
year_bar = st.slider("Select Year for Bar Chart", min_value=min_year_bar, max_value=max_year_bar, value=min_year_bar, key="slider_bar")

# Filter data by selected year
filtered_data_bar = data_bar[data_bar['Year'] == year_bar]

fig_bar = go.Figure()

# full-time and part-time males
fig_bar.add_trace(go.Bar(
    x=['Male'],
    y=filtered_data_bar['fmale'],
    name='Full-Time Male',
    marker_color='navy'
))
fig_bar.add_trace(go.Bar(
    x=['Male'],
    y=filtered_data_bar['pmale'],
    name='Part-Time Male',
    marker_color='lightblue'
))

# full-time and part-time females
fig_bar.add_trace(go.Bar(
    x=['Female'],
    y=filtered_data_bar['ffemale'],
    name='Full-Time Female',
    marker_color='darkred'
))
fig_bar.add_trace(go.Bar(
    x=['Female'],
    y=filtered_data_bar['pfemale'],
    name='Part-Time Female',
    marker_color='pink'
))

fig_bar.update_layout(
    barmode='stack',
    title=f"Workforce Distribution by Gender and Employment Type ({year_bar})",
    xaxis=dict(title="Gender"),
    yaxis=dict(title="Workforce Population"),
    legend=dict(title="Employment Type and Gender"),
    font=dict(size=14)
)

st.plotly_chart(fig_bar)

st.markdown("""
This stacked bar chart visualizes the workforce distribution by gender and employment type (full-time and part-time).
Use the slider to filter data by year.
            From the chart, Male cooks dominate the total workforce, the total workforce size (full-time + part-time) for males is larger than for females.
This reflects a gender imbalance in the profession, with males holding the majority of roles, whether full-time or part-time.
            There are also gender Stereotypes in the Industry, despite cooking being traditionally viewed as a female role in domestic settings, the professional cooking industry (e.g., chefs, line cooks) is male-dominated.
This highlights a disconnect between cultural expectations and workforce representation.

Women may face challenges such as:
Lack of advancement opportunities in professional kitchens.
A male-dominated workplace culture.
Perceived gender biases in hiring or promotion.
These factors could push women into part-time roles or discourage them from entering the profession entirely.
            
""")

# 4.Treemap: Occupations by Industry Group
url_treemap = "https://raw.githubusercontent.com/wackyjackyi/ie6600data/refs/heads/main/ie6600p2/Occupations_by_Industries.csv"
@st.cache_data
def load_data_treemap():
    data = pd.read_csv(url_treemap)
    data['Year'] = data['Year'].astype(int)
    data['Total Population'] = data['Total Population'].astype(int)
    data['Average Wage'] = data['Average Wage'].round(2)
    return data
data_treemap = load_data_treemap()

st.title("Occupations by Industry Group")

# Year slider with unique key
min_year_treemap = data_treemap['Year'].min()
max_year_treemap = data_treemap['Year'].max()
year_treemap = st.slider("Select Year for Treemap", min_value=min_year_treemap, max_value=max_year_treemap, value=min_year_treemap, key="slider_treemap")

# Filter data by selected year
filtered_data_treemap = data_treemap[data_treemap['Year'] == year_treemap]

# Define fixed colors for Industry Sector
unique_sectors = data_treemap['Industry Sector'].unique()
sector_color_map = {sector: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, sector in enumerate(unique_sectors)}

# Assign colors to the filtered data
filtered_data_treemap['Color'] = filtered_data_treemap['Industry Sector'].map(sector_color_map)

fig_treemap = px.treemap(
    filtered_data_treemap,
    path=["Industry Sector", "Industry Group"],
    values="Total Population",
    color="Industry Sector",
    color_discrete_map=sector_color_map,
    hover_data={"Total Population": True, "Average Wage": True},
    labels={"Total Population": "Total Population", "Average Wage": "Average Wage"},
    title=f"Treemap of Industries by Total Population ({year_treemap})",
)

# Increase font size
fig_treemap.update_layout(
    title_font_size=24,
    font=dict(size=16),
)

# Customize hover template
fig_treemap.update_traces(
    hovertemplate="<b>Industry Group:</b> %{label}<br>"
                  "<b>Total Population:</b> %{value}<br>"
                  "<b>Average Wage:</b> $%{customdata[1]:.2f}"
)

st.plotly_chart(fig_treemap)

st.markdown("""
The treemap visually represents the proportion of cooks employed by various industries:
            Restaurants & Food Services occupies the majority of the space.
            Other industries are represented in smaller blocks, scaled by their share of employment.
            Dominance of Restaurants & Food Services:
Restaurants & Food Services overwhelmingly dominate employment for cooks.
This reflects the demand for cooks in food-related businesses, including fast food, casual dining, and fine dining.
However, it also shows a lack of diversity in employment opportunities for cooks, with most jobs concentrated in one industry.
""")

st.title("Conclusion")
st.markdown("""
This project aims to learn about the employment landscape of cooks in the United States. 
            By identifying key trends, regional disparities, and workforce composition, 
            the project highlights challenges such as gender representation and wage disparities while 
            uncovering opportunities for growth and development within the cook profession.
""")
