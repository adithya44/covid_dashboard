import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title('Covid Dashboard')
data_path = 'districts.csv'


@st.cache()
def load_data():
    data = pd.read_csv(data_path)
    data.set_index('Date',inplace=True)
    #data.drop(index='2021-05-19',inplace=True)
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text('Data loaded!')

def plot_timeseries(actuals, predicted=None):
    traces = []
    actuals = go.Scatter(name=actuals.name,
                         x=actuals.index,
                         y=actuals,
                         marker=dict(size=12,
                                     color="blue"
                                     ))
    traces.append(actuals)
    if predicted is not None:
        predicted = go.Scatter(name=predicted.name,
                               x=predicted.index,
                               y=predicted,
                               marker=dict(size=12,
                                           color="green"))
        traces.append(predicted)
    fig = go.Figure(data=traces)
    return fig

def get_detailed_data(df,state=None,district=None):
    if state:
        df = df.loc[df['State']==state]
    if district:
        df = df.loc[df['District']==district]
    df = df.groupby(by='Date').sum()
    df['prev_confirm'] = df['Confirmed'].shift(1)
    df['prev_recover'] = df['Recovered'].shift(1)
    df['prev_decease'] = df['Deceased'].shift(1)
    df['daily_cases'] = df['Confirmed'] - df['prev_confirm']
    df['daily_cured'] = df['Recovered'] - df['prev_recover']
    df['daily_deaths'] = df['Deceased'] - df['prev_decease']
    df['active_cases'] = df['Confirmed'] - df['Recovered'] - df['Deceased']
    df['recovery_vs_cases'] = df['daily_cases'] - df['daily_cured']
    df['shift'] = df['daily_cases'].shift(1)
    df['percentage_change'] = ((df['daily_cases'] - df['shift']) / df['daily_cases']) * 100
    df['meanval'] = df['daily_cases'].rolling(window=5).mean()
    return df

india_df = get_detailed_data(data)


# st.subheader('India data')
# st.write(data)

st.subheader('Daily cases')
india_chart = plot_timeseries(india_df['daily_cases'])
st.plotly_chart(india_chart)

st.subheader('Avg cases')
india_chart = plot_timeseries(india_df['meanval'])
st.plotly_chart(india_chart)

# st.subheader('Recovery vs Cases')
# india_chart = plot_timeseries(india_df['recovery_vs_cases'])
# st.plotly_chart(india_chart)


states = data['State'].unique()

state_selected = st.selectbox(
'Select state', states
)

districts = data.loc[data['State']==state_selected]['District'].unique()
district_selected = st.selectbox(
'Select district', districts
)


st.write('You selected:', state_selected)


state_df = get_detailed_data(data,state_selected)
# st.subheader('State data')
# st.write(state_df)

st.subheader('Daily cases')
state_chart = plot_timeseries(state_df['daily_cases'])
st.plotly_chart(state_chart)

st.subheader('Avg cases')
state_chart = plot_timeseries(state_df['meanval'])
st.plotly_chart(state_chart)

# st.subheader('Recovery vs Cases')
# state_chart = plot_timeseries(state_df['recovery_vs_cases'])
# st.plotly_chart(state_chart)

state_chart = plot_timeseries(state_df['daily_cases'])
st.plotly_chart(state_chart)


district_df = get_detailed_data(data,state_selected,district_selected)
# st.subheader('District data')
# st.write(district_df)

st.subheader('Daily cases')
district_chart = plot_timeseries(district_df['daily_cases'])
st.plotly_chart(district_chart)


st.subheader('Avg cases')
district_chart = plot_timeseries(district_df['meanval'])
st.plotly_chart(district_chart)

# st.subheader('Recovery vs Cases')
# district_chart = plot_timeseries(district_df['recovery_vs_cases'])
# st.plotly_chart(district_chart)

