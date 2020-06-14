'''
title           : read_structure_store_data.py
description     : 
author          : Adil Moujahid
date_created    : 20200614
date_modified   : 20200614
version         : 1.0
usage           : python structure_data.py
python_version  : 3.7.6
'''

import json
import unicodedata
import numpy as np
import pandas as pd


with open('./data/matches_Spain.json') as json_file:
    matches_spain_data = json.load(json_file)

with open('./data/events_Spain.json') as json_file:
    events_spain_data = json.load(json_file)

#Structure all Real Madrid and FC Barcelona matches information into 2 Pandas DataFrames.
barca_matches  = [match for match in matches_spain_data if '676' in match['teamsData'].keys()]
real_matches  = [match for match in matches_spain_data if '675' in match['teamsData'].keys()]

barca_matches_df = pd.DataFrame(barca_matches)
real_matches_df = pd.DataFrame(real_matches)

#Structure Messi and Ronaldo's events data
messi_events_data = []
for event in events_spain_data:
    if event['playerId'] == 3359:
        messi_events_data.append(event)
        
messi_events_data_df = pd.DataFrame(messi_events_data)

ronaldo_events_data = []
for event in events_spain_data:
    if event['playerId'] == 3322:
        ronaldo_events_data.append(event)

ronaldo_events_data_df = pd.DataFrame(ronaldo_events_data)


#Adding tags to events data
def add_tag(tags, tag_id):
    return tag_id in [tag['id'] for tag in tags]

messi_events_data_df['goal'] = messi_events_data_df['tags'].apply(lambda x: add_tag(x, 101))
messi_events_data_df['assist'] = messi_events_data_df['tags'].apply(lambda x: add_tag(x, 301))
messi_events_data_df['key_pass'] = messi_events_data_df['tags'].apply(lambda x: add_tag(x, 302))
messi_events_data_df['left_foot'] = messi_events_data_df['tags'].apply(lambda x: add_tag(x, 401))
messi_events_data_df['right_foot'] = messi_events_data_df['tags'].apply(lambda x: add_tag(x, 402))

ronaldo_events_data_df['goal'] = ronaldo_events_data_df['tags'].apply(lambda x: add_tag(x, 101))
ronaldo_events_data_df['assist'] = ronaldo_events_data_df['tags'].apply(lambda x: add_tag(x, 301))
ronaldo_events_data_df['key_pass'] = ronaldo_events_data_df['tags'].apply(lambda x: add_tag(x, 302))
ronaldo_events_data_df['left_foot'] = ronaldo_events_data_df['tags'].apply(lambda x: add_tag(x, 401))
ronaldo_events_data_df['right_foot'] = ronaldo_events_data_df['tags'].apply(lambda x: add_tag(x, 402))


messi_events_data_df = pd.merge(messi_events_data_df, barca_matches_df, left_on='matchId', right_on='wyId', copy=False, how="left")
ronaldo_events_data_df = pd.merge(ronaldo_events_data_df, real_matches_df, left_on='matchId', right_on='wyId', copy=False, how="left")

#Saving Data to Disk
messi_events_data_df.to_pickle('./data/messi_events_data_df.pkl')
ronaldo_events_data_df.to_pickle('./data/ronaldo_events_data_df.pkl')

#Getting matches dates
barca_matches_dates_df = barca_matches_df[['label', 'date']].copy()
real_matches_dates_df = real_matches_df[['label', 'date']].copy()

barca_matches_dates_df['date'] = pd.to_datetime(barca_matches_df['date'], utc=True).dt.date
real_matches_dates_df['date'] = pd.to_datetime(real_matches_df['date'], utc=True).dt.date

#Change date to string 
barca_matches_dates_df['date'] = barca_matches_dates_df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))
real_matches_dates_df['date'] = real_matches_dates_df['date'].apply(lambda x: x.strftime('%Y-%m-%d'))

barca_matches_dates_df = barca_matches_dates_df.rename(columns={"label": "match"})
real_matches_dates_df = real_matches_dates_df.rename(columns={"label": "match"})

barca_matches_dates_df.to_pickle('./data/barca_matches_dates_df.pkl')
real_matches_dates_df.to_pickle('./data/real_matches_dates_df.pkl')

