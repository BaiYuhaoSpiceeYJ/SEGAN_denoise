import optparse
import random
import librosa
import numpy as np
from scipy.io import wavfile
import sys
import os


def main():
    usage="python wav_noise_add.py [<options>] <clean.wav> <noise1.wav> [<noise2.wav>...] <output_name>"
    parser=optparse.OptionParser(usage)
    parser.add_option('--start-time-ms', dest='start_time_ms', type=int, help='start time', default=0)
    parser.add_option('--random-slide-ms', dest='random_slide_ms',type=int, \
                            help='when adding noise repeatly, we randomly increase [0, random_slide_size] time step from last time end', \
                            default=1000)
    parser.add_option('--min-noise-size-ms', dest='min_noise_size_ms',type=int, \
                            help='when cur-clean-data length is less than min_noise_size, we ignore it', \
                            default=1500)
    parser.add_option('--min-noise-level', dest='min_noise_level',type=float, \
                            default=0.2)
    parser.add_option('--max-noise-level', dest='max_noise_level',type=float, \
                            default=0.5)
    options, args=parser.parse_args()

    assert len(args)>=3
    clean_name = args[0]
    output_name = args[-1]
    del args[0]
    del args[-1]

    # print(options.start_time_ms)
    # print(options.random_slide_ms)
    # print(options.min_noise_size_ms)
    # print(options.max_noise_level)
    # print(options.min_noise_level)

    print(clean_name)
    print(args)
    clean_data, clean_sr = librosa.load(clean_name, sr=8000)

    noise_datas_srs = [librosa.load(noise_name, sr=8000) for noise_name in args]

    noise_datas = [x[0] for x in noise_datas_srs]

    random.shuffle(noise_datas)
    srs = [x[1] for x in noise_datas_srs]
    srs.append(clean_sr)
    
    for i in range(len(srs)-1):
        assert srs[i] == srs[i+1]

    start_i = int(clean_sr // 1000 * options.start_time_ms)

    rand = np.random.rand(1)[0]
    if 0 <= rand < 0.05:
        clean_data = clean_data + np.random.uniform(0.0, 0.4) * np.random.normal(0, 0.04, len(clean_data))
    elif 0.05 <= rand < 0.1:
        clean_data = clean_data + np.random.uniform(0.0, 0.4) * np.random.uniform(-0.08, 0.08, len(clean_data))
    else:
        end = False
        while not end:
            for y in noise_datas:
                start_i = int(start_i + clean_sr // 1000 * options.random_slide_ms * random.random())
                if int(start_i + clean_sr // 1000 * options.min_noise_size_ms) > clean_data.shape[0] :
                    end = True
                    break
                end_i = min(start_i+y.shape[0], clean_data.shape[0])
                # print(start_i)
                # print(end_i)
                level = options.min_noise_level + (options.max_noise_level - options.min_noise_level) * random.random()

                # print(level)
                clean_data[start_i:end_i] = clean_data[start_i:end_i] \
                                            + level * y[0:end_i-start_i]

                start_i = end_i

    #wavfile.write(output_name, clean_sr, np.array(clean_data * 2 ** 15, np.int16))
    librosa.output.write_wav(output_name, clean_data, clean_sr, norm=True)
if __name__ == "__main__":
    main()



