import os

x = r"python -u train.py --save_path ckpt_segan+ --clean_trainset C:\Users\SpiceeYJ\Desktop\clean-8k --noisy_trainset C:\Users\SpiceeYJ\Desktop\added --cache_dir C:\Users\SpiceeYJ\Desktop\pkl_for_train --no_train_gen --batch_size 32 --no_bias"
os.system(x)
