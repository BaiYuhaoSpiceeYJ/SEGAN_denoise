#!/bin/bash
. path.sh

if [[ $# -ne 3 ]]; then
  echo "$0 <clean_root> <noise_root> <output_dir>"
fi

clean_root=$1
noise_root=$2
output_dir=$3

if [[ ! -e $output_dir ]]; then
    mkdir -p $output_dir
fi

if [[ ! -e $output_dir/clean ]]; then
    mkdir -p $output_dir/clean
fi

if [[ ! -e $output_dir/noise_segment ]]; then
    mkdir -p $output_dir/noise_segment
fi


resample.sh --concurrent-num 32 --sample-rate 8000 $clean_root $output_dir/clean

noisy_segment.sh --concurrent-num 32 --min-time-length-ms 5000 --overlap-time-length-ms 1500 \
                  --target-sample-rate 8000 $noise_root $output_dir/noise_segment

wav_noise_add.sh --concurrent-num 32 $output_dir/clean $output_dir/noise_segment $output_dir

python -u train.py --save_path ckpt_segan+ \
	--clean_trainset $output_dir/noisy_add_output/clean.scp \
	--noisy_trainset $output_dir/noisy_add_output/clean_add_noisy.scp \
	--cache_dir $output_dir/data_for_model_train --no_train_gen --batch_size 32 --no_bias
	#--clean_trainset $output_dir/clean
	#--noisy_trainset $output_dir/noisy_add_wav