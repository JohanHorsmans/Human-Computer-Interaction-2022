# Setup
import streamlit as st
import spotipy
import altair as alt 
from spotipy_client import *
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

client_id = 'ff0973a833764edda878ecd1a526e5e5'
client_secret = '17ac9bc2d757421e9be9e6bbf3a30984'

spotify = SpotifyAPI(client_id, client_secret)

client_credentials_manager = SpotifyClientCredentials(client_id="ff0973a833764edda878ecd1a526e5e5", client_secret="17ac9bc2d757421e9be9e6bbf3a30984")
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


# Main part of the script: 

st.markdown("<h1 style='text-align: center; color: white;'>DJ Assistant</h1>", unsafe_allow_html=True) # Header
Name_of_Artist = st.text_input("Artist Name") # Input artist name
Name_of_song = st.text_input("Song Name") # Input song name

# Add customizability features and toogle switch:
advanced = st.checkbox('Advanced features')

if advanced == True:
    tempo_max = st.slider("Max tempo?", 10, 200, None)

# Don't move on with the script until you have entered names:

if len(Name_of_Artist) == 0: 
    st.write("Hello! Welcome to my app - please, enter the artist name") 
elif len(Name_of_song) == 0:
    st.write("Hello! Welcome to my app - please, enter the song name to see song statistics")
else: # Names are specified -> move on.
    Data = spotify.search({"artist": f"{Name_of_Artist}", "track": f"{Name_of_song}"}, search_type="track") # Load the data for the specified track

    metadata = [] # Create empty list for meta data

    # Data is saved as nested dictionary. Create loop for saving info for the selected song.
    for song, info in enumerate(Data['tracks']['items']):
        track = info['album'] # Save track info.
        song_name = info['name'] # Save song name.
        track_uri = info["uri"] # Save link for song.
        metadata.append((song, track['artists'][0]['name'], song_name, track['release_date'])) # Append artist name, song name and release date to metadata-list.

    #st.write(metadata[0][1]) # Sanity check
    #st.write(metadata[0][2]) # Sanity check
    #st.write(metadata[0][3]) # Sanity check

    # Load audio features for song:
    your_song_feats = (sp.audio_features(track_uri)[0])

    #st.write(round(your_song_feats["tempo"])) # Sanity check

    # Save features as dataframe:
    df = pd.DataFrame(your_song_feats, index=[0])

    # Dataframe cleaning:
    df = df.drop(['id','uri','track_href','analysis_url','type'], axis=1)

    df['tempo'] = int(round(df['tempo']))

    df = df.rename({0: "Value"})

    # Display dataframe.
    #st.dataframe(df) # Sanity check

    track_uri = [track_uri]
    
    st.write("Your song info:")
    st.dataframe(df)
    st.write("Press go when you are ready")





# Info:


# Add activation button:
state = st.button("Find your next track") # Press when ready

# Specify what buttons do:
if state == False: # If go button is not pressed:
    st.write("")
elif advanced == True: # If go button is pressed and advanced settings switch is also pressed:
    recomms = sp.recommendations(seed_tracks = track_uri, limit=1, max_tempo = tempo_max) # target_key = 6
    #st.write(recomms)
    st.write("You should spin:")
    st.write(recomms['tracks'][0]['album']['artists'][0]['name']) # artist name
    st.write(recomms['tracks'][0]['name']) # song name 
    st.write(recomms['tracks'][0]['uri']) # uri name 
else: # If go button is pressed but advanced settings switch is not pressed:
    recomms = sp.recommendations(seed_tracks = track_uri, limit=1)
    #st.write(recomms)


    st.write("You should spin:")
    st.write(recomms['tracks'][0]['album']['artists'][0]['name']) # artist name
    st.write(recomms['tracks'][0]['name']) # song name 
    st.write(recomms['tracks'][0]['uri']) # uri name 



