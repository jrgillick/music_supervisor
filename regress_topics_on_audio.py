import featurize, load_data, numpy as np
import sklearn.linear_model
from scipy import stats
import statsmodels.api as sm
import sys
from sklearn import preprocessing
import pandas as pd

data = load_data.load_data()
data.tempo /= np.max(data.tempo)

topics=["topic-0-nice-bit", "topic-1-sir-dear", "topic-2-christmas-la", "topic-3-dad-mom", "topic-4-sir-colonel", "topic-5-um-work", "topic-6-president-mr.", "topic-7-japanese-dawson", "topic-8-unsub-garcia", "topic-9-game-team", "topic-10-sir-captain", "topic-11-mr.-court", "topic-12-boat-water", "topic-13-leave-understand", "topic-14-fuck-shit", "topic-15-war-country", "topic-16-years-world", "topic-17-plane-move", "topic-18-captain-ship", "topic-19-police-kill", "topic-20-bit-mum", "topic-21-ah-aah", "topic-22-'t-narrator", "topic-23-sighs-chuckles", "topic-24-ya-'em", "topic-25-remember-feel", "topic-26-boy-huh", "topic-27-mr.-sir", "topic-28-dr.-doctor", "topic-29-father-lord", "topic-30-money-business", "topic-31-alright-lt", "topic-32-sir-brother", "topic-33-school-class", "topic-34-vic-jax", "topic-35-gibbs-mcgee", "topic-36-monsieur-madame", "topic-37-baby-yo", "topic-38-agent-security", "topic-39-kill-dead", "topic-40-music-show", "topic-41-ofthe-thankyou", "topic-42-dude-cool", "topic-43-spanish-el", "topic-44-eat-nice", "topic-45-murder-killed", "topic-46-car-drive", "topic-47-town-horse", "topic-48-film-movie", "topic-49-woman-married"]

feats = topics

def run_regression_statsmodels(target, features):
	X = data[features]
	y = data[target]

	scaler = preprocessing.StandardScaler()
	X[topics] = scaler.fit_transform(X[topics])
	
	if target != "mode":
		X_with_bias_term = sm.add_constant(X)
		est = sm.OLS(y, X_with_bias_term)
		fit = est.fit()
		print(fit.summary())

	else:
		model = sklearn.linear_model.LogisticRegression()
		#X = data[significant_feats]
		model.fit(X,y)
		score = model.score(X,y)
		coefs = zip(features,[("%0.4f" % c) for c in model.coef_[0]])
		coef_vals = [float(c[1]) for c in coefs]
		order = np.argsort(coef_vals)
		coefs = np.array(coefs)[order]
		print "Score: " + str(score)
		for c in coefs:
			(score, feat)=c
			print "%s\t%s" % (score, feat)
		print 

# e.g. python regress_topic_audio_genre_on_rating.py danceability 
run_regression_statsmodels(sys.argv[1], feats)

