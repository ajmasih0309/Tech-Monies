# imports
import pickle5 as pickle
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression


# Loading model
model = pickle.load(open('firstbasicmodel.pkl','rb'))

# Loading features
feature_dict = pickle.load(open('features.pkl','rb'))

# Caching the model for faster loading
# @st.cache

# Application Body
st.title('Salary Prediction')
st.image('https://cdn.pixabay.com/photo/2018/10/03/11/31/wallet-3721156_1280.png', width=200)
st.header('Provide your inputs for predicting Salary:')

# selections
jobTitle = st.selectbox('Select Job Title:', list(feature_dict['title scraped for'].keys()))
country = st.selectbox('Select Country:', list(feature_dict['Country'].keys()))
position = st.selectbox('Select Seniority:', list(feature_dict['Position'].keys()))
yearExp = st.number_input('Enter Total Experience (Years):', min_value=1, max_value=25, value=1)
contract = st.selectbox('Select Job Type', list(feature_dict['contract_type'].keys()))
eligibility = st.selectbox('Select Seniority:', list(feature_dict['eligibility'].keys()))

# Prediction & output
if st.button('Predict Salary'):
  dataset = [
    feature_dict['title scraped for'][jobTitle],
    feature_dict['Country'][country],
    feature_dict['Position'][position],
    yearExp,
    feature_dict['contract_type'][contract],
    feature_dict['eligibility'][eligibility]
    ]
  df = pd.DataFrame(dataset)
  salary = model.predict(df.T).flatten().tolist()
  st.success(f'Expected Salary between **\${salary[0]:,.0f}** and **\${salary[1]:,.0f}** annually.')