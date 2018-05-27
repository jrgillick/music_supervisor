import load_data, gzip, sys, numpy as np

def load_subtitle_text(path):
  return [l for l in gzip.open(path).read().split('\n') if '<' not in l and '>' not in l]

data = load_data.load_subtitle_paths()
rows = [row for index,row in data.iterrows()]

#'/data/jrgillick/clean_subtitles.txt'
# output all subtitles into one big file for loading - about 7G
with open('clean_subtitles.txt','wb') as f:
	for row in rows: 
		line = '\t'.join(load_subtitle_text(row.subtitle_path)) + '\n'
		movie_id = row.movie_id
		f.write(movie_id + '\t\t' + line)

