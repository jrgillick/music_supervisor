import os, json, pandas as pd, numpy as np
from tqdm import tqdm

def get_subtitle_path(movie_id):
	return np.array(subtitle_paths[subtitle_paths['movie_id'] == movie_id])[0][1]

def load_subtitle_paths():
	return pd.read_table('/data/corpora/soundtracks/imdb.subtitles.first_paths',sep='\t',header=None,names=['movie_id','subtitle_path'])

def load_subtitles():
	lines = [{'movie_id': l.split('\t\t')[0], 'script': l.split('\t\t')[1]} for l in tqdm(open('/data/corpora/soundtracks/clean_subtitles.txt').read().split('\n')[0:-1])]
	return pd.DataFrame(lines)

def load_audio_info(path):
	h = json.load(open(path))
	soundtrack_id = path.split('.json')[0].split('/')[-1]
	h['soundtrack_id'] = soundtrack_id
	return h

def load_audio_features():
	root_audio_path = '/data/corpora/soundtracks/audio_info/'
	all_audio_paths = [root_audio_path + f for f in os.listdir(root_audio_path)]
	infos = [load_audio_info(p) for p in tqdm(all_audio_paths)]
	return pd.DataFrame(infos)

def load_soundtracks(path='/data/corpora/soundtracks/imdb.soundtracks.txt'):
	lines = [l.split('\t') for l in open('/data/corpora/soundtracks/imdb.soundtracks.txt').read().split('\n')][0:-1]
	return [{'movie_id': l[0], 'soundtrack_ids': l[1]} for l in lines]

def load_flat_soundtracks():
	tracks = load_soundtracks()
	flat_tracks = []
	for t in tracks:
		movie_id = t['movie_id']
		for soundtrack_id in t['soundtrack_ids'].split(' '):
			flat_tracks.append([movie_id, soundtrack_id])
	df = pd.DataFrame(flat_tracks,columns=['movie_id','soundtrack_id'])
	return df

def get_audio_features(data, soundtrack_id):
	audio_features = ['acousticness','danceability','duration_ms','energy','instrumentalness','key','liveness','loudness','mode','speechiness','tempo','time_signature','valence']
	return np.array(data[data['soundtrack_id']=='6aNwvrNOT6NmcxWTHlVFSC'][audio_features])[0]

# load metadata from imdb dump of title.basics.tsv.gz
def load_titles_basic_metadata(path = '/data/corpora/imdb/title.basics.tsv'):
  return pd.read_csv(path,sep='\t')

def load_data_with_metadata():
  data = load_data()
  titles_metadata = load_titles_basic_metadata()
  return data.merge(titles_metadata,left_on='movie_id',right_on='tconst',how='left')

def load_data():
	data = load_flat_soundtracks().merge(load_subtitle_paths()).merge(load_audio_features())
	subtitles = load_subtitles()
	data.reset_index(inplace=True)
	subtitles.reset_index(inplace=True)
	data = data.merge(subtitles)
  return data
