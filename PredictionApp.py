# imports
import pickle5 as pickle
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from forex_python.converter import CurrencyRates

# Loading model
model = pickle.load(open('secondmodel.pkl','rb'))

# Loading features
feature_dict = pickle.load(open('features.pkl','rb'))

# Loading scaler
scalerX = pickle.load(open('scalerX.pkl','rb'))
scalerY = pickle.load(open('scalerY.pkl','rb'))

# Caching the model for faster loading
# @st.cache

# Application Body
st.title('Salary Prediction')
st.image('https://cdn.pixabay.com/photo/2018/10/03/11/31/wallet-3721156_1280.png', width=200)
st.header('Provide your inputs for predicting Salary:')

# selections
cols = list(feature_dict.keys())
jobTitle = st.selectbox('Select Job Title', list(feature_dict[cols[0]].keys()))
country = st.selectbox('Select Country', list(feature_dict[cols[1]].keys()))
position = st.selectbox('Select Seniority', list(feature_dict[cols[2]].keys()))
yearExp = st.number_input('Enter Total Experience (Years):', min_value=1, max_value=25, value=1)
contract = st.selectbox('Select Job Type', list(feature_dict[cols[4]].keys()))
eligibility = st.selectbox('Select highest education', list(feature_dict[cols[5]].keys()))
skills = st.multiselect('Select one or more skills', cols[6:])

# Salary conversion
country_index = feature_dict[cols[1]][country]
currency_code = ['INR', 'USD', 'EUR', 'USD'] # 'NGN'
currency_sign = ['₹', '\$', '￡', '\$'] #  '₦'
cc = currency_code[country_index]
cs = currency_sign[country_index]

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
  df = df.T.values
  scaledDF = scalerX.transform(df)
  prediction = model.predict(scaledDF)
  prediction = scalerY.inverse_transform(prediction)
  salary = prediction.flatten().tolist()
  min_Salary = CurrencyRates().convert('USD', cc, salary[0])
  max_Salary = CurrencyRates().convert('USD', cc, salary[1])
  st.success(f'Expected Salary between **{cs}{salary[0]:,.0f}** and **{cs}{salary[1]:,.0f}** annually.')
  
st.text('Can you help us improve in salary prediction?')
if st.button('Yes, I will'):
  # User Survey
  st.components.v1.iframe("https://docs.google.com/forms/d/e/1FAIpQLSdUwljNwSdey09TQO38Bq3VF9DwngNjvTNMJDsd2T1abRbXmw/viewform?embedded=true"
                      , width=640, height=2543, scrolling=False)
