'''
title           : app.py
description     : Streamlit app that compares Messi and Ronaldo's stats and shows their positions on the pitch.
author          : Adil Moujahid
date_created    : 20200521
date_modified   : 20200613
version         : 1.0
usage           : streamlit run app.py
python_version  : 3.7.6
'''

import datetime
import unicodedata

import markdown
import json
import numpy as np
import pandas as pd

import bokeh

import streamlit as st

from plots import *


@st.cache(allow_output_mutation=True)
def get_data(foot):

    #Reading Data
    messi_events_data_df = pd.read_pickle("./data/messi_events_data_df.pkl")
    ronaldo_events_data_df = pd.read_pickle("./data/ronaldo_events_data_df.pkl")

    #Dealing with double backslashes
    messi_events_data_df['label'] = messi_events_data_df['label'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))
    ronaldo_events_data_df['label'] = ronaldo_events_data_df['label'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))

    if foot == 'Left':
        messi_events_data_df = messi_events_data_df[messi_events_data_df['left_foot']]
        ronaldo_events_data_df = ronaldo_events_data_df[ronaldo_events_data_df['left_foot']]
    if foot == 'Right':
        messi_events_data_df = messi_events_data_df[messi_events_data_df['right_foot']]
        ronaldo_events_data_df = ronaldo_events_data_df[ronaldo_events_data_df['right_foot']]

    barca_matches_dates_df = pd.read_pickle("./data/barca_matches_dates_df.pkl")
    real_matches_dates_df = pd.read_pickle("./data/real_matches_dates_df.pkl")

    barca_matches_dates_df['match'] = barca_matches_dates_df['match'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))
    real_matches_dates_df['match'] = real_matches_dates_df['match'].apply(lambda x: bytes(x, encoding='utf-8').decode('unicode-escape'))

    return messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df


def plot_goals(messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df):

    #Getting events data positions
    messi_goals = messi_events_data_df[messi_events_data_df['goal'] == True]['positions']
    ronaldo_goals = ronaldo_events_data_df[ronaldo_events_data_df['goal'] == True]['positions']

    #Pitch with events
    p_messi = plot_events(messi_goals, 'Goals', 'red')
    p_ronaldo = plot_events(ronaldo_goals, 'Goals', 'blue')

    #Table
    messi_stats = messi_events_data_df.groupby(['label']).sum()['goal'].astype(int)
    messi_stats_df = pd.DataFrame(data=zip(messi_stats.index, messi_stats), columns=['match', '#goals'])
    ronaldo_stats = ronaldo_events_data_df.groupby(['label']).sum()['goal'].astype(int)
    ronaldo_stats_df = pd.DataFrame(data=zip(ronaldo_stats.index, ronaldo_stats), columns=['match', '#goals'])
    #Adding Dates
    messi_stats_df = pd.merge(messi_stats_df, barca_matches_dates_df, on='match', copy=False, how="left")
    ronaldo_stats_df = pd.merge(ronaldo_stats_df, real_matches_dates_df, on='match', copy=False, how="left")
    #Change order of columns
    messi_stats_df = messi_stats_df[['date', 'match', '#goals']]
    ronaldo_stats_df = ronaldo_stats_df[['date', 'match', '#goals']]

    grid = bokeh.layouts.grid(
        children=[
            [p_messi, p_ronaldo],
            [print_table(messi_stats_df), print_table(ronaldo_stats_df)],
        ],
        sizing_mode="stretch_width",
    )

    return bokeh.models.Panel(child=grid, title="Goals")


def plot_assists(messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df):

    #Getting events data positions
    messi_assists = messi_events_data_df[messi_events_data_df['assist'] == True]['positions']
    ronaldo_assists = ronaldo_events_data_df[ronaldo_events_data_df['assist'] == True]['positions']

    #Pitch with events
    p_messi = plot_events(messi_assists, 'Assists', 'red')
    p_ronaldo = plot_events(ronaldo_assists, 'Assists', 'blue')

    #Table
    messi_stats = messi_events_data_df.groupby(['label']).sum()['assist'].astype(int)
    messi_stats_df = pd.DataFrame(data=zip(messi_stats.index, messi_stats), columns=['match', '#assists'])
    ronaldo_stats = ronaldo_events_data_df.groupby(['label']).sum()['assist'].astype(int)
    ronaldo_stats_df = pd.DataFrame(data=zip(ronaldo_stats.index, ronaldo_stats), columns=['match', '#assists'])
    #Adding Dates
    messi_stats_df = pd.merge(messi_stats_df, barca_matches_dates_df, on='match', copy=False, how="left")
    ronaldo_stats_df = pd.merge(ronaldo_stats_df, real_matches_dates_df, on='match', copy=False, how="left")
    #Change order of columns
    messi_stats_df = messi_stats_df[['date', 'match', '#assists']]
    ronaldo_stats_df = ronaldo_stats_df[['date', 'match', '#assists']]

    grid = bokeh.layouts.grid(
        children=[
            [p_messi, p_ronaldo],
            [print_table(messi_stats_df), print_table(ronaldo_stats_df)],
        ],
        sizing_mode="stretch_width",
    )

    return bokeh.models.Panel(child=grid, title="Assists")


def plot_shots(messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df):

    #Getting events data positions
    messi_shots = messi_events_data_df[messi_events_data_df['eventName'] == 'Shot']['positions']
    ronaldo_shots = ronaldo_events_data_df[ronaldo_events_data_df['eventName'] == 'Shot']['positions']

    #Pitch with events
    p_messi = plot_events(messi_shots, 'Shots', 'red')
    p_ronaldo = plot_events(ronaldo_shots, 'Shots', 'blue')


    # Table
    messi_stats = messi_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    messi_stats_df = pd.DataFrame(data=zip(messi_stats[:, 'Shot'].index, messi_stats[:, 'Shot']), columns=['match', '#shots'])
    ronaldo_stats = ronaldo_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    ronaldo_stats_df = pd.DataFrame(data=zip(ronaldo_stats[:, 'Shot'].index, ronaldo_stats[:, 'Shot']), columns=['match', '#shots'])
    #Adding Dates
    messi_stats_df = pd.merge(messi_stats_df, barca_matches_dates_df, on='match', copy=False, how="left")
    ronaldo_stats_df = pd.merge(ronaldo_stats_df, real_matches_dates_df, on='match', copy=False, how="left")
    #Change order of columns
    messi_stats_df = messi_stats_df[['date', 'match', '#shots']]
    ronaldo_stats_df = ronaldo_stats_df[['date', 'match', '#shots']]

    grid = bokeh.layouts.grid(
        children=[
            [p_messi, p_ronaldo],
            [print_table(messi_stats_df), print_table(ronaldo_stats_df)],
        ],
        sizing_mode="stretch_width",
    )

    return bokeh.models.Panel(child=grid, title="Shots")

def plot_free_kicks(messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df):

    #Getting events data positions
    messi_free_kicks = messi_events_data_df[messi_events_data_df['subEventName'] == 'Free kick shot']['positions']
    ronaldo_free_kicks = ronaldo_events_data_df[ronaldo_events_data_df['subEventName'] == 'Free kick shot']['positions']

    #Pitch with events
    p_messi = plot_events(messi_free_kicks, 'Free Kicks', 'red')
    p_ronaldo = plot_events(ronaldo_free_kicks, 'Free Kicks', 'blue')

    # Table
    try:
        messi_stats = messi_events_data_df.groupby(['label', 'eventName']).count()['eventId']
        messi_stats_df = pd.DataFrame(data=zip(messi_stats[:, 'Free Kick'].index, messi_stats[:, 'Free Kick']), columns=['match', '#free kicks'])
    except:
        messi_stats_df = pd.DataFrame(columns=['match', '#free kicks'])
    try:
        ronaldo_stats = ronaldo_events_data_df.groupby(['label', 'eventName']).count()['eventId']
        ronaldo_stats_df = pd.DataFrame(data=zip(ronaldo_stats[:, 'Free Kick'].index, ronaldo_stats[:, 'Free Kick']), columns=['match', '#free kicks'])
    except:
        ronaldo_stats_df = pd.DataFrame(columns=['match', '#free kicks'])

    #Adding Dates
    messi_stats_df = pd.merge(messi_stats_df, barca_matches_dates_df, on='match', copy=False, how="left")
    ronaldo_stats_df = pd.merge(ronaldo_stats_df, real_matches_dates_df, on='match', copy=False, how="left")
    #Change order of columns
    messi_stats_df = messi_stats_df[['date', 'match', '#free kicks']]
    ronaldo_stats_df = ronaldo_stats_df[['date', 'match', '#free kicks']]


    grid = bokeh.layouts.grid(
        children=[
            [p_messi, p_ronaldo],
            [print_table(messi_stats_df), print_table(ronaldo_stats_df)],
        ],
        sizing_mode="stretch_width",
    )

    return bokeh.models.Panel(child=grid, title="Free Kicks")



def plot_passes(messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df):

    #Getting events data positions
    messi_passes = messi_events_data_df[messi_events_data_df['eventName'] == 'Pass']['positions']
    ronaldo_passes = ronaldo_events_data_df[ronaldo_events_data_df['eventName'] == 'Pass']['positions']

    #Pitch with events
    p_messi = plot_events(messi_passes, 'Passes', 'red')
    p_ronaldo = plot_events(ronaldo_passes, 'Passes', 'blue')

    # Table
    messi_stats = messi_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    messi_stats_df = pd.DataFrame(data=zip(messi_stats[:, 'Pass'].index, messi_stats[:, 'Pass']), columns=['match', '#passes'])
    ronaldo_stats = ronaldo_events_data_df.groupby(['label', 'eventName']).count()['eventId']
    ronaldo_stats_df = pd.DataFrame(data=zip(ronaldo_stats[:, 'Pass'].index, ronaldo_stats[:, 'Pass']), columns=['match', '#passes'])
    #Adding Dates
    messi_stats_df = pd.merge(messi_stats_df, barca_matches_dates_df, on='match', copy=False, how="left")
    ronaldo_stats_df = pd.merge(ronaldo_stats_df, real_matches_dates_df, on='match', copy=False, how="left")
    #Change order of columns
    messi_stats_df = messi_stats_df[['date', 'match', '#passes']]
    ronaldo_stats_df = ronaldo_stats_df[['date', 'match', '#passes']]

    grid = bokeh.layouts.grid(
        children=[
            [p_messi, p_ronaldo],
            [print_table(messi_stats_df), print_table(ronaldo_stats_df)],
        ],
        sizing_mode="stretch_width",
    )

    return bokeh.models.Panel(child=grid, title="Passes")


if __name__ == '__main__':

    #CSS to display content correctly
    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{
                max-width: 95%;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.write(''' ### Foot''')
    foot = st.sidebar.radio("", ('Either Left or Right', 'Left', 'Right'))
    messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df = get_data(foot)

    #Calculate Stats of both playters and structure them in a Pandas DataFrame
    goals = [messi_events_data_df['goal'].sum(), ronaldo_events_data_df['goal'].sum()]
    assists = [messi_events_data_df['assist'].sum(), ronaldo_events_data_df['assist'].sum()]
    shots = [messi_events_data_df[messi_events_data_df['eventName'] == 'Shot'].count()['eventName'],
             ronaldo_events_data_df[ronaldo_events_data_df['eventName'] == 'Shot'].count()['eventName']]
    free_kicks = [messi_events_data_df[messi_events_data_df['subEventName'] == 'Free kick shot'].count()['subEventName'], 
                ronaldo_events_data_df[ronaldo_events_data_df['subEventName'] == 'Free kick shot'].count()['subEventName']]
    passes = [messi_events_data_df[messi_events_data_df['eventName'] == 'Pass'].count()['eventName'],
            ronaldo_events_data_df[ronaldo_events_data_df['eventName'] == 'Pass'].count()['eventName']]

    stats_df = pd.DataFrame([goals, assists, shots, free_kicks, passes],
                            columns=['Messi', 'Ronaldo'], 
                            index=['Goals', 'Assists', 'Shots', 'Free Kicks', 'Passes'])

    st.sidebar.markdown(""" ### Stats """)
    st.sidebar.dataframe(stats_df)

    st.sidebar.write('''
        ### About
        Football logs are used to create an interactive Streamlit web app that analyzes Messi and Ronaldo's game during LaLiga season 2017-18. 
        The app compares both players' stats and shows their positions on the pitch.

        The app was developed by [adilmoujahid](https://github.com/adilmoujahid). ''')

    st.sidebar.write('''
    Checkout this [tutorial](http://adilmoujahid.com/posts/2020/06/streamlit-messi-ronaldo/) to learn how this app was built)
    ''')
    st.image('./messi_ronaldo.png', use_column_width=True, output_format='PNG')

    tabs = bokeh.models.Tabs(
        tabs=[
            plot_goals(messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df),
            plot_assists(messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df),
            plot_shots(messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df),
            plot_free_kicks(messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df),
            plot_passes(messi_events_data_df, ronaldo_events_data_df, barca_matches_dates_df, real_matches_dates_df),
        ]
    )
    st.bokeh_chart(tabs)