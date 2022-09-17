# imports
import pickle5 as pickle
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression


# Loading model
model = pickle.load(open('secondmodel.pkl','rb'))

# Loading features
feature_dict = pickle.load(open('features.pkl','rb'))

# Caching the model for faster loading
# @st.cache

# Application Body
st.title('Salary Prediction')
st.image('https://cdn.pixabay.com/photo/2018/10/03/11/31/wallet-3721156_1280.png', width=200)
st.header('Provide your inputs for predicting Salary:')

# selections
cols = list(feature_dict.keys())
jobTitle = st.selectbox('Select Job Title:', list(feature_dict[cols[0]].keys()))
country = st.selectbox('Select Country:', list(feature_dict[cols[1]].keys()))
position = st.selectbox('Select Seniority:', list(feature_dict[cols[2]].keys()))
yearExp = st.number_input('Enter Total Experience (Years):', min_value=1, max_value=25, value=1)
contract = st.selectbox('Select Job Type', list(feature_dict[cols[4]].keys()))
eligibility = st.selectbox('Select Seniority:', list(feature_dict[cols[5]].keys()))
skills = st.multiselect('Select one or more skills:', cols[6:])


# Prediction & output
if st.button('Predict Salary'):
  dataset = [
    feature_dict[cols[0]][jobTitle],
    feature_dict[cols[1]][country],
    feature_dict[cols[2]][position],
    yearExp,
    feature_dict[cols[4]][contract],
    feature_dict[cols[5]][eligibility]
    ]
  for i in cols[6:]:
    if feature_dict[i] in skills:
      dataset.append(1)
    else:
      dataset.append(0)
  df = pd.DataFrame(dataset)
  salary = model.predict(df.T).flatten().tolist()
  st.success(f'Expected Salary between **\${salary[0]:,.0f}** and **\${salary[1]:,.0f}** annually.')
