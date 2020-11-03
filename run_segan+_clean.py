import os
import librosa

CKPT_PATH="ckpt_segan+"

# please specify the path to your G model checkpoint
# as in weights_G-EOE_<iter>.ckpt
G_PRETRAINED_CKPT="weights_EOE_G-Generator-97616.ckpt"
#G_PRETRAINED_CKPT="weights_EOE_G-Generator-578881.ckpt"
# please specify the path to your folder containing
# noisy test files, each wav in there will be processed
TEST_FILES_PATH=r"C:\Users\SpiceeYJ\Desktop\t1"

# please specify the output folder where cleaned files
# will be saved
SAVE_PATH=r"C:\Users\SpiceeYJ\Desktop\test\t2"
#a,_ = librosa.load(r'C:\Users\SpiceeYJ\Desktop\test\airplane2-8k-16bit-1.wav',sr=None)#原音频
#librosa.output.write_wav(r'C:\Users\SpiceeYJ\Desktop\test\airplane2-8k-16bit-1.wav', a, 8000, norm=True)
x = r'python -u clean.py --g_pretrained_ckpt {}/{} --test_files {} --cfg_file {}/train.opts --synthesis_path {}'\
	.format(CKPT_PATH,G_PRETRAINED_CKPT,TEST_FILES_PATH,CKPT_PATH,SAVE_PATH)
os.system(x)