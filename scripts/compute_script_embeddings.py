import sys
sys.path.insert(0, '../')
import vector_features

for i in tqdm(range(len(feats))):
	v = vector_features.VectorFeatures( [line.decode('utf-8') for line in feats[i].split('\t')[0:-1]] )
