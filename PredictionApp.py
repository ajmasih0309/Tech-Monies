# imports
import pickle5 as pickle
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
# from forex_python.converter import CurrencyRates
import requests
from st_on_hover_tabs import on_hover_tabs
st.set_page_config(layout="wide")

# Loading model
model = pickle.load(open('secondmodel.pkl','rb'))

# Loading features
feature_dict = pickle.load(open('features.pkl','rb'))

# Loading scaler
scalerX = pickle.load(open('scalerX.pkl','rb'))
scalerY = pickle.load(open('scalerY.pkl','rb'))

# Exchange Rate


# Currency Convertor
class RealTimeCurrencyConverter():
  def __init__(self,url):
    self.data= requests.get(url).json()
    self.currencies = self.data['rates']

  def convert(self, from_currency, to_currency, amount): 
    initial_amount = amount 
    #first convert it into USD if it is not in USD.
    # because our base currency is USD
    if from_currency != 'USD' : 
      amount = amount / self.currencies[from_currency] 
  
    # limiting the precision to 4 decimal places 
    amount = round(amount * self.currencies[to_currency], 4) 
    return amount

url = 'https://api.exchangerate-api.com/v4/latest/USD'
converter = RealTimeCurrencyConverter(url)

# loading css
# st.markdown('<style>' + open('styles.css').read() + '</style>', unsafe_allow_html=True)

# Caching the model for faster loading
# @st.cache


# sidebar
with st.sidebar:
        tabs = on_hover_tabs(tabName=['Home', 'Salary Prediction', 'Survey', 'Contributors'], 
                            iconName=['home', 'money', 'dashboard', 'groups'], default_choice=0)

# Application Body
# Overview
if tabs == 'Home':
  st.title('Salary Prediction')
  st.subheader('About')
  st.write("""This is a Salary Prediction Application.
  It gives you expected salary that can be asked from recruiter/company based on Country, Total Experience, Highest Qualification and few more factors. """)
  st.warning('NOTE: This Application will only give you a possible salary range. In reality the salary can vary because of external factors which are not considered here.')
  st.subheader("How To Use The Application")
  st.write("""
        1. Input Information by using dropdown list and +/- buttons for experience.
        2. Once all the Information is entered click on Predict Salary.
        3. You will be returned the predicted value of Salary.
        4. If you want to make a new prediction repeat step 1 & 2.
        """)
  st.subheader('Help Us Improve')
  st.info("""
        Kindly participate in survey & help us improve the model for Salary Prediction.
        """)

# Model
if tabs == 'Salary Prediction':
  # st.image('https://cdn.pixabay.com/photo/2018/10/03/11/31/wallet-3721156_1280.png', width=200)
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
  currency_code = ['INR', 'NGN', 'EUR', 'USD']
  currency_sign = ['₹', '₦', '￡', '\$']
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
    min_Salary = converter.convert('USD', cc, salary[0])
    max_Salary = converter.convert('USD', cc, salary[1])
    st.success(f'Expected Salary between **{cs}{salary[0]:,.0f}** and **{cs}{salary[1]:,.0f}** annually.')

# Survey
if tabs == 'Survey':    
  st.text('Can you help us improve in salary prediction?')
  if st.button('Yes, I will'):
    # User Survey
    st.components.v1.iframe("https://docs.google.com/forms/d/e/1FAIpQLSdUwljNwSdey09TQO38Bq3VF9DwngNjvTNMJDsd2T1abRbXmw/viewform?embedded=true"
                      , width=640, height=2543, scrolling=False)

# Contributors
elif tabs == 'Contributors':
        st.title('Contributors')
        st.text("""
        This app was developed by:
        """)
        st.write('- Abhishek John Masih (https://github.com/ajmasih0309)')
        st.write('- Victor Oguche (https://github.com/RoyalVee)')
        st.write('- Opeyemi Sereki (https://github.com/chocolatebunny-0)')
        st.write('- Life Popoola (https://github.com/lifepopkay)')
        st.write('- Ovie Iboyitie (https://github.com/OvieIboyitie)')
        st.info('This Application was developed in #DSRoom challenge under the mentorship of Samson Afolabi (https://twitter.com/samsonafo)')
