import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import plotly.express as px
import time

st.title('A Streamlit-based ISS Tracker')

def get_iss_location():
    response = requests.get('http://api.open-notify.org/iss-now.json')
    data = response.json()

    latitude = float(data['iss_position']['latitude'])
    longitude = float(data['iss_position']['longitude'])
    timestamp = int(data['timestamp'])

    current_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    return latitude, longitude, current_time

path = []

for i in range(10):
    latitude, longitude, current_time = get_iss_location()
    path.append((latitude, longitude))
    time.sleep(60)

st.write(f'Current location of the ISS:')
st.write(f'Latitude: {latitude}')
st.write(f'Longitude: {longitude}')
st.write(f'Time: {current_time}')

df = pd.DataFrame(path, columns=['latitude', 'longitude'])

fig = px.scatter_geo(df, lat='latitude', lon='longitude')
st.plotly_chart(fig)

response = requests.get('http://api.open-notify.org/astros.json')
data = response.json()
people_in_space = data['number']
people_in_space_names = [person['name'] for person in data['people']]
st.write(f'There are currently {people_in_space} people aboard the International Space Station:')
for name in people_in_space_names:
    st.write(name)
