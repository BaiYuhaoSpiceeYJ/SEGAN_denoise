###将其中的MP3音频转为wav###
import glob
import os
import librosa
import time

noise_path = r'C:\Users\SpiceeYJ\Desktop\nn'
mp3_files = glob.glob(noise_path+ r'\*.mp3')

for mp3_file in mp3_files:
    filename = (mp3_file.split('\\')[-1]).split('.')[0]
    print(filename)
    x='ffmpeg -i {} -ar 8000 {}'.format(noise_path+'\\'+filename+'.mp3',noise_path+'\\'+filename+'.wav')
    os.system(r'{}'.format(x))
    y='del {}'.format(noise_path+'\\'+filename+'.mp3')
    os.system(r'{}'.format(y))

###将wav音频进行8k重采样###
noise_8k_path = noise_path + '-8k'
if not os.path.exists(noise_8k_path):
    os.mkdir(noise_8k_path)
wav_files = glob.glob(noise_path + r'\*.wav')

for wav_file in wav_files:
    filename = (wav_file.split('\\')[-1]).split('.')[0]
    print(filename)
    os.rename(noise_path + '\\' + filename + '.wav',
              noise_path + '\\' + (filename.split('(')[-1]).split(')')[0] + '.wav', )
    x = 'ffmpeg -i {} -ar 8000 {}'.format(noise_path + '\\' + (filename.split('(')[-1]).split(')')[0] + '.wav',
                                          noise_8k_path + '\\' + (filename.split('(')[-1]).split(')')[0] + '-8k.wav')
    os.system(r'{}'.format(x))

###将音频转成16bit位深度###
noise_8k_16bit_path = noise_8k_path + '-16bit'
if not os.path.exists(noise_8k_16bit_path):
    os.mkdir(noise_8k_16bit_path)
wav_files = glob.glob(noise_8k_path+ r'\*.wav')

for wav_file in wav_files:
    filename = (wav_file.split('\\')[-1]).split('.')[0]
    print(filename)
    x='sox {} -b 16 {}'.format(noise_8k_path+'\\'+filename+'.wav',noise_8k_16bit_path+'\\'+filename+'-16bit.wav')
    os.system(r'{}'.format(x))

###给噪音分段4s###
noise_8k_16bit_frame_path = noise_8k_16bit_path + '-frame2'
if not os.path.exists(noise_8k_16bit_frame_path):
    os.mkdir(noise_8k_16bit_frame_path)
wav_files = glob.glob(noise_8k_16bit_path + r'\*.wav')


def calculate_time(time):
    minu = time // 60
    sec = time % 60
    return minu, sec


for wav_file in wav_files:
    duration = librosa.get_duration(filename=wav_file)
    filename = (wav_file.split('\\')[-1]).split('.')[0]
    print(filename)

    if duration < 2:
        pass
    else:
        i = 0
        count = 0
        while duration - i > 4:
            start_min, start_sec = calculate_time(i)
            x = 'ffmpeg -i {} -ss 00:{}:{} -t 00:00:04 {}'.format(noise_8k_16bit_path + '\\' + filename + '.wav', \
                                                                  start_min, start_sec,
                                                                  noise_8k_16bit_frame_path + '\\' + filename + '-' + str(
                                                                      count) + '.wav')
            os.system(r'{}'.format(x))
            i += 1
            count += 1
        if duration - i < 2:
            pass
        else:
            left = round(duration - i)
            start_min, start_sec = calculate_time(i)
            x = 'ffmpeg -i {} -ss 00:{}:{} -t 00:00:{} {}'.format(noise_8k_16bit_path + '\\' + filename + '.wav', \
                                                                  start_min, start_sec, left,
                                                                  noise_8k_16bit_frame_path + '\\' + filename + '-' + str(
                                                                      count) + '.wav')
            os.system(r'{}'.format(x))