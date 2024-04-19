import streamlit as st
from pyforest import *
import warnings
warnings.filterwarnings('ignore')
import pickle

model = pickle.load(open('data/model.pkl', 'rb'))

# ----- Page configs -----
st.set_page_config(
    page_title="Fallou Fall Portfolio",
    page_icon="🧪",
)

st.title("🚴 Bike Renting Expectation  🚴")

st.sidebar.image("data/eae_img.png", width=200)
st.sidebar.write("""
Bike sharing systems represent a modern evolution of traditional bike rentals, where the entire process—from membership to rental and return—is automated. These systems enable users to effortlessly rent a bike from one location and return it to another. Currently, there are over 500 bike-sharing programs worldwide, comprising more than 500 thousand bicycles. The growing interest in these systems stems from their significant impact on traffic, environmental sustainability, and public health.

Beyond their practical applications, bike sharing systems generate rich datasets that are of interest for research purposes. The goal is to develop an end-to-end regression task, where the user provides the data and receives results from the best-performing hyper-tuned machine learning model. Additionally, users have the flexibility to select deployment options that best suit their needs.
""")



def load_data():
    data_path = "./../data/data.csv"
    df = pd.read_csv(data_path)
    return df

weekday_mapping = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
month_mapping = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
season_mapping = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
season_1 = season_2 = season_3 = season_4 = holiday_1 = holiday_2=False
working_1 = working_2 = False
weather_1 = weather_2 = weather_3 =False
weather_mapping = {'Clear, Few clouds,': 1, 'ist + Cloudy, Mist': 2, 'ight Snow, Light Rain ': 3}

user_input = {}
user_input['month'] = st.selectbox('Select month:', options=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
user_input['weekday'] = st.selectbox('Select weekday:', options=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
user_input['season'] = st.selectbox('Select season:', options=['Spring', 'Summer', 'Fall', 'Winter'])
user_input['weather'] = st.radio('Weather Day ?',  options=['Clear Few clouds' , 'Mist  Cloudy  Mist', 'Light Snow  Light Rain '])
user_input['temp'] = st.number_input('Enter value for temp:', step=1, min_value=0, max_value=45)
user_input['atemp'] = st.number_input('Enter value for atemp:', step=1, min_value=0, max_value=45)
user_input['humidity'] = st.number_input('Enter value for humidity:', step=1, min_value=20, max_value=100)
user_input['windspeed'] = st.number_input('Enter value for windspeed:', step=1, min_value=4, max_value=10)
user_input['workingDays'] = st.radio('Working Day ?', options=['Yes', 'No'])
user_input['casual'] = st.radio('Casual ?', options=['Yes', 'No'])
user_input['holiday'] = st.radio('Select Holiday ?', options=['Yes', 'No'])

if user_input['month'] in month_mapping:
    month = month_mapping[user_input['month']]


if user_input['season'] in season_mapping:
    season = season_mapping[user_input['season']]

if user_input['weekday'] in weekday_mapping:
    weekday = weekday_mapping[user_input['weekday']]

if user_input['season'] in season_mapping:
    selected_season = season_mapping[user_input['season']]
    if selected_season == 1:
        season_1 = True
    elif selected_season == 2:
        season_2 = True
    elif selected_season == 3:
         season_3 = True
    elif selected_season == 4:
        season_4 = True

    if user_input['holiday'] == "Yes":
        holiday_1 = True
        holiday_2 = False
    elif user_input['holiday'] == "No":
        holiday_1 = False
        holiday_2 = True

    if user_input['workingDays'] == "Yes":
        working_1 = True
        working_2 = False
    elif user_input['workingDays'] == "No":
        working_1 = False
        working_2 = True

        if user_input['weather'] == "Clear Few clouds" :
            weather_1 = True
            weather_2 = False
            weather_3=False
        elif user_input['weather'] == "Mist  Cloudy  Mist" :
            weather_1 = False
            weather_2 = True
            weather_3=False
        elif user_input['weather'] == "Light Snow  Light Rains" :
            weather_1 = False
            weather_2 = False
            weather_3=True

values = [month, weekday,user_input['temp']/40 ,user_input['atemp'] /50,user_input['humidity']/100,
          user_input['windspeed']/60,season_1,season_2, season_3, season_4, holiday_1, holiday_2,working_1,working_2,weather_1,
          weather_2,weather_3]






st.markdown(
    """
    <style>
    .stButton>button {
        background-color: red;
        color:#ffffff
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button('Predict'):

    prediction = model.predict([np.array(values)])
    st.markdown(
        f'<div style="background-color: lightgreen; padding: 10px; font-size: 27px;display: flex; align-items: center; justify-content: center;">Bike Rent expected: {prediction}</div>',
        unsafe_allow_html=True)
