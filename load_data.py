import os, json, pandas as pd, numpy as np
from tqdm import tqdm

def load_subtitle_paths():
	return pd.read_table('/data/corpora/soundtracks/imdb.subtitles.first_paths',sep='\t',header=None,names=['movie_id','subtitle_path'])

def load_subtitles():
	print "Loading subtitles..."
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
	print "Loading audio features..."
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

# load metadata from imdb dump of title.basics.tsv.gz
def load_titles_basic_metadata(path = '/data/corpora/imdb/title.basics.tsv'):
  return pd.read_csv(path,sep='\t',low_memory=False)


def add_metadata_to_data(data):
	titles_metadata = load_titles_basic_metadata()
	data = data.merge(titles_metadata,left_on='movie_id',right_on='tconst',how='inner')
	all_genres = list(set(np.concatenate([g.split(',') for g in list(data.genres)])))
	genre_list = []
	print "Loading metadata..."
	for i in tqdm(range(len(data))):
		h = {}
		row_genres = ['genre_' + g for g in data.genres[i].split(',')]
		for r in row_genres:
			h[r] = 1
		genre_list.append(h)
	genre_df = pd.DataFrame(genre_list)
	genre_df.fillna(0,inplace=True)
	data.reset_index(inplace=True)
	genre_df.reset_index(inplace=True)
	return data.merge(genre_df)

def pad_id(m):
	if len(m) == 9:
		return m
	else:
		prefix = 'tt'
		suffix = m.split(prefix)[-1]
		pad_length = 7-len(suffix)
		pad_str = ''.join(list(np.zeros(pad_length).astype(np.int32).astype(str)))
		return prefix+pad_str+suffix

def fix_movie_ids(data):
	movie_ids = data.movie_id
	movie_ids = [pad_id(m) for m in movie_ids]
	data.movie_id = movie_ids
	return data

def load_ratings(path='/data/corpora/imdb/title.ratings.tsv'):
	return pd.read_csv(path,sep='\t')

def load_titles_tm(path = '/data/corpora/imdb/tm/topics.50.txt'):
  return pd.read_csv(path,sep='\t',low_memory=False)


def load_data():
	data = load_flat_soundtracks().merge(load_subtitle_paths()).merge(load_audio_features())
	subtitles = load_subtitles()
	data.reset_index(inplace=True)
	subtitles.reset_index(inplace=True)
	data = data.merge(subtitles)
	data = fix_movie_ids(data)
	data = data.merge(load_ratings(),left_on='movie_id',right_on='tconst')
	data = data.merge(load_titles_tm(),left_on='movie_id',right_on='tconst')
	data = add_metadata_to_data(data)
	return data
