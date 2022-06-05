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

st.markdown("<h1 style='text-align: center; color: white;'>DJ ASSISTANT</h1>", unsafe_allow_html=True) # Header
Name_of_Artist = st.text_input("Artist Name") # Input artist name
Name_of_song = st.text_input("Song Name") # Input song name

# Add customizability features and toogle switch:
with st.expander("Advanced features"):
    mintempo = st.checkbox("Minimum BPM")
    maxtempo = st.checkbox("Maximum BPM")
    key = st.checkbox("Same key")
    if mintempo == True:
        tempo_min = st.slider("Minimum BPM", 50, 250, None)
    if maxtempo == True:
        tempo_max = st.slider("Maximum BPM", 50, 250, None)


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

    # Load audio features for song:
    your_song_feats = (sp.audio_features(track_uri)[0])

    #st.write(round(your_song_feats["tempo"])) # Sanity check

    # Save features as dataframe:
    df = pd.DataFrame(your_song_feats, index=[0])

    # Dataframe cleaning:
    df = df.drop(['id','uri','track_href','analysis_url','type', 'danceability', 'energy', 'loudness', 'mode','speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'time_signature'], axis=1)

    df['tempo'] = int(round(df['tempo']))

    df = df.rename({0: "Value"})
    df = df.rename(columns = {'key': "Key", "tempo": "Tempo", "duration_ms": "Duration"})


    # Specify key
    if key == True:
        key_target = int(df['Key'])
        #st.write(key_target)

    #print(key_target)


    # Display dataframe.
    #st.dataframe(df) # Sanity check

    track_uri = [track_uri]
    
    
    l = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    d = dict([(y,x) for x,y in enumerate(l)])
    inv_map = {v: k for k, v in d.items()}

    df['Key'] = inv_map[int(df['Key'])]
    #st.write(int(key_target))


    #####
    # Convert from ms to m:s.
    ms = int(df['Duration'])
    seconds, ms = divmod(ms, 1000)
    minutes, seconds = divmod(seconds, 60)
    df['Duration'] = f'{int(minutes):01d}:{int(seconds):02d}'

    
    #####
    
    st.write("Your song info:")
    st.dataframe(df)
    st.write("Press go when you are ready")




        

# Info:

# Add activation button:
state = st.button("Find your next track") # Press when ready

# Specify what buttons do:
if state == False: # If go button is not pressed:
    st.write("")
#elif advanced == True: # If go button is pressed and advanced settings switch is also pressed:
elif key == True and mintempo == True and maxtempo == True:
    recomms = sp.recommendations(seed_tracks = track_uri, limit=1, min_tempo = tempo_min, max_tempo = tempo_max, target_key = key_target) # target_key = 6
    artist_name = (recomms['tracks'][0]['album']['artists'][0]['name']) # artist name
    song_name = (recomms['tracks'][0]['name']) # song name 
    song_uri = (recomms['tracks'][0]['uri']) # uri name 
    image_url = recomms['tracks'][0]['album']['images'][0]['url']
    import requests
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    st.subheader(f"Here is your next track:")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
    st.caption("Click image for redirection to Spotify.")
elif key == True and mintempo == True:
    recomms = sp.recommendations(seed_tracks = track_uri, limit=1, min_tempo = tempo_min, target_key = key_target) # target_key = 6
    artist_name = (recomms['tracks'][0]['album']['artists'][0]['name']) # artist name
    song_name = (recomms['tracks'][0]['name']) # song name 
    song_uri = (recomms['tracks'][0]['uri']) # uri name 
    image_url = recomms['tracks'][0]['album']['images'][0]['url']
    import requests
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    st.subheader(f"Here is your next track:")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
    st.caption("Click image for redirection to Spotify.")
elif key == True and maxtempo == True:
    recomms = sp.recommendations(seed_tracks = track_uri, limit=1, max_tempo = tempo_max, target_key = key_target) # target_key = 6
    artist_name = (recomms['tracks'][0]['album']['artists'][0]['name']) # artist name
    song_name = (recomms['tracks'][0]['name']) # song name 
    song_uri = (recomms['tracks'][0]['uri']) # uri name 
    image_url = recomms['tracks'][0]['album']['images'][0]['url']
    import requests
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    st.subheader(f"Here is your next track:")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
    st.caption("Click image for redirection to Spotify.")
elif mintempo == True and maxtempo == True:
    recomms = sp.recommendations(seed_tracks = track_uri, limit=1, min_tempo = tempo_min, max_tempo = tempo_max) # target_key = 6
    artist_name = (recomms['tracks'][0]['album']['artists'][0]['name']) # artist name
    song_name = (recomms['tracks'][0]['name']) # song name 
    song_uri = (recomms['tracks'][0]['uri']) # uri name 
    image_url = recomms['tracks'][0]['album']['images'][0]['url']
    import requests
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    st.subheader(f"Here is your next track:")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
    st.caption("Click image for redirection to Spotify.")
elif mintempo == True:
    recomms = sp.recommendations(seed_tracks = track_uri, limit=1, min_tempo = tempo_min) # target_key = 6
    artist_name = (recomms['tracks'][0]['album']['artists'][0]['name']) # artist name
    song_name = (recomms['tracks'][0]['name']) # song name 
    song_uri = (recomms['tracks'][0]['uri']) # uri name 
    image_url = recomms['tracks'][0]['album']['images'][0]['url']
    import requests
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    st.subheader(f"Here is your next track:")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
    st.caption("Click image for redirection to Spotify.")
elif maxtempo == True:
    recomms = sp.recommendations(seed_tracks = track_uri, limit=1, max_tempo = tempo_max) # target_key = 6
    artist_name = (recomms['tracks'][0]['album']['artists'][0]['name']) # artist name
    song_name = (recomms['tracks'][0]['name']) # song name 
    song_uri = (recomms['tracks'][0]['uri']) # uri name 
    image_url = recomms['tracks'][0]['album']['images'][0]['url']
    import requests
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    st.subheader(f"Here is your next track:")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
    st.caption("Click image for redirection to Spotify.")
elif key == True:
    recomms = sp.recommendations(seed_tracks = track_uri, limit=1, target_key = key_target) # target_key = 6
    artist_name = (recomms['tracks'][0]['album']['artists'][0]['name']) # artist name
    song_name = (recomms['tracks'][0]['name']) # song name 
    song_uri = (recomms['tracks'][0]['uri']) # uri name 
    image_url = recomms['tracks'][0]['album']['images'][0]['url']
    import requests
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    st.subheader(f"Here is your next track:")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
    st.caption("Click image for redirection to Spotify.")
else: # If go button is pressed but advanced settings switch is not pressed:
    recomms = sp.recommendations(seed_tracks = track_uri, limit=1)
    artist_name = (recomms['tracks'][0]['album']['artists'][0]['name']) # artist name
    song_name = (recomms['tracks'][0]['name']) # song name 
    song_uri = (recomms['tracks'][0]['uri']) # uri name 
    image_url = recomms['tracks'][0]['album']['images'][0]['url']
    import requests
    img_data = requests.get(image_url).content
    with open('image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    st.subheader(f"Here is your next track:")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
    st.caption("Click image for redirection to Spotify.")



with st.expander("How to use"):
    st.subheader("Welcome to DJ ASSISTANT — Your new tool for creating amazing DJ-sets!")
    st.write("DJ ASSISTANT is an AI-based song recommender that can assist you in creating a coherent and streamlined DJ-set without ever being afraid of embarrassing crossfades. All you need to get started is a song that you like. DJ ASSISTANT will then proceed to recommend a similar song that you can use as the next song for your set.")
    st.write("It works like this:")
    st.write("1. Specify the artist and song name for a track that you like.")
    st.write("2. If you want the recommended song to be in the same key* or have specific BPM requirements, you can specify this under 'Advanced features'.")
    st.write("3. Press the 'Find your next track'-button to let DJ ASSISTANT work its magic.") 
    st.write("4. Click on the song artwork for a direct redirection to the song on Spotify.") 
    st.write(" ")
    st.caption("NOTE: You can find the BPM, key and duration of your self-chosen track in the table that appears when you have specified artist- and song name")
    st.caption("*: DJ ASSISTANT does currently not discriminate minor and major keys and will only filter based on the 'root'-key (e.g. G or C#).")



# expander with info: https://docs.streamlit.io/library/api-reference/layout/st.expander