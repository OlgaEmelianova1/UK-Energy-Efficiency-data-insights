import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from PIL import Image
from bokeh.plotting import figure
from itertools import count
from turtle import color

st.title("UK National Energy Efficiency Data Framework. Insights.")


with st.sidebar:
    st.title("SUMMARY")

    st.write("National Energy Efficiency Data-Framework (NEED) is a potentially valuable resource for researchers looking at energy efficiency and energy consumption in households. This Dashboard aims to complement the NEED data with a crucial findings about photovolaic panels installation, natural gas matters and other insights.")
    st.write('')
    st.write("Solar power represented a very small part of electricity production in the United Kingdom until the 2010s when it increased rapidly, thanks to feed-in tariff (FIT) subsidies and the falling cost of photovoltaic (PV) panels.")
    st.write('')
    st.write("The 2021-2022* Global energy crisis definitly accelerates the switch on the renewables. Will this transition which was already boosted by the Paris Agreement** in 2015 be pushed even faster by the global consequences of the Russian invasion on Ukraine?..")
    st.write('')
    image = Image.open('favpng_energy-transition-renewable-energy-energy-development-wind-power.png')
    st.image(image)
    st.write('')
    st.subheader("Dashboard made by:")
    col1, col2 = st.columns(2)

    with col1:
        image1 = Image.open('github_logo.png')
        st.image(image1)
    with col2:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('[Olga Emelianova](https://github.com/OlgaEmelianova1/UK-Energy-Efficiency-data-insights/projects?type=beta)')
    st.write('')
    st.caption("*The 2021–2022 global energy crisis is the most recent in a series of cyclical energy shortages experienced over the last fifty years. It is more acutely affecting countries such as the United Kingdom and China, among others.")
    st.caption("**The Paris Agreement, often referred to as the Paris Accords or the Paris Climate Accords, is an international treaty on climate change, adopted in 2015. It covers climate change mitigation, adaptation, and finance.")


st.write('[Access to the Data source](https://data.gov.uk/dataset/7390402c-e7ce-4e2f-bb08-d8d65f852f47/national-energy-efficiency-data-framework-need-anonymised-datasets/datafile/c66720fa-5c7e-48e1-bf95-4a4d1dccaecc/preview)')

# Read Data
data = "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/857035/anon_set_50k_2019.csv"
# Create a DataFrame
df = pd.read_csv(data, delimiter = ',')
df = df.fillna(0)
# Create some new variables 
df['AVG_Econs'] = df[['Econs2017', 'Econs2016', 'Econs2015', 'Econs2014', 'Econs2013',
                      'Econs2012', 'Econs2011', 'Econs2010', 'Econs2009', 'Econs2008', 
                      'Econs2007', 'Econs2006', 'Econs2005']].mean(axis=1)

df['AVG_Gcons'] = df[['Gcons2017', 'Gcons2016', 'Gcons2015', 'Gcons2014', 'Gcons2013',
       'Gcons2012', 'Gcons2011', 'Gcons2010', 'Gcons2009', 'Gcons2008',
       'Gcons2007', 'Gcons2006', 'Gcons2005']].mean(axis=1)

#Replace the property age code by a real denomination

df['PROP_AGE_FINAL'] = df['PROP_AGE_FINAL'].replace({'101': 'before 1930', '102': '1930-1949', '103': '1950-1966', 
                                                     '104': '1967-1982', '105': '1983-1995', '106': '1996 onwards'})

# Transfrom the 'band' colomn to numeric
def map_values(row, values_dict):
    return values_dict[row]

values_dict = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5,
                                 'F': 6, 'G': 7, 'H': 8, 'I': 9}

df['band_num'] = df['band'].apply(map_values, args = (values_dict,))


#Transform it to dummy variable : A, B = 1; C and higher - 0

df["EE_BAND"] = np.where(
   (df.band_num > 2), 
   "1", 
   "0"
)
df['EE_BAND'] = pd.to_numeric(df['EE_BAND'])


# Create a new dataframe that have all condumption data in one column 
df["id"] = df.index + 1

all_cons = df[['id', 'Gcons2017', 'Gcons2016',
       'Gcons2015', 'Gcons2014', 'Gcons2013', 'Gcons2012', 'Gcons2011',
       'Gcons2010', 'Gcons2009', 'Gcons2008', 'Gcons2007', 'Gcons2006',
       'Gcons2005', 'Econs2017', 'Econs2016', 'Econs2015', 'Econs2014',
       'Econs2013', 'Econs2012', 'Econs2011', 'Econs2010', 'Econs2009',
       'Econs2008', 'Econs2007', 'Econs2006', 'Econs2005']]

all_cons_dep = pd.melt(all_cons, id_vars=['id'], value_vars=['Gcons2017', 'Gcons2016',
       'Gcons2015', 'Gcons2014', 'Gcons2013', 'Gcons2012', 'Gcons2011',
       'Gcons2010', 'Gcons2009', 'Gcons2008', 'Gcons2007', 'Gcons2006',
       'Gcons2005', 'Econs2017', 'Econs2016', 'Econs2015', 'Econs2014',
       'Econs2013', 'Econs2012', 'Econs2011', 'Econs2010', 'Econs2009',
       'Econs2008', 'Econs2007', 'Econs2006', 'Econs2005'])

all_cons_dep['energy_source'] = all_cons_dep['variable'].str[:1]
all_cons_dep['year'] = all_cons_dep['variable'].str[-4:]

all_cons_dep.rename(columns = {'value':'consumption, kw/h'}, inplace = True)
all_cons_dep = all_cons_dep[['id', 'consumption, kw/h', 'energy_source', 'year']]
all_cons_sort = all_cons_dep.sort_values(by=['year'])

# Create a new Dataframe that include the code, region, longutide and latitude to create the geographical maps

geo = {
    'GOR_EW':["E12000001", "E12000002", "E12000003", "E12000004", "E12000005", "E12000006", "E12000007", "E12000008", "E12000009", "W99999999"],
   'region':["North East", "North West", "Yorkshire and The Humber", "East Midlands", "West Midlands", "East of England", "London", "South East", "South West", "Wales"],
    'lat':[55.041, 53.6221, 53.9062, 53.0452, 52.4751, 52.1911, 51.5072, 51.1781, 50.7772, 52.1307],
    'long':[-1.651, -2.5945, -1.0334, -0.3982, -1.8298, 0.1927, -0.1276, -0.5596, -3.9995, -3.7837]
}

geo_data = pd.DataFrame(geo)

df = df.merge(geo_data, on='GOR_EW', how='left')
df = df.reset_index(drop=True)


# get the additional data for the gas bill amount


bill_data = pd.read_excel(io="average_annual_domestic_gas_bills.xlsx", 
                          sheet_name=4,
                          header=15)

# get the additional data for the gas import origine


import_data = pd.read_excel(io="uk_gas_import.xlsx", 
                          sheet_name="Annual (GWh)",
                          header=4)

import_data=import_data.rename(columns={'Bacton to Zeebrugge Interconnector':'Bacton to Zeebrugge Interconnector pipeline(Belgium)',
                                        'Balgzand to Bacton (BBL)':'Netherlands pipeline',
                                        'Total Norway pipeline': 'Norway pipeline'})

import_data=import_data[['Year', 'Bacton to Zeebrugge Interconnector pipeline(Belgium)',
       'Netherlands pipeline', 'Norway pipeline',
       'Total pipeline', 'Qatar', 'Russia', 'Trinidad & Tobago', 'USA',
       'Algeria', 'Angola', 'Australia', 'Belgium', 'Cameroon',
       'Dominican Republic', 'Egypt', 'Equatorial Guinea', 'France',
       'Netherlands', 'Nigeria', 'Norway', 'Peru', 'Yemen', 'Total LNG',
       'Total Imports']]
import_data = import_data[:-1]

# get the additional data for the gas price historic

gas_price_data = pd.read_csv("gas_prices.csv", delimiter = ',')


gas_price_data['year'] = gas_price_data['DATE'].str[-4:]
gas_price_data = gas_price_data.rename(columns={"PNGASEUUSDM": "price,£"})


# get the additional data for the PV installation campaign details


pv_data = pd.read_csv("photovoltaic_data_uk.csv", delimiter = ',')
pv_data['year'] = pv_data['period'].str[-4:]




#Show data
add_selectbox = st.selectbox(
    "Choose data to show",
    ("NEED Framework Data, cleaned & transformed", "Solar Photovoltaics deployment in the UK", "Gas domestic bill data", "Origin of the natural gas import in UK", "Natural gas price historic data")
)


if add_selectbox == "NEED Framework Data, cleaned & transformed":
    st.metric(label="Rows", value="55154")
    st.metric(label="Columns", value="44")
    st.write(df)
    if st.button("Show values look-ups"):
        st.write("IMD_band - Index of multiple deprivation (quintiles)")
        st.write("PROP_AGE_FINAL - pre-1930, 1930-1949, 1950-1966, 1967-1982, 1983-1995, 1996 onwards")
        st.write("PV_FLAG: 1 - photovoltaics, no photovoltaics")
        st.write("CWI_FLAG: 1  - Cavity wall insulation installed through a Government scheme, 0 - no")
        st.write("LI_FLAG: 1 - Loft insulation installed through a Government scheme, 0 - no")
        st.write("FLOOR_AREA_BAND: 1 - 1 to 50 m2, #2 - 51-100 m2, #3 - 101-150 m2, #4 - Over 151 m2")
        st.write("EE_BAND - 0 - A and B, 1 - C to G")
        st.write("GOR_EW - Region")
        st.write("MAIN_HEAT_FUEL - 2: Gas, 1: other")
        st.write("GconsYEAR - Annual gas consumption in kWh (2005 - 2017)")
        st.write("EconsYEAR - Annual electricity consumption in kWh (2005 - 2017)")
        st.write("GasValFlagYEAR - Flag indicating records with valid gas consumption and off gas households")
        st.write("ElectValFlagYEAR - Flag indicating record with valid electricity consumption")
    else:
        st.write("")
    
if add_selectbox == "Solar Photovoltaics deployment in the UK":
    st.write(pv_data)

if add_selectbox == "Gas domestic bill data":
    st.write(bill_data)
    
if add_selectbox == "Origin of the natural gas import in UK":
    st.write(import_data)

if add_selectbox == "Natural gas price historic data":
    st.write(gas_price_data)

#######

code = ''' all_cons = df[['id', 'Gcons2017', 'Gcons2016',
       'Gcons2015', 'Gcons2014', 'Gcons2013', 'Gcons2012', 'Gcons2011',
       'Gcons2010', 'Gcons2009', 'Gcons2008', 'Gcons2007', 'Gcons2006',
       'Gcons2005', 'Econs2017', 'Econs2016', 'Econs2015', 'Econs2014',
       'Econs2013', 'Econs2012', 'Econs2011', 'Econs2010', 'Econs2009',
       'Econs2008', 'Econs2007', 'Econs2006', 'Econs2005']]

all_cons_dep = pd.melt(all_cons, id_vars=['id'], value_vars=['Gcons2017', 'Gcons2016',
       'Gcons2015', 'Gcons2014', 'Gcons2013', 'Gcons2012', 'Gcons2011',
       'Gcons2010', 'Gcons2009', 'Gcons2008', 'Gcons2007', 'Gcons2006',
       'Gcons2005', 'Econs2017', 'Econs2016', 'Econs2015', 'Econs2014',
       'Econs2013', 'Econs2012', 'Econs2011', 'Econs2010', 'Econs2009',
       'Econs2008', 'Econs2007', 'Econs2006', 'Econs2005'])

all_cons_dep['energy_source'] = all_cons_dep['variable'].str[:1]
all_cons_dep['year'] = all_cons_dep['variable'].str[-4:]

all_cons_dep.rename(columns = {'value':'consumption, kw/h'}, inplace = True)
all_cons_dep = all_cons_dep[['id', 'consumption, kw/h', 'energy_source', 'year']]
all_cons_sort = all_cons_dep.sort_values(by=['year'])

sns.set(rc={'figure.figsize':(15,10)})
sns.lineplot(data=all_cons_sort, x="year", y="consumption, kw/h", hue="energy_source") '''


with st.expander("Explore the domestic consumption data"):
    st.image("consumption_graph.png")
    if st.button("Show code"):
        st.code(code, language='python')
    else:
        st.write("")


with st.expander("Energy Efficiency Band"):
    fig = px.bar(
    df, 
    x='band', 
    color='band',
    color_discrete_map={
        'A': "darkgreen",
        'B': "green",
        'C': "lightgreen",
        'D': "greenyellow",
        'E': "yellow", 
        'F': "orange",
        'G': "orangered",
        'H': "red",
        'I': "darkred"
        }
    )
    st.plotly_chart(fig)

with st.expander("Natural gas UK import origine by year"):
    fig = px.bar(import_data, x="Year", y=['Bacton to Zeebrugge Interconnector pipeline(Belgium)',
            'Netherlands pipeline', 'Norway pipeline',
            'Qatar', 'Russia', 'Trinidad & Tobago', 'USA',
            'Algeria', 'Angola', 'Australia', 'Belgium', 'Cameroon',
            'Dominican Republic', 'Egypt', 'Equatorial Guinea', 'France',
            'Netherlands', 'Nigeria', 'Norway', 'Peru', 'Yemen'], title="Import by year")
    st.plotly_chart(fig)



with st.expander("Natural gas pricing statistics"):
    col1, col2 = st.columns(2)

    with col1:
        x = gas_price_data['year']
        y = gas_price_data['price,£']
        p = figure(
            title='Natural gas prices historical data',
            x_axis_label='x',
            y_axis_label='y')
        p.line(x, y, legend_label='Price,£ per barrel', line_width=2)
        st.bokeh_chart(p, use_container_width=True)

        st.metric(label="November 2021 natural gas price, £ per barrel", value="27.201387", delta="25.9 £")
   
    with col2:
        x = bill_data['Year']
        y = bill_data['Direct debit: Bill (Pounds)']
        p = figure(
            title='Average annual domestic gas bills in UK',
            x_axis_label='x',
            y_axis_label='y')
        p.line(x, y, legend_label='Bill,£', line_width=2)
        st.bokeh_chart(p, use_container_width=True)

        st.metric(label="Average annual domestic gas bill in UK in 2019 (Pounds)", value="643", delta="362 £")


with st.expander("Photovoltaic deployment"):
    select_box = st.selectbox(
        "Choose data to show",
        ("Cumulative capacity(mw)", "Cumulative count")
        )

    if select_box == "Cumulative capacity(mw)":
        fig = px.bar(pv_data, x="year", y="cumulative capacity(mw)")
        st.plotly_chart(fig)
    if select_box == "Cumulative count":
        fig = px.bar(pv_data, x="year", y="cumulative count")
        st.plotly_chart(fig)

with st.expander("Average electricity consumption based on NEED attributes"):
    select_box = st.selectbox(
        "Choose the attribute",
        ("By Region", "Photovoltaic installed, yes/non", "Loft insulation installed through a Government scheme, yes/non", "Cavity wall insulation installed through a Government scheme, yes/non", "Rating by the Index of Multiple deprivation (1 - not deprived, 5 - least deprived)")
        )
    
    if select_box == "By Region":
        fig = px.bar(df, x="region", y="AVG_Econs")
        st.plotly_chart(fig)

    if select_box == "Photovoltaic installed, yes/non":
        fig = px.bar(df, x="PV_FLAG", y="AVG_Econs")
        st.plotly_chart(fig)

    if select_box == "Loft insulation installed through a Government scheme, yes/non":
        fig = px.bar(df, x="LI_FLAG", y="AVG_Econs")
        st.plotly_chart(fig)

    if select_box == "Cavity wall insulation installed through a Government scheme, yes/non":
        fig = px.bar(df, x="CWI_FLAG", y="AVG_Econs")
        st.plotly_chart(fig)

    if select_box == "Rating by the Index of Multiple deprivation (1 - not deprived, 5 - least deprived)":
        fig = px.bar(df, x="IMD_band", y="AVG_Econs")
        st.plotly_chart(fig)

#Correlation matrix

    corr_df = df[['PROP_AGE_FINAL', 'FLOOR_AREA_BAND', 
            'LI_FLAG', 'CWI_FLAG', 'PV_FLAG', 'IMD_band',
            'AVG_Econs', 'AVG_Gcons', 'EE_BAND', 'MAIN_HEAT_FUEL']]

    corrMatrix = corr_df.corr()

with st.expander("Correlation Matrix"):
    
    fig = px.imshow(corrMatrix, text_auto=True)
    st.plotly_chart(fig)

        