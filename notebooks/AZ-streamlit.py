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
import statsmodels.api as sm
import matplotlib.ticker


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
lon_lat_quality_df_map = load_dataframe(path='data/lon_lat_quality_df2.csv')
most_common_disease_canton = load_dataframe(path='data/most_common_disease_canton.csv')
most_common_disease_canton_wo = load_dataframe(path='data/most_common_disease_canton_wo.csv')
disease_pop_cantn = load_dataframe(path='data/disease_pop_canton.csv')
text_files_data = load_dataframe(path='data/text_files_data.csv')

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
disease_group_lst = ['Cardiac diseases',
                        'Diseases of the nervous system, cerebrovascular accident (stroke)',
                        'Geriatric Medicine',
                        'Lung diseases',
                        'Diseases of the abdominal organs',
                        'Vascular Diseases',
                        'Gynecology and obstetrics',
                        'Diseases of the urinary tract and male genitalia',
                        'Diseases of the bones, joints, connective tissues',
                        'Complex conditions',
                        'Skin disorders',
                        'Highly specialized medicine',
                        'Palliative Medicine',
                        ]

#colors

color_discrete_map = {'Cardiac diseases':'rgb(16,78,139)',
                          'Diseases of the abdominal organs':'rgb(154,50,205)',
                          'Gynecology and obstetrics':'rgb(151,255,255)',
                          'Diseases of the bones, joints, connective tissues':'rgb(55,165,172)'
                          }

#####################
##Text files fataframe processing
####################
text_files_data['year'] = text_files_data['year'].astype(int)

urinary = text_files_data[text_files_data['disease_group'] == 'Diseases of the urinary tract and male genitalia']
bone = text_files_data[text_files_data['disease_group'] == 'Diseases of the bones, joints, connective tissues']
specialized_medicine = text_files_data[text_files_data['disease_group'] == 'Highly specialized medicine']
cardiac = text_files_data[text_files_data['disease_group'] == 'cardiac']
nervous = text_files_data[text_files_data['disease_group'] == 'Nervous system, cerebrovascular accident (stroke)']
lung = text_files_data[text_files_data['disease_group'] == 'Lung diseases']
gynecology = text_files_data[text_files_data['disease_group'] == 'Gynecology and obstetrics']
abdominal = text_files_data[text_files_data['disease_group'] == 'Abdominal organs disease']
vascular = text_files_data[text_files_data['disease_group'] == 'Vascular Diseases']
skin = text_files_data[text_files_data['disease_group'] == 'Skin disorders']
geriatric = text_files_data[text_files_data['disease_group'] == 'Geriatric Medicine']
palliative = text_files_data[text_files_data['disease_group'] == 'Palliative Medicine']

urinary_y = urinary.groupby(by='year').sum().reset_index()
bone_y = bone.groupby(by='year').sum().reset_index()
specialized_medicine_y = specialized_medicine.groupby(by='year').sum().reset_index()
cardiac_y = cardiac.groupby(by='year').sum().reset_index()
nervous_y = nervous.groupby(by='year').sum().reset_index()
lung_y = lung.groupby(by='year').sum().reset_index()
gynecology_y = gynecology.groupby(by='year').sum().reset_index()
abdominal_y = abdominal.groupby(by='year').sum().reset_index()
vascular_y = vascular.groupby(by='year').sum().reset_index()
skin_y = skin.groupby(by='year').sum().reset_index()
geriatric_y = geriatric.groupby(by='year').sum().reset_index()
palliative_y = palliative.groupby(by='year').sum().reset_index()

def linear_reg(df):
    y = df['casesch']
    X = sm.add_constant(df['year'])

    linear_1 = sm.OLS(y, X).fit()

    parm1, parm2 = linear_1.params

    return parm1, parm2

##########################
#Graphs
##########################


st.subheader("Number of patients 2014-2019 per hospital")

fig5 = px.scatter_mapbox(
    lon_lat_quality_df_map,
    color="normalized_by_population",
    size='normalized_by_population',
    lat='lat', lon='lng',
    center={"lat": 46.8, "lon": 8.3},
    hover_data=['hospital', 'number_of_cases', 'city', 'canton_name'],
    mapbox_style="open-street-map",
    zoom=6.3,
    opacity=0.8,
    width=1500,
    height=750,
    labels={"canton_name":"Canton",
            "hospital": "Hospital",
            "city": "City",
            "number_of_cases":"Number of patients"},
    title="<b>Number of patients 2014-2019 per hospital</b>",
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


st.subheader("Most represented disease groups according to canton")

fig4 = px.histogram(most_common_disease_canton, x="canton_name", y="normalized_by_population",
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
fig4.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.635
))
fig4.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)'))
st.plotly_chart(fig4)

################################################

st.subheader("Number of patients according to disease group")

fig3 = px.histogram(most_common_disease_canton_wo, x="canton_name", y="normalized_by_population", color="disease_group",
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
fig3.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.635
))
fig3.update_layout(legend = dict(bgcolor = 'rgba(0,0,0,0)'))
st.plotly_chart(fig3)

##############################################

st.subheader("Number of patients per hospital")

col9, col10= st.columns(2)
canton9 = col9.selectbox("Choose a Canton for comparison", cantons_list)
canton10 = col10.selectbox("Choose a Second Canton for comparison", cantons_list)

lon_lat_quality_df2['normalized_by_population'] = lon_lat_quality_df2[['number_of_cases']].div(lon_lat_quality_df2.population, axis=0)
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
st.subheader("Disease distribution in cantons and forecasting future patients number")

show_labels = st.radio(label='Choose disease group:', options=disease_group_lst)
col13, col14 = st.columns(2)

df13_canton = disease_pop_cantn[disease_pop_cantn['disease_group'] == show_labels]
fig13 = px.choropleth_mapbox(df13_canton, geojson=gs, color="normalized_by_population",
                           hover_data= ['canton_name', 'disease_group', 'number_of_cases_2014_2019', 'population', 'normalized_by_population'],
                           locations="canton_name", featureidkey="properties.kan_name",
                           center={"lat": 46.818, "lon": 8.2275}, #swiss longitude and latitude
                           mapbox_style="carto-positron", zoom=7, opacity=0.8, width=950, height=750,
                           labels={"canton_name":"Canton",
                           "normalized_by_population":"Number of patients normalised"},
                           title="<b>Normalised Number patients according to disease group</b>",
                           color_continuous_scale="Viridis")
fig13.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, hoverlabel={"bgcolor":"white", "font_size":12, "font_family":"Sans"})
col13.plotly_chart(fig13)

if show_labels == 'Cardiac diseases':
    df_prediction = cardiac_y
elif show_labels == 'Diseases of the nervous system, cerebrovascular accident (stroke)':
    df_prediction = nervous_y
elif show_labels == 'Geriatric Medicine':
    df_prediction = geriatric_y
elif show_labels == 'Lung diseases':
    df_prediction = lung_y
elif show_labels == 'Diseases of the abdominal organs':
    df_prediction = abdominal_y
elif show_labels == 'Vascular Diseases':
    df_prediction = vascular_y
elif show_labels == 'Gynecology and obstetrics':
    df_prediction = gynecology_y
elif show_labels == 'Diseases of the urinary tract and male genitalia':
    df_prediction = urinary_y
elif show_labels == 'Diseases of the bones, joints, connective tissues':
    df_prediction = bone_y
elif show_labels == 'Skin disorders':
    df_prediction = skin_y
elif show_labels == 'Palliative Medicine':
    df_prediction = palliative_y
else:
    df_prediction = specialized_medicine_y

x, y = linear_reg(df_prediction)

fig14, ax = plt.subplots()
fig14 = plt.figure(figsize=(18, 10))
plt.plot(df_prediction['year'], df_prediction['casesch'], 'o')           # scatter plot showing actual data
for i in [2020, 2021, 2022, 2023, 2024, 2025]:
  pred = x + y*i
  plt.plot(i, pred, color='red', marker='o')   # regression line
plt.xlabel('year')
plt.ylabel('number of cases')
plt.title('number of disease group infections')

locator = matplotlib.ticker.MultipleLocator(2)
plt.gca().xaxis.set_major_locator(locator)
formatter = matplotlib.ticker.StrMethodFormatter("{x:.0f}")
plt.gca().xaxis.set_major_formatter(formatter)

col14.write(" ")
col14.write(" ")
col14.write(" ")
col14.write(" ")
col14.write(" ")
col14.pyplot(fig14)

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




