# Eliza Giane
# Ben Toker
# Sep 3,2025

import librosa
import numpy as np

KEYS = 'C C# D D# E F F# G G# A A# B'.split()

class Track:
    def __init__(self, audiofile):
        self.id = audiofile
        # with librosa:
        self.tempo = None
        self.key = None
        self.mode = None
        self.time_sig = None
        self.loudness = None
        self.duration = None
        # with essentia (tbd):
        self.energy = None
        self.acousticness = None
        self.danceability = None
        self.instrumentalness = None
        self.speechiness = None
        self.valence = None


    def extract_tempo(self, y, sr):
        """Extract tempo in BPM"""
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        self.tempo = float(tempo.item())
    
    def extract_chroma(self, y, sr):
        """Extract musical key (0-11) and mode (0: minor, 1: major)"""  
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        
        # sum chroma across time to get key profile
        key_profile = np.sum(chroma, axis=1)
        key_profile = key_profile / np.sum(key_profile)  # normalize
        
        # Krumhansl-Schmuckler key profiles
        major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 
                                 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 
                                 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
        
        # normalize profiles
        major_profile = major_profile / np.sum(major_profile)
        minor_profile = minor_profile / np.sum(minor_profile)
        
        # find best key by correlation
        best_key = 0
        best_mode = 1
        max_correlation = -1
        
        for key_shift in range(12):
            # shift profiles to test different keys
            shifted_major = np.roll(major_profile, key_shift)
            shifted_minor = np.roll(minor_profile, key_shift)
            
            # calculate correlations
            major_corr = np.corrcoef(key_profile, shifted_major)[0, 1]
            minor_corr = np.corrcoef(key_profile, shifted_minor)[0, 1]
            
            # check if this is the best match
            if major_corr > max_correlation:
                max_correlation = major_corr
                best_key = key_shift
                best_mode = 1 
            
            if minor_corr > max_correlation:
                max_correlation = minor_corr
                best_key = key_shift
                best_mode = 0 
        
        self.key = best_key
        self.mode = best_mode

    def extract_time_signature(self, y, sr):
        """Extract time signature (simplified: 3 or 4)"""
        # 3/4: every 3rd beat is be stronger
        # 4/4: every 4th beat (sometimes 2nd) is be stronger

        tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
        
        if len(beats) < 8:
            self.time_sig = 4  # default to 4/4
            return
        
        # convert beat frames to time
        beat_times = librosa.frames_to_time(beats, sr=sr)
        beat_intervals = np.diff(beat_times)
        
        # look at beat strength patterns to infer time signature
        onset_envelope = librosa.onset.onset_strength(y=y, sr=sr)
        
        # downsample to beat rate
        beat_strength = []
        for i in range(len(beats)-1):
            start_frame = beats[i]
            end_frame = beats[i+1]
            avg_strength = np.mean(onset_envelope[start_frame:end_frame])
            beat_strength.append(avg_strength)
        
        if len(beat_strength) < 6:
            self.time_sig = 4
            return
        
        # check periodicity
        autocorr = np.correlate(beat_strength, beat_strength, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        if len(autocorr) > 4:
            # check if there's stronger correlation at lag 3 vs lag 4
            corr_3 = autocorr[3] if len(autocorr) > 3 else 0
            corr_4 = autocorr[4] if len(autocorr) > 4 else 0
            
            self.time_sig = 3 if corr_3 > corr_4 * 1.2 else 4
        else:
            self.time_sig = 4

    def extract_loudness(self, y, sr):
        """Extract loudness in dB"""
        # RMS energy
        rms = np.sqrt(np.mean(y**2))
        
        # convert to dB
        if rms > 0:
            loudness_db = 20 * np.log10(rms)
        else:
            loudness_db = -60  # Very quiet
        
        self.loudness = float(loudness_db)

    def extract_duration(self, y, sr):
        """Extract duration in seconds"""
        duration_seconds = len(y) / sr
        self.duration = float(duration_seconds)


    def extract_basic_features(self):
        """Extract all audio features using librosa"""
        print(f"\nAnalyzing: {self.id}")
        
        # load audio file
        y, sr = librosa.load(self.id)
        print("loaded")
        
        # extract each feature
        self.extract_tempo(y, sr)
        print("tempo done")

        self.extract_chroma(y, sr)
        print("key and mode done")

        self.extract_time_signature(y, sr)
        print("time signature done")

        self.extract_loudness(y, sr)
        print("loudness done")

        self.extract_duration(y, sr)
        print("duration done")

        print("Extraction complete!")

    def print_features(self):
        print(f"\nFeatures for: {self.id}")
        print(f"Tempo: {self.tempo:.1f} BPM")
        print(f"Key: {KEYS[self.key]}")
        print(f"Mode: {'Minor' if self.mode == 0 else 'Major'}")
        print(f"Time Signature: {self.time_sig}/4")
        print(f"Loudness: {self.loudness:.1f} dB")
        print(f"Duration: {self.duration:.1f} seconds")
        print()
