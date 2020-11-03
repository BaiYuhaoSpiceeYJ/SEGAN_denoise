import glob
import librosa
import os
import numpy as np
import optparse



def main():
#     workspace = r'C:/Users/SpiceeYJ/Desktop/1/**/*.wav'
#     output_dir = r'C:/Users/SpiceeYJ/Desktop/out/'
#     if not os.path.exists(output_dir):
#         os.mkdir(output_dir)
    usage="python segment.py <datatang_dir> <output_dir> <sr>"
    parser=optparse.OptionParser(usage)
    option, args=parser.parse_args()

    datatang_dir = args[0]
    output_dir = args[1]
    sr = int(args[2])
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
      

    wav_list = glob.glob(datatang_dir + '/**/*.wav', recursive=True)
    for wav in wav_list:
        print(wav)
        """handle .txt to get a segment list"""
        txt = '.'.join(wav.split('.')[:-1]) + '.txt'
        with open(txt, "r", encoding='utf-8') as f:
            Q1 = []
            Q2 = []
            Q3 = []
            Q4 = []
            for line in f.readlines():
                line = line.strip('\n') 
                Q1.append(line.split('\t')[0])
                Q2.append(line.split('\t')[1])
            Q1 = np.asarray(Q1,np.float32)
            Q2 = np.asarray(Q2,np.float32)
            assert len(Q1) == len(Q2)

            segment_list = []
            for i in range(len(Q1)-1):
                if i==0 and Q1[0]> 0:
                    segment_list.append([0,Q1[0]])
                if Q1[i+1] - Q2[i] > 0:
                    segment_list.append([Q2[i],Q1[i+1]])

        """segmentation of wave file"""
        basename = os.path.basename(wav)
        output_dir2 = output_dir + '/' + basename.split('.')[0]+'/'
        if not os.path.exists(output_dir2):
            os.mkdir(output_dir2)
        wav,_ = librosa.load(wav, sr=sr)
        idx = 0
        for segment in segment_list:
            wav_segment = wav[int(segment[0]*sr):int(segment[1]*sr)]
            output_name = output_dir2 + basename.split('.')[0] + '_' +str(idx) + '.wav'
            try:
                librosa.output.write_wav(output_name, wav_segment, sr, norm=True)
            except:
                librosa.output.write_wav(output_name, wav_segment, sr, norm=False)
            idx += 1
        
if __name__ == "__main__":
    main()
