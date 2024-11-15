import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pydeck as pdk
import shapely

st.set_page_config(
    page_title="Project Level Analysis",
    page_icon="🔎",
)
st.title("Project Level Analysis 🔎")
#--------------------------------------------------------------------------------------------------------------------#
project_df = pd.read_csv("data/project_level_data.csv", low_memory=False)

# Filter uncompleted projects
incomplete_project_df = project_df[project_df['Job_Status'] != "Completed Construction"]

job_type_count = project_df['Job_Type'].value_counts().reset_index()
job_type_count.columns = ['Job_Type', 'Count']


permit_year_count = project_df['PermitYear'].value_counts().reset_index()
permit_year_count.columns = ['PermitYear', 'Count']
#--------------------------------------------------------------------------------------------------------------------#
"""
We will now examine project-level data in the NYC Department of Planning's Housing Database. The NYC DCP Housing Database
contains all NYC Department of Buildings (DOB)-approved housing construction, alteration, and demolition jobs filed or 
completed in NYC since January 1, 2010. In this analysis, we will look at recorded jobs from this date up until the end of 2023.

The majority of jobs filed on record at the DOB consist of property alterations, followed by new construction, then demolitions.
Between 2010 and 2023, there were almost four times as many jobs filed/approved for building alterations than there were
demolitions (38k vs 10.5k, respectively):
"""
job_type_fig = px.bar(job_type_count, x='Job_Type', y='Count', color ='Job_Type', title = "Number of Records on File by Job Type")
st.plotly_chart(job_type_fig)

"""
Although our dataset consists of building jobs approved and completed between 2010-2023, we can see that many records received permits
pre-2010. This could be due to the fact that some of the records included in our dataset includes jobs completed in the years at/immediately after 2010:
"""
permit_year_fig = px.bar(permit_year_count, x='PermitYear', y='Count')
st.plotly_chart(permit_year_fig)

"""
Among uncompleted projects in our dataset, 60% of jobs on record are already permitted for construction. 23.6% of jobs only got to file applications,
and 15.8% had their applications approved (but are not yet permitted for construction):
"""
pie_chart_fig = px.pie(incomplete_project_df, names='Job_Status', title='Proportion of Job Statuses for Incomplete Projects')
st.plotly_chart(pie_chart_fig)


"""
Obtaining permits is a necessary step in the construction and building modification process since they are a tool that ensures projects comply with 
zoning regulations, codes, and safety standards. However, policymakers, economists, and planners recognize that process of obtaining permits and 
complying with land use regulations can be costly and time-consuming. This can raise the costs of housing production and hinder the growth of housing supply.

One set of natural questions we could ask with our data is, "how long has it typically taken for a project to be permitted once it has been filed?"
Understanding the timeline to permit approval may highlight whether certain types of projects have advantages in the permitting process. 
In the following boxplot figure, we can see that there is substantial variation in the time elapsed from project filing to permit date. Although
the project that has taken the long time to be permitted was an alteration job (7090 days), it appears that the projects that typically take the longest to 
receive permits are new construction jobs, with a median of 253 days.
"""

Days_File_Permit_Box = px.box(project_df, x='Days_File_Permit', y='Job_Type', color = 'Job_Type',
                     title='Days Elapsed from Filing Date to Permit Date, by Job Type (2010-2023)',
                     points=False)  # points=False to exclude outliers
st.plotly_chart(Days_File_Permit_Box)

"""
Alternatively, one could also ask, "how long does it take for a project to be completed once it has been permitted?" We can see from the following boxplot
that demolition projects are typically recorded to be completed on the date the project it is permitted. Additionally, it appears that new construction
projects take slightly longer to complete than alteration projects (with median a time of 821 and 725 days, respectively):
"""

Days_Perm_Comp = px.box(project_df, x='Days_Perm_Comp', y='Job_Type', color = 'Job_Type',
                     title='Days Elapsed from Permit Date to Project Completion, by Job Type (2010-2023)',
                     points=False)  # points=False to exclude outliers

st.plotly_chart(Days_Perm_Comp)