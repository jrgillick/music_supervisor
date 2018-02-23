import featurize, load_data
from tqdm import tqdm

data = load_data.load_data()

rows = [row for index,row in tqdm(data.iterrows())]

with open('/data/jrgillick/clean_subtitles.txt','wb') as f:
	for row in tqdm(rows): 
		line = '\t'.join(featurize.load_subtitle_text(row.subtitle_path)) + '\n'
		movie_id = row.movie_id
		f.write(movie_id + '\t\t' + line)

