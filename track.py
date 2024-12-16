# Eliza Giane
# Ben Toker
# Dec 15,2024

# this file contains the Track class used to create objects that store information about a certain tracck

class Track:
    def __init__(self,acousticness,analysis_url,danceability,duration_ms,energy,id,instrumentalness,key, liveness, loudness, mode, speechiness, tempo, time_sig, track_href, track_type, uri, valence):
        self.acousticness = acousticness
        self.analysis_url = analysis_url
        self.danceability = danceability
        self.duration_ms = duration_ms
        self.energy = energy
        self.id = id
        self.instrumentalness = instrumentalness
        self.key = key
        self.liveness = liveness 
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness 
        self.tempo = tempo
        self.time_sig = time_sig
        self.track_href = track_href
        self.track_type = track_type
        self.uri = uri
        self.valence = valence



'''
received by spotify API:
{
  "acousticness": 0.00242,
  "analysis_url": "https://api.spotify.com/v1/audio-analysis/2takcwOaAZWiXQijPHIx7B",
  "danceability": 0.585,
  "duration_ms": 237040,
  "energy": 0.842,
  "id": "2takcwOaAZWiXQijPHIx7B",
  "instrumentalness": 0.00686,
  "key": 9,
  "liveness": 0.0866,
  "loudness": -5.883,
  "mode": 0,
  "speechiness": 0.0556,
  "tempo": 118.211,
  "time_signature": 4,
  "track_href": "https://api.spotify.com/v1/tracks/2takcwOaAZWiXQijPHIx7B",
  "type": "audio_features",
  "uri": "spotify:track:2takcwOaAZWiXQijPHIx7B",
  "valence": 0.428
}
'''