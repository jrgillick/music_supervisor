# table 1
python regress_topics_on_audio.py danceability > topic_on_danceability.results.txt
python regress_topics_on_audio.py mode > topic_on_mode.results.txt
python regress_topics_on_audio.py tempo > topic_on_tempo.results.txt
python regress_topics_on_audio.py acousticness > topic_on_acousticness.results.txt
python regress_topics_on_audio.py instrumentalness > topic_on_instrumentalness.results.txt

# table 2
python regress_topic_audio_genre_on_rating.py danceability > danceability.results.txt
python regress_topic_audio_genre_on_rating.py mode >  .results.txt
python regress_topic_audio_genre_on_rating.py tempo > tempo.results.txt
python regress_topic_audio_genre_on_rating.py acousticness > acousticness.results.txt
python regress_topic_audio_genre_on_rating.py instrumentalness > instrumentalness.results.txt

