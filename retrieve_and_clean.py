import os
import requests
import zipfile
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
from shapely import wkt

#----------------------------------------------------------#
'''
GET COMMUNITY-DISTRICT & PROJECT-LEVEL HOUSING DATABASE:
'''
community_district_url = 'https://data.cityofnewyork.us/resource/dbdt-5s7j.json'

def fetch_data(url, params=None):
    '''
    This function fetches data from the urls defined above and stores
    them in a pandas datafrome. The function als returns a message 
    if the online data retrieval was a success.
    '''
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        print(f"Failed to retrieve data from {url}: Status {response.status_code}")
        return None

# Load data to df's by calling function:
community_district_df = fetch_data(community_district_url)
#----------------------------------------------------------#
# We will use the csv file instead. This is because the ArcGIS data is limited to only 32,000 observations:
project_level_url = 'https://s-media.nyc.gov/agencies/dcp/assets/files/zip/data-tools/bytes/nychdb_23q4_csv.zip'
response = requests.get(project_level_url)

zip_path = os.path.join('src','data', f'project_level_database.zip')
    
with open(zip_path, 'wb') as f:
    f.write(response.content)
        
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall('src\\data\\')

project_df = pd.read_csv('src\\data\\HousingDB_post2010.csv')


#----------------------------------------------------------#
'''
CLEAN community_district_df AND CONVERT TO GEODATAFRAME:
'''
# Set all columns except 'the_geom' as numeric:
for col in community_district_df.columns:
    if col != 'the_geom':
        community_district_df[col] = pd.to_numeric(community_district_df[col], errors='coerce')

# Create borough column:
community_district_df['borough'] = community_district_df['commntydst'].apply(
    lambda x: 'Bronx' if str(x).startswith('1') else
              'Brooklyn' if str(x).startswith('2') else
              'Manhattan' if str(x).startswith('3') else
              'Queens' if str(x).startswith('4') else
              'Staten Island' if str(x).startswith('5') else
              'Unknown'  # If unknown
)

# Create totals column:
community_district_df['Total'] = community_district_df[['comp2010', 'comp2011', 'comp2012', 'comp2013',
                                                         'comp2014', 'comp2015', 'comp2016', 'comp2017',
                                                         'comp2018', 'comp2019', 'comp2020', 'comp2021',
                                                         'comp2022', 'comp2023']].sum(axis=1)

#----------------------------------------------------------#
# Rename values in project_df['Job_Status']:
project_df['Job_Status'] = project_df['Job_Status'].apply(lambda x: x[3:].strip())

# Convert to numeric columns
project_df['CompltYear'] = pd.to_numeric(project_df['CompltYear'], errors= 'coerce')
project_df['PermitYear'] = pd.to_numeric(project_df['PermitYear'], errors= 'coerce')

# Convert to datetime:
project_df['DateFiled'] = pd.to_datetime(project_df['DateFiled'])
project_df['DatePermit'] = pd.to_datetime(project_df['DatePermit'])
project_df['DateComplt'] = pd.to_datetime(project_df['DateComplt'])

# Calculate number of days between permit issuance and project completion:
project_df['Days_Perm_Comp'] = (project_df['DateComplt'] - project_df['DatePermit']).dt.days

# Calculate number of days between date project was filed and date of permit issuance:
project_df['Days_File_Permit'] = (project_df['DatePermit'] - project_df['DateFiled']).dt.days

#----------------------------------------------------------#
# SAVE DATA TO DATA FOLDER:

if community_district_df is not None:
    community_district_df.to_csv(os.path.join('src', 'data', 'community_district_data.csv'))
    print("community_district_df saved successfully as CSV.")
else:
    print("Failed to save community_district_df.")

if project_df is not None:
    project_df.to_csv(os.path.join('src', 'data', 'project_level_data.csv'), index=False)
    print("Project-level data saved successfully as CSV.")
else:
    print("Failed to save project-level data as CSV.")

