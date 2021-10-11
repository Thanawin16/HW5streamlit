# -*- coding: utf-8 -*-
# Copyright 2018-2019 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example of showing geographic data."""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk


# SETTING PAGE CONFIG TO WIDE MODE

st.set_page_config(layout="wide")

st.text("By Thanawin Wanna 6130813621")

##################################################################################
###########################################################################################

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns(2)


with row1_1:
    st.header('This website shows number of traffic users from the beginning and terminal point.')
    st.write("use the website by selecting your travelling date and time")

with row1_2:
    selected_date = st.selectbox("Choose your travelling date",("January 1st, 2019", "January 2nd, 2019","January 3rd, 2019","January 4th, 2019","January 5th, 2019"))
    selected_time = st.slider("Time Selection", 0, 23)


# LOADING DATA
DATE_TIME = "date/time"
DATA_DAY1 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190101.csv")
DATA_DAY2 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190102.csv")
DATA_DAY3= ("https://raw.githubusercontent.com/Maplub/odsample/master/20190103.csv")
DATA_DAY4 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190104.csv")
DATA_DAY5 = ("https://raw.githubusercontent.com/Maplub/odsample/master/20190105.csv")

#SELECT DATA ACCORDING TO selected_date
if selected_date == "January 1st, 2019" :
  DATA_URL = DATA_DAY1
elif selected_date == "January 2nd, 2019" :
  DATA_URL = DATA_DAY2
elif selected_date == "January 3rd, 2019" :
  DATA_URL = DATA_DAY3
elif selected_date == "January 4th, 2019" :
  DATA_URL = DATA_DAY4
elif selected_date == "January 5th, 2019" :
  DATA_URL = DATA_DAY5

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data = data[['timestart','latstartl','lonstartl']].copy()
    data = data.rename(columns = {'timestart': 'Date/Time', 'latstartl': 'Lat', 'lonstartl': 'Lon'}, inplace = False)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])
    return data


data = load_data(100000)

##################################################################################
##################################################################################
# CREATING FUNCTION FOR MAPS

def map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))
    
##################################################################################
##################################################################################
# FILTERING DATA BY HOUR SELECTED
data = data[(data[DATE_TIME].dt.hour == selected_time) & (data[DATE_TIME].dt.year == 2019)]


# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS


# SETTING THE ZOOM LOCATIONS FOR THE AIRPORTS
zoom_level = 11
#midpoint1 = (np.average(data1["lat"]), np.average(data1["lon"]))
#midpoint2 = (np.average(data2["lat"]), np.average(data2["lon"]))
midpoint = [13.736717, 100.523186]

map(data, midpoint[0], midpoint[1], zoom_level)
st.write("Above histogram shows number of traffic users at selected time")


# FILTERING DATA FOR THE HISTOGRAM
filtered = data[
    (data[DATE_TIME].dt.hour >= selected_time) & (data[DATE_TIME].dt.hour < (selected_time + 1))
    ]

hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0, 60))[0]

chart_data = pd.DataFrame({"minute": range(60), "travelling started": hist})

# LAYING OUT THE HISTOGRAM SECTION
st.write("")
st.altair_chart(alt.Chart(chart_data)
          .mark_area(
              interpolate='step-after',
          ).encode(
              x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
              y=alt.Y("travelling started:Q"),
              tooltip=['minute', 'travelling started']
          ).configure_mark(
              opacity=0.5,
              color='red'
          ), use_container_width=True)
st.write("Above histogram shows number of traffic users at each session of time" )

from PIL import Image
import urllib.request
urllib.request.urlretrieve('https://i.pinimg.com/474x/8c/40/05/8c4005377742272315e792545a9c93df.jpg', "sample.png")
img = Image.open("sample.png")
st.image(img,use_column_width=True)
