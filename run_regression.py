import featurize, load_data, numpy as np
import sklearn.linear_model
from scipy import stats

data = load_data.load_data()
data.tempo /= np.max(data.tempo)

audio_features1 = ['mode','tempo','danceability','acousticness','instrumentalness']
audio_features2 = ['acousticness','danceability','duration_ms','energy','instrumentalness','key','liveness','loudness','mode','speechiness','tempo','time_signature','valence']

genre_features = [d for d in list(data.columns) if 'genre_' in d]

feats = audio_features1+genre_features

def run_regression(features):
	X = data[features]
	y = data.averageRating
	significant_feats = []
	for feature in features:
		sig = test_significance(X,y,feature)
		if sig.pvalue < 0.05:
			significant_feats.append(feature)
	model = sklearn.linear_model.LinearRegression()
	#X = data[significant_feats]
	model.fit(X,y)
	score = model.score(X,y)
	coefs = zip(features,[("%0.4f" % c) for c in model.coef_])
	coef_vals = [float(c[1]) for c in coefs]
	order = np.argsort(coef_vals)
	coefs = np.array(coefs)[order]
	print "Score: " + str(score)
	for c in coefs:
		if c[0] in significant_feats: print c
	print 

def test_significance(X,y,feature):
	return stats.linregress(X[feature],y)

run_regression(feats)
