# Understanding Housing Growth in New York City
This web app is my first data visuallization app built using Shiny for Python. This app is meant to serve as an interactive guide to understanding the state of housing production in New York City. I present a series of data visualizations and maps using the NYC Department of City Planning’s (DCP) Housing Database. 

The NYC Department of City Planning’s (DCP) Housing Database and contains all NYC Department of Buildings (DOB)-approved housing construction demolition jobs filed or completed in NYC since January 1, 2010. In particular, I make use of datasets at the project-level and community-district level.

Some of the features that this app includes are:
- Data visualizations detailing the net change in Class-A housing units added over time.
- Plots describing how many and how long it takes for projects to receive permits.
- Plots describing how long it takes for projects with permits to complete.
- Map plotting projects that have not been completed as of 2023 Q4.

This app can be run locally by running the '''app.py''' script in the '''src''' folder (currently working on deploying this web app on Render). This repository already contains the datasets used in the web app; to see how the data was retrieved, see '''retrieve_and_clean.py''' in the '''code''' folder.
