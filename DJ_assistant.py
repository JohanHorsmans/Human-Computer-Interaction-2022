import streamlit as st
import spotipy

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")


Types_of_Features = ("acousticness", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness", "tempo", "valence")

st.title("Spotify Features App")
Name_of_Artist = st.text_input("Artist Name")
Name_of_song = st.text_input("Song Name")
Name_of_Feat = st.selectbox("Feature", Types_of_Features)



#######
#if st.button("Dou you wanna customize?"):
 #   st.write("Good choice!")
 #   tempo_max = st.slider("Max tempo?", 10, 200, 120)


# Når knappen ikke er trykket ned, så er værdien none.

#######

button_clicked = st.button("OK")

from spotipy_client import *
import pandas as pd

client_id = 'ff0973a833764edda878ecd1a526e5e5'
client_secret = '17ac9bc2d757421e9be9e6bbf3a30984'

spotify = SpotifyAPI(client_id, client_secret)

Data = spotify.search({"artist": f"{Name_of_Artist}", "track": f"{Name_of_song}"}, search_type="track")



#Data = spotify.search({"track": f"{Name_of_song}"}, search_type="track")

#st.markdown(Data)

#st.dataframe(data=Data, width=None, height=None)

need = []
for i, item in enumerate(Data['tracks']['items']):
    track = item['album']
    track_id = item['id']
    song_name = item['name']
    popularity = item['popularity']
    track_uri = item["uri"]
    #explicit = item['explicit']
    need.append((i, track['artists'][0]['name'], track['name'], track_id, song_name, track['release_date'], popularity))
    #need.append((i, track['artists'][0]['name'], track['name'], track_id, song_name, track['release_date'], popularity, explicit))


#st.write(track) 

#st.markdown(need)

#st.write(track_uri)

## TUTORIAL 1:
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id="ff0973a833764edda878ecd1a526e5e5", client_secret="17ac9bc2d757421e9be9e6bbf3a30984")
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

your_song = st.write(sp.audio_features(track_uri)[0])

## TUROIAL 1 END


## TUTORIAL 2:
#Guide: https://spotipy.readthedocs.io/en/2.19.0/?highlight=recommend#spotipy.client.Spotify.recommendations


list = [track_uri]

st.write(track_uri)


#if  st.button("Do u you wanna customize?"):
#    st.write("Good choice!")
#    tempo_max = st.slider("Max tempo?", 10, 200, None)
#    if tempo_max == None:
#        print("please chose")
#    else:
#        recomms = sp.recommendations(seed_tracks = list, limit=1, min_tempo = tempo_max)
#        st.write(recomms)
#else: recomms = sp.recommendations(seed_tracks = list, limit=1)

if st.checkbox('Click me'):
    tempo_max = st.slider("Max tempo?", 10, 200, None)
    if st.button("Ready?"):
        recomms = sp.recommendations(seed_tracks = list, limit=1, max_tempo = tempo_max)
        st.write(recomms)
    else: st.write("waiting")

else: 
    recomms = sp.recommendations(seed_tracks = list, limit=1)
    st.write(recomms)


#recomms = sp.recommendations(seed_tracks = list, limit=1, max_tempo = tempo_max, max_key = 6, min_key = 3)
#st.write(recomms)

# max_key = 6 betyder at den aldrig kommer op på 6. Dvs. den ægte max key er 5. Det er ikke inklusiv tallet.


##

Track_df = pd.DataFrame(need, index=None, columns=('Item', 'Artist', 'Album Name', 'Id', 'Song Name', 'Release Date', 'Popularity'))

access_token = spotify.access_token

headers = {
    "Authorization": f"Bearer {access_token}"
}
endpoint = "https://api.spotify.com/v1/audio-features/"

Feat_df = pd.DataFrame()
for id in Track_df['Id'].iteritems():
    track_id = id[1]
    lookup_url = f"{endpoint}{track_id}"
    ra = requests.get(lookup_url, headers=headers)
    audio_feat = ra.json()
    Features_df = pd.DataFrame(audio_feat, index=[0])
    Feat_df = Feat_df.append(Features_df)

Full_Data = Track_df.merge(Feat_df, left_on="Id", right_on="id")

Sort_DF = Full_Data.sort_values(by=['Popularity'], ascending=False)

chart_df = Sort_DF[['Artist', 'Album Name', 'Song Name', 'Release Date', 'Popularity', f'{Name_of_Feat}']]

import altair as alt

feat_header = Name_of_Feat.capitalize()

st.header(f'{feat_header}' " vs. Popularity")
c = alt.Chart(chart_df).mark_circle().encode(
    alt.X('Popularity', scale=alt.Scale(zero=False)), y=f'{Name_of_Feat}', color=alt.Color('Popularity', scale=alt.Scale(zero=False)), 
    size=alt.value(200), tooltip=['Popularity', f'{Name_of_Feat}', 'Song Name', 'Album Name'])

st.altair_chart(c, use_container_width=True)

st.header("Table of Attributes")
st.table(chart_df)

st.write("acousticness: Confidence measure from 0.0 to 1.0 on if a track is acoustic.")
st.write("danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.")
st.write("energy: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.")
st.write("instrumentalness: Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.")
st.write("liveness: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.")
st.write("loudness: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.")
st.write("speechiness: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.")
st.write("tempo: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.")
st.write("valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).")


st.write("Information about features is from:  https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/")