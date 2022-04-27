# Import needed packages
import streamlit as st
from plotly.subplots import make_subplots
from urllib.request import urlopen
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
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
    df = pd.read_csv(path)
    return df

@st.cache
def load_jsonfile(path):
    with open(path) as response:
        regions = json.load(response)
    return regions


#Read Data
hospitals_total_lonlat = load_dataframe(path='data/hospitals_total_lonlat.csv')
group_disease_cantons_wo_G = load_dataframe(path= 'data/group_disease_cantons_wo_G.csv')
most_pop_disease_canton = load_dataframe(path= 'data/most_pop_disease_canton.csv')
lon_lat_quality_df = load_dataframe(path= 'data/lon_lat_quality_df.csv')
hospitals_total = load_dataframe(path= 'data/hospitals_total.csv')
canton_hospitals_pop = load_dataframe(path='data/canton_hospitals_pop.csv')
deliv_canton_2019_rooms = load_dataframe(path='data/deliv_canton_2019_rooms.csv')
cantons_hospital_serv = load_dataframe(path='data/cantons_hospital_serv.csv')

gs = load_jsonfile(path='data/georef-switzerland-kanton.geojson')

#data processing
hospitals_total_lonlat = hospitals_total_lonlat.rename(columns={'Number_of_operating_rooms': 'Operating Rooms', 'Number_of_delivery_rooms': 'Delivery Rooms', 'Dia': 'Dialysis', 'physicians in training' :'Physicians in training'})
lon_lat_quality_df2 = lon_lat_quality_df.drop(columns=['Unnamed: 0', 'lat', 'lng', 'population_proper'])

#lists of data
cantons_list = ['Thurgau', 'Graubünden', 'Luzern', 'Bern', 'Valais',
                'Basel-Landschaft', 'Solothurn', 'Vaud', 'Schaffhausen', 'Zürich',
                'Aargau', 'Uri', 'Neuchâtel', 'Ticino', 'St. Gallen', 'Genève',
                'Glarus', 'Jura', 'Zug', 'Obwalden', 'Fribourg', 'Schwyz',
                'Appenzell Ausserrhoden', 'Appenzell Innerrhoden', 'Nidwalden', 'Basel-Stadt']

servs1 = ['Operating Rooms', 'Delivery Rooms', 'MRI', 'CT', 'PET', 'Dialysis']
servs = ['Physicians', 'Physicians in training', 'Nursing staff', 'Other medical personnel', 'Total staff']
servs_all = ['Operating Rooms', 'Delivery Rooms', 'MRI', 'CT', 'PET', 'Dialysis', 'Physicians', 'Physicians in training', 'Nursing staff', 'Other medical personnel', 'Total staff']

#colors

color_discrete_map = {'Cardiac diseases':'rgb(16,78,139)',
                          'Diseases of the abdominal organs':'rgb(154,50,205)',
                          'Gynecology and obstetrics':'rgb(151,255,255)',
                          'Diseases of the bones, joints, connective tissues':'rgb(55,165,172)'
                          }

##########################
#Graphs
##########################


st.subheader("Number of cases 2014-2019 per hospital")

fig5 = px.scatter_mapbox(
    lon_lat_quality_df,
    color="number_of_cases",
    size='number_of_cases',
    lat='lat', lon='lng',
    center={"lat": 46.8, "lon": 8.3},
    hover_data=['hospital', 'number_of_cases', 'city', 'canton_name'],
    mapbox_style="open-street-map",
    zoom=6.3,
    opacity=0.8,
    width=1600, height=600,
    labels={"canton_name":"Canton",
            "hospital": "Hospital",
            "city": "City",
            "number_of_cases":"Number of patients"},
    color_continuous_scale="Viridis"
)
fig5.update_layout(margin={"r":0,"t":35,"l":0,"b":0},
                  font={"family":"Sans",
                       "color":"maroon"},
                  hoverlabel={"bgcolor":"white",
                              "font_size":15,
                             "font_family":"Arial"},
                  title={"font_size":20,
                        "xanchor":"left", "x":0.01,
                        "yanchor":"bottom", "y":0.95}
                 )

st.plotly_chart(fig5)

col9, col10= st.columns(2)
canton9 = col9.selectbox("Choose a Canton for comparison", cantons_list)
canton10 = col10.selectbox("Choose a Second Canton for comparison", cantons_list)

col11, col12= st.columns(2)
table5 = lon_lat_quality_df2[lon_lat_quality_df2['canton_name'] == canton9]
col11.table(table5)

table6 = lon_lat_quality_df2[lon_lat_quality_df2['canton_name'] == canton10]
col12.table(table6)

######################################
st.header("Hospital distribution in Switzerland")

fig11 = px.choropleth_mapbox(canton_hospitals_pop, geojson=gs, color="Hospital numbers",
                           hover_data= ['Total', 'age 0-19', 'age 20-64', 'age 65+', 'Male', 'Female'],
                           locations="canton_name", featureidkey="properties.kan_name",
                           center={"lat": 46.818, "lon": 8.2275}, #swiss longitude and latitude
                           mapbox_style="carto-positron", zoom=7, opacity=0.8, width=1500, height=750,
                           labels={"canton_name":"Canton",
                           "Hospital numbers":"Number of hospitals per canton"},
                           title="<b>Number of hospitals per Canton</b>",
                           color_continuous_scale="Viridis")
fig11.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, hoverlabel={"bgcolor":"white", "font_size":12, "font_family":"Sans"})
st.plotly_chart(fig11)


col1, col2= st.columns(2)
canton1 = col1.selectbox("Choose a Canton", cantons_list)
canton2 = col2.selectbox("Choose a Second Canton", cantons_list)

col3, col4= st.columns(2)
table1 = canton_hospitals_pop[canton_hospitals_pop['canton_name'] == canton1]
col3.table(table1)

table2 = canton_hospitals_pop[canton_hospitals_pop['canton_name'] == canton2]
col4.table(table2)

##########################

st.subheader("Birth rate distribution according to cantons in Switzerland")
fig12 = px.choropleth_mapbox(deliv_canton_2019_rooms, geojson=gs, color="Number of deliveries",
                           hover_data= ['Number of cesarean sections', 'Number_of_operating_rooms', 'Number_of_delivery_rooms'],
                           locations="canton_name", featureidkey="properties.kan_name",
                           center={"lat": 46.818, "lon": 8.2275}, #swiss longitude and latitude
                           mapbox_style="carto-positron", zoom=7, opacity=0.8, width=1500, height=750,
                           labels={"canton_name":"Canton",
                           "Number of deliveries":"Number of births per canton"},
                           title="<b>Number of deliveries per Canton</b>",
                           color_continuous_scale="Viridis")
fig12.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, hoverlabel={"bgcolor":"white", "font_size":12, "font_family":"Sans"})
st.plotly_chart(fig12)


col5, col6= st.columns(2)
canton3 = col5.selectbox("Select a Canton", cantons_list)
canton4 = col6.selectbox("Select a Second Canton", cantons_list)

col7, col8= st.columns(2)
table3 = deliv_canton_2019_rooms[deliv_canton_2019_rooms['canton_name'] == canton3]
col7.table(table3)

table4 = deliv_canton_2019_rooms[deliv_canton_2019_rooms['canton_name'] == canton4]
col8.table(table4)


################################################

st.subheader("Most represented disease groups according to canton")

fig4 = px.histogram(most_pop_disease_canton, x="canton_name", y="number_of_cases_2014_2019",
                    color="disease_group", color_discrete_map=color_discrete_map, log_x=False, width=1800, height=1000)
fig4.update_layout(
    font_family="Courier New",
    font_color="blue",
    title_font_family="Times New Roman",
    title_font_color="red",
    legend_title_font_color="green"
)
fig4.update_layout(
    xaxis_title="Canton Name",
    yaxis_title="Number of patients in disease group 2014-2019",
    legend_title="Disease Group",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
fig4.update_xaxes(title_font_family="Arial")
fig4.update_xaxes(tickangle=50)
st.plotly_chart(fig4)

################################################

st.subheader("Number of cases according to disease group")

fig3 = px.histogram(group_disease_cantons_wo_G, x="canton_name", y="number_of_cases_2014_2019", color="disease_group",
                    color_discrete_map=color_discrete_map, log_x=False, width=1800, height=1000)
fig3.update_layout(
    font_family="Courier New",
    font_color="blue",
    title_font_family="Times New Roman",
    title_font_color="red",
    legend_title_font_color="green"
)
fig3.update_layout(
    xaxis_title="Canton Name",
    yaxis_title="Number of patients in disease group 2014-2019",
    legend_title="Disease Group",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)
fig3.update_xaxes(title_font_family="Arial")
fig3.update_xaxes(tickangle=50)
st.plotly_chart(fig3)

##############################################

########################
st.subheader("Hospitals Equipment")


show_labels = st.radio(label='Choose the type of equipment you are looking for:', options= servs1)


fig1 = px.scatter_mapbox(hospitals_total_lonlat, lat='lat', lon='lng', color=show_labels, size=show_labels, hover_data=['canton_name', 'hospital', 'Hospital_type'],
                          zoom=7.5, width=1600, height=600
                        )
fig1.update_layout(mapbox_style="open-street-map")
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig1)

#############################################

# st.subheader("Hospitals Staff")
#
# servs = ['Physicians', 'Physicians in training', 'Nursing staff', 'Other medical personnel', 'Total staff']
#
# show_labels2 = st.radio(label='Choose type of Service you are looking for:', options= servs)
#
# fig2 = px.scatter_mapbox(hospitals_total_lonlat, lat='lat', lon='lng', color=show_labels2, hover_data=['canton_name', 'hospital', 'Hospital_type'],
#                           zoom=7.5, width=1600, height=600
#                         )
# fig2.update_layout(mapbox_style="open-street-map")
# fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#
# st.plotly_chart(fig2)

st.subheader("All Hospital services across Switzerland")

cols = list(cantons_hospital_serv.columns)

service_select = st.multiselect('Select the services you are interested in:', cols)
canton_select = st.multiselect('Select the canton/s you are interested in:', cantons_list)
service_select.append('canton_name')

if service_select:
    selection_table = cantons_hospital_serv[service_select]
    cols2 = list(selection_table.columns)
    if canton_select:
        selection_table2 = pd.DataFrame(columns=cols2)
        for i in canton_select:
            entry = selection_table.loc[selection_table['canton_name'] == i]
            selection_table2 = selection_table2.append([entry])
        st.table(selection_table2)
    else:
        st.table(selection_table)
else:
    st.write("")




