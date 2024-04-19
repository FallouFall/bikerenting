import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import scipy.stats as stats
import pandas as pd
from sklearn.ensemble import RandomForestRegressor


# Load data

nrows = st.slider("Select the number of rows to read:", min_value=1000, max_value=2000, step=100)
try:
  df = pd.read_csv("data/day.csv", index_col=False, nrows=nrows)

except FileNotFoundError:
  st.error("Error: Data file not found. Please check the path.")


if 'df' in locals():
  st.subheader("Data Preview")
  df = pd.DataFrame(df)
  st.write(df)

st.divider()
# Data preprocessing
df.rename(columns={'instant': 'rec_id', 'dteday': 'datetime', 'yr': 'year', 'mnth': 'month',
                   'weathersit': 'weather_condition', 'hum': 'humidity', 'cnt': 'total_count'}, inplace=True)
df['datetime'] = pd.to_datetime(df['datetime'])
df['season'] = df['season'].astype('category')
df['year'] = df['year'].astype('category')
df['month'] = df['month'].astype('category')
df['holiday'] = df['holiday'].astype('category')
df['weekday'] = df['weekday'].astype('category')
df['workingday'] = df['workingday'].astype('category')
df['weather_condition'] = df['weather_condition'].astype('category')

st.title("🚴 Bike Sharing System 🚴")

st.sidebar.image("data/eae_img.png", width=200)
st.sidebar.write("""
Bike sharing systems represent a modern evolution of traditional bike rentals, where the entire process—from membership to rental and return—is automated. These systems enable users to effortlessly rent a bike from one location and return it to another. Currently, there are over 500 bike-sharing programs worldwide, comprising more than 500 thousand bicycles. The growing interest in these systems stems from their significant impact on traffic, environmental sustainability, and public health.

Beyond their practical applications, bike sharing systems generate rich datasets that are of interest for research purposes. The goal is to develop an end-to-end regression task, where the user provides the data and receives results from the best-performing hyper-tuned machine learning model. Additionally, users have the flexibility to select deployment options that best suit their needs.
""")

st.subheader("Total rental bikes per Month Season")
season_names = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df['season_name'] = df['season'].map(season_names)
fig = px.bar(df, x='month', y='total_count', color='season_name', barmode='group',
             title='Season',
             labels={'total_count': 'Total Rental Bikes', 'month': 'Month', 'season_name': 'Season'},
             color_continuous_scale='deepbluesky')
fig.update_layout(title_font_size=20, title_font_family='Arial')
st.plotly_chart(fig)
st.divider()

st.subheader("Weekday Performance On the Year")
weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df['weekday_name'] = df['weekday'].apply(lambda x: weekday_names[x])
fig = px.bar(df, x='month', y='total_count', color='weekday_name', barmode='group',
             title='Weekday',
             labels={'total_count': 'Total Rental Bikes', 'month': 'Month', 'weekday_name': 'Weekday'},
             color_continuous_scale='deepbluesky')
fig.update_layout(title_font_size=20, title_font_family='Arial')
st.plotly_chart(fig)
st.divider()

st.subheader("Workingday Performance On Season")
season_names = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df_sorted = df.sort_values(by='total_count', ascending=True)
df_sorted['season_name'] = df_sorted['season'].replace(season_names)
fig = px.bar(df_sorted, x='workingday', y='total_count', color='season_name',
             title='Workingday',
             labels={'total_count': 'Total Rental Bikes', 'workingday': 'Working Day', 'season_name': 'Season'},
             color_continuous_scale='deepbluesky')
fig.update_layout(title_font_size=20, title_font_family='Arial')
st.plotly_chart(fig)
st.divider()

st.subheader("Holiday distribution")
season_names = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df['season_name'] = df['season'].replace(season_names)
fig = px.violin(df, x='holiday', y='total_count', color='season_name',
                title='Holiday wise distribution of counts (colored by Season)',
                labels={'total_count': 'Total Rental Bikes', 'holiday': 'Holiday', 'season_name': 'Season'},
                color_discrete_sequence=px.colors.qualitative.Bold)
fig.update_layout(title_font_size=20, title_font_family='Arial')
st.plotly_chart(fig)
st.divider()

st.subheader("Total rental bikes : Weather Condition")
weather_names = {1: "Clear, Few clouds, Partly cloudy", 2: "Mist + Cloudy, Mist , Broken clouds,",
                 3: "Light Snow, Light Rain , Thunderstorm ", 4: "Heavy Rain , Ice Pallets "}
df['weather_name'] = df['weather_condition'].replace(weather_names)
colors = px.colors.qualitative.Set1[:len(df['weather_condition'].unique())]
fig = px.bar(df, x='weather_condition', y='total_count', color='weather_name',
             color_discrete_sequence=colors,
             title='Weather Condition wise Monthly Distribution of Counts',
             labels={'total_count': 'Total ', 'weather_condition': 'Weather Code', 'weather_name': 'Weather Condition'})
fig.update_layout(title_font_size=20, title_font_family='Arial')
st.plotly_chart(fig)
st.divider()

st.subheader("Outliers Analysis of total rental bikes")
fig = px.box(df, y='total_count',
             title='Total rental bikes',
             labels={'total_count': 'Total rental bikes'},
             color_discrete_sequence=px.colors.qualitative.Bold)
fig.update_layout(title_font_size=20, title_font_family='Arial')
st.plotly_chart(fig)
st.divider()

st.subheader("Outliers Analysis Of different Weather Conditions")
colors = px.colors.qualitative.Set1[:len(df[['temp', 'windspeed', 'humidity']].columns)]
fig = px.box(df[['temp', 'windspeed', 'humidity']],
             title='Temp, Windspeed, Humidity Outliers',
             labels={'value': 'Value', 'variable': 'Variable'},
             color='variable', color_discrete_sequence=colors)
fig.update_layout(title_font_size=20, title_font_family='Arial')
st.plotly_chart(fig)
st.divider()

st.subheader("Q-Q Plot Total rental bikes")
def plot_curve(df, feature):
    hist_trace = go.Histogram(x=df[feature], marker=dict(color='skyblue'))
    hist_fig = go.Figure(data=[hist_trace],
                         layout=dict(title="Histogram of Total rental bikes ",
                                     height=500,
                                     width=500))

    qq_plot = stats.probplot(df[feature], dist='norm', fit=True)
    qq_plot_trace = go.Scatter(x=qq_plot[0][0], y=qq_plot[0][1], mode='markers', marker=dict(color='salmon'))
    qq_plot_fig = go.Figure(data=[qq_plot_trace],
                            layout=dict(title="Q-Q Plot of Total rental bikes  ",
                                        height=500,
                                        width=500))

    st.plotly_chart(hist_fig)
    st.plotly_chart(qq_plot_fig)

plot_curve(df, 'total_count')
st.divider()

st.subheader("Heatmap Correlation of the different parameters")
correMtr = df[["temp", "atemp", "humidity", "windspeed", "casual", "registered", "total_count"]].corr()
fig = go.Figure(data=go.Heatmap(
    z=correMtr.values,
    x=correMtr.columns,
    y=correMtr.index,
    colorscale='blues',
    colorbar=dict(title='Correlation'),
    hoverongaps=False))

fig.update_layout(title='Correlation  of attributes',
                  xaxis=dict(title=''),
                  yaxis=dict(title=''))
st.plotly_chart(fig)
st.divider()