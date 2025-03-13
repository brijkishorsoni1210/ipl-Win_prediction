
import streamlit as st
import pickle as pl
import pandas as pd
import time

# Load the trained model
pipe = pl.load(open('pipe.pkl', 'rb'))

# Define teams and cities
teams = ['Sunrisers Hyderabad', 'Mumbai Indians',
         'Royal Challengers Bangalore', 'Kolkata Knight Riders',
         'Kings XI Punjab', 'Chennai Super Kings',
         'Rajasthan Royals', 'Delhi Capitals']

cities = ['Hyderabad', 'Pune', 'Rajkot', 'Indore', 'Bangalore', 'Mumbai',
          'Kolkata', 'Delhi', 'Chandigarh', 'Kanpur', 'Jaipur', 'Chennai',
          'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion',
          'East London', 'Johannesburg', 'Kimberley', 'Bloemfontein',
          'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Kochi',
          'Visakhapatnam', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah',
          'Mohali', 'Bengaluru']

# Page title with animation
st.markdown("<h1 style='text-align: center; color: orange;'>🏏 IPL Win Predictor</h1>", unsafe_allow_html=True)

# Sidebar animation
with st.sidebar:
    st.image("https://media.giphy.com/media/xT9IgG50Fb7Mi0prBC/giphy.gif", use_container_width=True)
    st.header("Welcome to IPL Predictor!")
    st.markdown("<p style='text-align: justify;'>Select the teams, match details, and check the winning probabilities!</p>", unsafe_allow_html=True)

# Input fields
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('🏏 Select Batting Team', sorted(teams))
with col2:
    bowling_team = st.selectbox('🏏 Select Bowling Team', sorted(teams))

selected_city = st.selectbox('📍 Select Host City', sorted(cities))
target = st.number_input('🎯 Target Score', min_value=1)

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input('🏆 Current Score', min_value=0)
with col4:
    overs = st.number_input('⏳ Overs Completed', min_value=0.0, max_value=20.0, step=0.1)
with col5:
    wickets = st.number_input('❌ Wickets Out', min_value=0, max_value=10)

# Prediction button with animation
if st.button('🚀 Predict Probability'):
    with st.spinner('Calculating... 🏏'):
        time.sleep(2)  # Simulating processing time
    
    runs_left = target - score
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0
    
    input_df = pd.DataFrame({'batting_team': [batting_team], 'bowling_team': [bowling_team],
                             'city': [selected_city], 'runs_left': [runs_left],
                             'bowls_left': [balls_left], 'wickets_left': [wickets_left],
                             'total_runs_x': [target], 'crr': [crr], 'rrr': [rrr]})
    
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    
    # Display result with animation
    st.success("🏆 Prediction Completed!")
    st.balloons()
    
    st.markdown(f"""
        <div style='text-align: center;'>
            <h2 style='color: green;'>{batting_team} - {round(win * 100)}% 🔥</h2>
            <h2 style='color: red;'>{bowling_team} - {round(loss * 100)}% ❄️</h2>
        </div>
    """, unsafe_allow_html=True)