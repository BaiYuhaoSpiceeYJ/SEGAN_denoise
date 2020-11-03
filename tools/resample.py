import optparse
import random
import librosa
import sys
import os
import scipy.io.wavfile as wavfile
import numpy as np


def main():
    usage="python resample.py <noisy_wav_name> <output_path>"
    parser=optparse.OptionParser(usage)
    parser.add_option('--target-sample-rate', dest='target_sample_rate', type=int, help='the sample rate of the segment needed to save ', default=8000)         
    options, args=parser.parse_args()
    sr = options.target_sample_rate
    wav_path = args[0]
    output_path = args[1]
    clean_data, _ = librosa.load(wav_path, sr=sr)
    #librosa.output.write_wav(output_path, clean_data, sr, norm=True)
    wavfile.write(output_path, sr, np.array(clean_data * 2 ** 15, np.int16))

if __name__ == "__main__":
    main()



