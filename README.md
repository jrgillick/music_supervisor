# Music Supervisor

This repository contains code and data for the experiments in our paper:

Jon Gillick and David Bamman, "Telling Stories with Soundtracks: An Empirical Analysis of Music in Film ", NAACL 2018 Storytelling Workshop. Please cite this paper if you use the code.

#### To run the experiments yourself, first follow these instructions for downloading additional data.

1. Download the Opensubtitles 2016 data (http://opus.nlpl.eu/OpenSubtitles2016.php) into the root directory of this repo (if you want to put it somewhere else, you'll need to edit load_data.py to change a default path).

2. Use the Spotify API (https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/)  to download the audio features for all the track ID's listed in data/spotify_ids.txt. Store the results as .json files in the data/audio_info folder. This folder should have about 96K files with names like 1m4P7RuceKALPVRaX0ZqeN.json.

3. Run parse_subtitles.py to put all the relevant data from OpenSubtitles into one text file for easy loading. This script uses the paths in data/imdb.subtitles.paths, so if you have an error, check to make sure those paths match the path of the OpenSubtitles data on your machine.

4. The run_regression scripts should now be able to load all the data using load_data.py. If you have any errors, check the default paths in the load_data python script. 
