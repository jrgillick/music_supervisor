import featurize, load_data

data = load_data.load_data()

audio_features = ['acousticness','danceability','duration_ms','energy','instrumentalness','key','liveness','loudness','mode','speechiness','tempo','time_signature','valence']

feats = data.script
y = data[audio_features]

