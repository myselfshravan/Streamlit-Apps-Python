import streamlit as st
import pandas as pd
import numpy as np

# USN = '1MS21CI049'
# dob = '2003-05-21'
USN = st.text_input("Enter your USN", key="USN")
dob = st.text_input("Enter your DOB", key="dob")
st.title('Data of Student')
link = ('https://upylba53h2.execute-api.us-east-1.amazonaws.com/sis?usn=' + USN + '&dob=' + dob)
st.write(link)

