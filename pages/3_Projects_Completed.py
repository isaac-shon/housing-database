import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pydeck as pdk
import shapely

st.set_page_config(
    page_title="Projects Completed Each Month",
    page_icon="⌚", layout="wide"
)
st.title("Projects Completed Each Month ⌚")

#--------------------------------------------------------------------------------------------------------------------#
project_df = pd.read_csv("data/project_level_data.csv", low_memory=False)
project_df['DateComplt'] = pd.to_datetime(project_df['DateComplt']).dt.to_period('M')
project_df = project_df.sort_values(by='DateComplt')
#--------------------------------------------------------------------------------------------------------------------#
"""
Explore the interactive maps below to see when and where projects were completed in the city. Use the scroller to navigate any month between January 2010 and January 2024!
"""
fig = px.density_mapbox(
    project_df,
    lat="Latitude",
    lon="Longitude",
    animation_frame="DateComplt",
    radius=5, 
    center=dict(lat=40.7128, lon=-74.0060), 
    zoom=9,  # Zoom level
    mapbox_style="carto-darkmatter"
).update_layout(width=1400, height=800)

# Plot the filtered data on a map
st.plotly_chart(fig)