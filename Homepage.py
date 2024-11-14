# streamlit run Homepage.py
import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.write("# Welcome to the NYC Housing Dashboard! 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This web app is my first data visualization app built using Streamlit. On this web app, I present a series of data visualizations and maps using the NYC Department of City Planning’s (DCP) Housing Database. 
    At the bottom of this home page, you can see the data and raw code used in this project.

    **👈 Select a page from the sidebar** to see some of the visualizations made in Python!

    ### About the Data 🗽
    The NYC Department of City Planning’s (DCP) Housing Database contains all NYC Department of Buildings (DOB) approved housing construction, alteration and demolition jobs filed or completed in NYC since January 1, 2010. 
    More specifically, the dataset includes construction job types that add or remove residential units, such as new buildings, major alterations, and demolitions. This information can be used to determine 
    the change in legal housing units across time and space. Records in the Housing Database are geocoded to a high level of precision, are subject to numerous quality assurance and control checks, recoded 
    for usability, and are joined to other housing data sources used by city planners and analysts.

    ### Sources
    - Community District-Level Data: [NYC OpenData Link](https://data.cityofnewyork.us/Housing-Development/Housing-Database-by-Community-District/dbdt-5s7j/about_data)
    - Project-Level Data: [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    - Source Code: available [on GitHub](https://github.com/isaac-shon/housing-database) 
    """
)