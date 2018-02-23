import featurize, load_data, numpy as np
from sklearn.preprocessing import StandardScaler
import sklearn.linear_model

data = load_data.load_data()
data.tempo /= np.max(data.tempo)

audio_features1 = ['mode','tempo','danceability','acousticness','instrumentalness']
audio_features2 = ['acousticness','danceability','duration_ms','energy','instrumentalness','key','liveness','loudness','mode','speechiness','tempo','time_signature','valence']

def run_regression(audio_features):
	X = data[audio_features]
	y = data.averageRating
	#scaler = StandardScaler()
	#print(scaler.fit(X))
	#X = scaler.transform(X)
	model = sklearn.linear_model.LinearRegression()
	model.fit(X,y)
	score = model.score(X,y)
	coefs = zip(audio_features,[("%0.4f" % c) for c in model.coef_])
	print "Score: " + str(score)
	print coefs
	print 
