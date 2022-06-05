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
Types_of_Features = ("danceability", "energy", "valence", "instrumentalness")



st.markdown("<h1 style='text-align: center; color: white;'>DJ Assistant</h1>", unsafe_allow_html=True) # Header
Name_of_Artist = st.text_input("Artist Name") # Input artist name
Name_of_song = st.text_input("Song Name") # Input song name

# Add customizability features and toogle switch:
with st.expander("Advanced features"):
    mintempo = st.checkbox("Minimum BPM")
    maxtempo = st.checkbox("Maximum BPM")
    key = st.checkbox("Same key")
    audiofeature = st.checkbox("Auditory feature")
    if mintempo == True:
        tempo_min = st.slider("Minimum BPM", 10, 200, None)
    if maxtempo == True:
        tempo_max = st.slider("Maximum BPM", 10, 200, None)
    if audiofeature == True:
        name_of_feat = st.selectbox("Selcet your auditory feature", Types_of_Features)
        if st.checkbox("Description of audio features"):
            "- Hello world"
            "- sd "
            "- asda"
            "- bla bla bla"



#st.write(Name_of_Feat)

#advanced = st.checkbox('Advanced features')

#if advanced == True:
#    tempo = st.checkbox("tempo")
#    key = st.checkbox("key")
#    if tempo == True:
#        tempo_max = st.slider("Max tempo?", 10, 200, None)
#    if key == True:
#        key_target = st.slider("Target key?", 1, 12, None)

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



    if key == True:
        key_target = df['key']
        #st.write(key_target)
        

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
    st.subheader(f"Here is your next track (click image for link):")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
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
    st.subheader(f"Here is your next track (click image for link):")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
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
    st.subheader(f"Here is your next track (click image for link):")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
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
    st.subheader(f"Here is your next track (click image for link):")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
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
    st.subheader(f"Here is your next track (click image for link):")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
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
    st.subheader(f"Here is your next track (click image for link):")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
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
    st.subheader(f"Here is your next track (click image for link):")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")
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
    st.subheader(f"Here is your next track (click image for link):")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")   
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
    st.subheader(f"Here is your next track (click image for link):")
    st.write(f"Song: {song_name}")
    st.write(f"By: {artist_name}")
    st.markdown(f"[![Foo]({image_url})]({song_uri})")

    

# expander with info: https://docs.streamlit.io/library/api-reference/layout/st.expander