import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pydeck as pdk
import shapely
import json
import re

st.set_page_config(
    page_title="Net Growth in Housing",
    page_icon = "📈"
)

st.title("Net Growth in Housing 📈")
#--------------------------------------------------------------------------------------------------------------------#
# Import & Prepare Data:
community_district_df = pd.read_csv("data/community_district_data.csv")

# Parse geometry function
def parse_geometry(geom_str):
    json_str = re.sub(r"'", r'"', geom_str)
    return shapely.geometry.shape(json.loads(json_str))

community_district_df['the_geom'] = community_district_df['the_geom'].apply(parse_geometry)
community_district_df = gpd.GeoDataFrame(community_district_df, geometry='the_geom', crs="EPSG:2263")
community_district_df = community_district_df.to_crs("EPSG:4326")

yearly_totals = community_district_df[['comp2010', 'comp2011', 'comp2012', 'comp2013', 'comp2014', 
                                        'comp2015', 'comp2016', 'comp2017', 'comp2018', 'comp2019', 
                                        'comp2020', 'comp2021', 'comp2022', 'comp2023']].sum()
yearly_totals = pd.DataFrame(yearly_totals, columns=['Total']).reset_index()
yearly_totals.columns = ['Year', 'Total']
yearly_totals['Year'] = yearly_totals['Year'].str[4:].astype(int)

# Yearly totals by borough
yearly_totals_by_borough = community_district_df.groupby('borough')[['comp2010', 'comp2011', 'comp2012', 'comp2013', 
                                                                     'comp2014', 'comp2015', 'comp2016', 'comp2017', 
                                                                     'comp2018', 'comp2019', 'comp2020', 'comp2021', 
                                                                     'comp2022', 'comp2023']].sum()
yearly_totals_by_borough = yearly_totals_by_borough.reset_index().melt(id_vars='borough', 
                                                                       var_name='Year', value_name='Total')
yearly_totals_by_borough['Year'] = yearly_totals_by_borough['Year'].str[4:].astype(int)
# Create map:
json_out = json.loads(community_district_df.to_json())

r = "255"
g = "(1 - (properties.Total/26253)) * 255"
b = "(properties.Total/26253) * 255"
fill = f"[{r},{g},{b}]"

geojson = pdk.Layer(
        "GeoJsonLayer",
        json_out,
        pickable=True,
        opacity=1,
        stroked=True,
        filled=True,
        extruded=True,
        wireframe=True,
        auto_highlight=True,
        get_elevation="properties.Total*0.001",
        elevation_scale=100,
        get_fill_color=fill,
    )

tooltip = {
    "html": "<b>Community District:</b> {commntydst}<br>"
            "<b>Net Change in Class-A Units:</b> {Total}<br>"
            "<b>Borough:</b> {borough}",
    "style": {"color": "white", "backgroundColor": "black"}
}

view_state = pdk.ViewState(
    longitude=-73.935242,
    latitude=40.730610,
    zoom=10,
    min_zoom = 9,
    pitch=30,
    bearing=0,
)

# Store map in map
map = pdk.Deck(
    layers=geojson,
    initial_view_state=view_state,
    tooltip=tooltip,
)

#--------------------------------------------------------------------------------------------------------------------#
"""
Housing production is typically driven by new construction and re-development of existing structures that add living spaces.
In large cities such as New York, it is vital to understand where and how much the supply of housing has grown. Between 2010 and 2023, the city 
saw significant changes in its housing landscape, characterized by the demolition and replacement of aging structures, the  repurposing 
of land, and the revitalization of declining communities.

In New York City, Class A housing units generally refer to dwellings typically used exclusively for residential purposes (for example, excluding hotels, lodgings, etc.). In this page, we will look at in particular 
the net growth in Class A housing units across the city between 2010 and 2023. We can see from the figure below that each year since 2012,
Class A housing units has been growing at a steady pace in the city:
"""

yearly_totals_fig = px.line(yearly_totals, x='Year', y='Total', title="Net Change in Class-A Housing Units, 2010-2023")
st.plotly_chart(yearly_totals_fig)

"""
When we look more closely by borough, however, we can see that this growth is certainly not uniform. In particular, 
although the net change in Class-A housing in Manhattan, Queens, and the Bronx appear to grow similarly over time, 
Staten Island seems to underperform all the other four boroughs. On the other hand, Brooklyn appears to regularly
have the highest net change in housing:
"""

yearly_totals_borough_fig = px.line(yearly_totals_by_borough, 
                                    x='Year', y='Total', color='borough', 
                                    title="Net Change in Class-A Housing Units by Borough, 2010-2023").update_layout(legend_title_text='Borough: ', 
                                        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
st.plotly_chart(yearly_totals_borough_fig)

"""
Let's now look more closely at the net change in Class-A housing at community district level. Below is an interactive
map that shows where the most housing has been built from 2010-2023. We can see that the strongest gains in Class-A units
were in Brooklyn and Queens, in particular the Greenpoint/Williamsburg and Woodside/Sunnyside community districts. In
Manhattan, it appears that the Clinton/Chelsea community district on the West Side had the highest net change in housing:
"""

st.pydeck_chart(map)

