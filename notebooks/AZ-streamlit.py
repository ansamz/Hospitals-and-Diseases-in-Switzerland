# Import needed packages
import streamlit as st
from plotly.subplots import make_subplots
from urllib.request import urlopen
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy
import pycountry #conda install -c conda-forge pycountry
from PIL import Image

# Add title and header
#page configuration
st.set_page_config(page_title="Hospitals and Diseases analysis", # page title, displayed on the window/tab bar
        		   page_icon="pill", # favicon: icon that shows on the window/tab bar (tip: you can use emojis)
                   layout="wide", # use full width of the page
                   menu_items={
                       'About': "Exploration of the infection, hospital and birth rates across Switzerland."
                   })

st.markdown("<h1 style='text-align: center; color: red;'>Hospitals in Switzerland</h1>", unsafe_allow_html=True)

# Load data and add it to cache
@st.cache
def load_dataframe(path):
    df = pd.read_csv(path, skiprows=rows_to_skip)
    return df

@st.cache
def load_jsonfile(path):
    with open(path) as response:
        regions = json.load(response)
    return regions


#Read Data
hospitals_total_lonlat = load_dataframe(path='/home/ansam/Documents/ansam-zedan/medico streamlit/data/hospitals_total_lonlat.csv')

#data processing
hospitals_total_lonlat = hospitals_total_lonlat.rename(columns={'Number_of_operating_rooms': 'Operating Rooms', 'Number_of_delivery_rooms': 'Delivery Rooms', 'Dia': 'Dialysis'})


st.header("Exploring hospitals data in Switzerland (not title just trying)")
st.subheader("hospitals services(trying)")

servs = ['Operating Rooms', 'Delivery Rooms', 'MRI', 'CT', 'PET', 'Dialysis', 'Physicians',
         'physicians in training', 'Nursing staff', 'Other medical personnel', 'Total staff']
show_labels = st.radio(label='Choose type of Service you are looking for:', options= servs)


fig1 = px.scatter_mapbox(hospitals_total_lonlat, lat='lat', lon='lng', color=show_labels, size=show_labels, hover_data=['canton_name', 'hospital', 'Hospital_type'],
                          zoom=7.5, height=700
                        )
fig1.update_layout(mapbox_style="open-street-map")
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig1)
