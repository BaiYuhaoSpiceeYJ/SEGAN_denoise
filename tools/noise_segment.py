import optparse
import random
import librosa
import sys
import os


def main():
    usage="python noise_segment.py <noisy_wav_name> <output_dir>"
    parser=optparse.OptionParser(usage)
    parser.add_option('--min-time-length-ms', dest='min_time_length_ms', type=int, help='minimal length of segment', default=3000)
    parser.add_option('--overlap-time-length-ms', dest='overlap_time_length_ms', type=int, help='the overlap time of neighbor segment',default=1500)
    parser.add_option('--target-sample-rate', dest='target_sample_rate', type=int, help='the sample rate of the segment needed to save ', default=8000)
                
    options, args=parser.parse_args()
    sr = options.target_sample_rate
    window_size = sr // 1000 * options.min_time_length_ms
    overlap_size = sr // 1000 * options.overlap_time_length_ms
    wav_path = args[0]
    output_path = args[1]

    clean_data, _ = librosa.load(wav_path, sr=sr)

    segments = []
    end = False
    start_i = overlap_size
    while not end:
        start_i = start_i-overlap_size
        if (start_i+2*window_size > clean_data.shape[0]):
            end_i = clean_data.shape[0]
            end = True
        else:
            end_i = start_i+window_size
        segments.append(clean_data[start_i:end_i])
        start_i = end_i
    wav_name = os.path.basename(wav_path)
    wav_name = wav_name[0:wav_name.find(".wav")]
    dir_name = output_path+"/"+wav_name
    wav_prefix = dir_name+"/"+wav_name
    os.makedirs(dir_name)
    for i in range(len(segments)):
        librosa.output.write_wav(wav_prefix+"_"+str(i)+"_noisy.wav", segments[i], sr, norm=False)
if __name__ == "__main__":
    main()



