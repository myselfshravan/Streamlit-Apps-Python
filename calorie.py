import streamlit as st
import pandas as pd
import numpy as np

st.title('Data of calories in food')
data = pd.read_json('https://raw.githubusercontent.com/terrenjpeterson/caloriecounter/master/src/data/foods.json')

st.subheader('List of Restaurants')
rest = st.radio('Select a restaurant', data['restaurant'])
st.write(rest)

for i in range(0, len(data)):
    if data['restaurant'][i] == rest:
        dataframe = pd.DataFrame(data['foodItems'][i])
        st.write(dataframe)

st.subheader('List of food items')
food = st.selectbox('Select a food item', dataframe)
