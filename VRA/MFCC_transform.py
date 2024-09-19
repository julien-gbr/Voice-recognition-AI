import matplotlib.pyplot as plt
import librosa
import librosa.display
import os
import numpy as np
import pandas as pd

input_dir = "Clean_files"
output_dir = "MFCC_data"

features = []
labels = []

def mfcc_extract(input_file):
    y, sr = librosa.load(input_file, sr=16000)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfccs_mean = np.mean(mfccs.T, axis=0)
    return mfccs_mean

for root, dirs, files in os.walk(input_dir):
    for file in files:
        if file.lower().endswith('.wav'):
            file_path = os.path.join(root, file)

            label = os.path.basename(root)

            mfccs = mfcc_extract(file_path)
            features.append(mfccs)
            labels.append(label)

df = pd.DataFrame(features)
df['label'] = labels

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file_path = os.path.join(output_dir, 'dataset.csv')

df.to_csv(output_file_path, index=False)
