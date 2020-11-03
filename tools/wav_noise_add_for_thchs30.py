import optparse
import random
import librosa
import sys
import numpy as np
import glob
from tqdm import tqdm


def wav_noise_add_single(clean_name, noise_name, output_name):

    clean_data, clean_sr = librosa.load(clean_name, sr=8000)
    noise_data, noise_sr = librosa.load(noise_name, sr=8000)

    max_length = np.maximum(clean_data.shape[0], noise_data.shape[0])

    clean_data = np.pad(clean_data, (0, max_length - clean_data.shape[0]), constant_values=0)
    noise_data = np.pad(noise_data, (0, max_length - noise_data.shape[0]), constant_values=0)

    added_data = clean_data + noise_data * np.random.uniform(0.2, 0.55)

    librosa.output.write_wav(output_name, added_data, clean_sr, norm=True)


def wav_add_white_noise(clean_name, output_name):

    clean_data, clean_sr = librosa.load(clean_name, sr=8000)
    clean_data = clean_data + np.random.uniform(0.0, 0.6) * np.random.normal(0, 0.04, len(clean_data))
    librosa.output.write_wav(output_name, clean_data, clean_sr, norm=True)

def wav_add_pink_noise(clean_name, output_name):

    clean_data, clean_sr = librosa.load(clean_name, sr=8000)
    clean_data = clean_data + np.random.uniform(0.0, 0.6) * np.random.uniform(-0.08, 0.08, len(clean_data))
    librosa.output.write_wav(output_name, clean_data, clean_sr, norm=True)


if __name__ == "__main__":
    clean_dir = r'C:\Users\SpiceeYJ\Desktop\clean-8k'
    noise_dir = r'C:\Users\SpiceeYJ\Desktop\noise-8k-16bit-frame'
    output_dir = r'C:\Users\SpiceeYJ\Desktop\added'

    clean_list = np.array(list(glob.glob(clean_dir+r'\*.wav')), dtype=str)
    noise_list = np.array(list(glob.glob(noise_dir+r'\*.wav')), dtype=str)

    for i in tqdm(range(len(clean_list))):
        rand = np.random.rand(1)[0]
        if i % len(noise_list) == 0:
            noise_list = noise_list[np.random.permutation(len(noise_list))]
            print('shuffle noise data')
        output_name = output_dir+r'\noise_added_'+clean_list[i].split('\\')[-1]
        if 0 <= rand < 0.8:
            wav_noise_add_single(clean_list[i], noise_list[i % len(noise_list)], output_name)
        elif 0.8 <= rand < 0.9:
            wav_add_white_noise(clean_list[i], output_name)
        else:
            wav_add_pink_noise(clean_list[i], output_name)

