import featurize, load_data, numpy as np
import sklearn.linear_model
from scipy import stats
import statsmodels.api as sm


data = load_data.load_data()
data.tempo /= np.max(data.tempo)

treatment_variable="danceability"

audio_features1 = ['mode','tempo','danceability','acousticness','instrumentalness']
audio_features2 = ['acousticness','danceability','duration_ms','energy','instrumentalness','key','liveness','loudness','mode','speechiness','tempo','time_signature','valence']


# topics=["topic-0-world-years", "topic-1-dr.-doctor", "topic-2-captain-sir", "topic-3-sighs-chuckles", "topic-4-sir-brother", "topic-5-i'ii-aii", "topic-6-game-team", "topic-7-leave-money", "topic-8-mr.-money", "topic-9-christmas-ya", "topic-10-dad-mom", "topic-11-car-water", "topic-12-president-country", "topic-13-kill-dead", "topic-14-music-show", "topic-15-agent-sir", "topic-16-police-killed", "topic-17-mr.-sir", "topic-18-shit-fuck", "topic-19-big-cool", "topic-20-um-feel", "topic-21-sir-captain", "topic-22-father-lord", "topic-23-bit-mum", "topic-24-mr.-money"]

topics=["topic-0-nice-bit", "topic-1-sir-dear", "topic-2-christmas-la", "topic-3-dad-mom", "topic-4-sir-colonel", "topic-5-um-work", "topic-6-president-mr.", "topic-7-japanese-dawson", "topic-8-unsub-garcia", "topic-9-game-team", "topic-10-sir-captain", "topic-11-mr.-court", "topic-12-boat-water", "topic-13-leave-understand", "topic-14-fuck-shit", "topic-15-war-country", "topic-16-years-world", "topic-17-plane-move", "topic-18-captain-ship", "topic-19-police-kill", "topic-20-bit-mum", "topic-21-ah-aah", "topic-22-'t-narrator", "topic-23-sighs-chuckles", "topic-24-ya-'em", "topic-25-remember-feel", "topic-26-boy-huh", "topic-27-mr.-sir", "topic-28-dr.-doctor", "topic-29-father-lord", "topic-30-money-business", "topic-31-alright-lt", "topic-32-sir-brother", "topic-33-school-class", "topic-34-vic-jax", "topic-35-gibbs-mcgee", "topic-36-monsieur-madame", "topic-37-baby-yo", "topic-38-agent-security", "topic-39-kill-dead", "topic-40-music-show", "topic-41-ofthe-thankyou", "topic-42-dude-cool", "topic-43-spanish-el", "topic-44-eat-nice", "topic-45-murder-killed", "topic-46-car-drive", "topic-47-town-horse", "topic-48-film-movie", "topic-49-woman-married"]

genre_features = [d for d in list(data.columns) if 'genre_' in d]

feats = audio_features1+genre_features+topics


def cem(target_feature, X, y):
	buckets=[]
	for i in range(2):
		buckets.append({})

	# keep track of counts -- we want to have the same distribution of the treatment within each bucket
	counts=np.zeros(2)

	# get the highest scoring topics for each movie
	argtopics=X[topics].idxmax(axis="columns")
	for i, row in X.iterrows():
		signature=[]
		signature.append(argtopics[i])

		# binarize the treatmenet variable (e.g., danceability)
		target_val=row[target_feature]
		if target_val > .5:
			target_val=int(1)
		else:
			target_val=int(0)

		counts[target_val]+=1

		# binarize the other audio features; genre features are already binary
		for feat in audio_features1:
			if feat == target_feature:
				continue
			val=row[feat]
			if val > .5:
				val=1
			else:
				val=0
			row[feat]=val
			signature.append(val)
		for feat in genre_features:
			signature.append(row[feat])
		sigstr=' '.join(str(x) for x in signature)

		# the feature values define the bucket this point is placed into
		if sigstr not in buckets[target_val]:
			buckets[target_val][sigstr]={}
		buckets[target_val][sigstr][i]=1

	matchedids={}
	f0=counts[0]/(counts[0]+counts[1])
	f1=1-f0

	for sigstring in buckets[0]:
		if sigstring in buckets[1]:

			# mininum of 5 points in each treatment condition within each bucket
			if len(buckets[0][sigstring]) < 5 or len(buckets[1][sigstring]) < 5:
				continue

			# subsample points in bucket to reflect overall distribution of treatment in overall data
			t0=len(buckets[0])*f0
			t1=len(buckets[1])*f1

			if t0 < 1 or t1 < 1:
				continue

			c=0
			for idd in buckets[0][sigstring]:
				matchedids[idd]=1
				c+=1
				if c >= t0:
					break
			c=0
			for idd in buckets[1][sigstring]:
				matchedids[idd]=1
				c+=1
				if c >= t1:
					break
			
	# return subset of matched data and regress on that
	return X.iloc[list(matchedids.keys())], y.iloc[list(matchedids.keys())]


def run_regression_cem(treatment_variable, features):
	X = data[features]
	y = data.averageRating

	X, y=cem(treatment_variable, X, y)
	X_with_bias_term = sm.add_constant(X)
	est = sm.OLS(y, X_with_bias_term)
	fit = est.fit()
	print(fit.summary())


def run_regression_statsmodels(features):
	X = data[features]
	y = data.averageRating

	X_with_bias_term = sm.add_constant(X)
	est = sm.OLS(y, X_with_bias_term)
	fit = est.fit()
	print(fit.summary())


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

run_regression_cem(treatment_variable, feats)
