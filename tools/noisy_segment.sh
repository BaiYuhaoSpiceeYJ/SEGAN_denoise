#!/bin/bash
#author: dj date: 2020.09.17

help_message="This script is designed to segment wav file to smaller length wav files, usage example: 
        $0  <noisy_dir> <output_dir> 
option param:
        --concurrent-num    :the concurrent number for adding noise parallelly
        --min-time-length-ms    :minimal length of segment
        --overlap-time-length-ms   :the overlap time of neighbor segment
        --target-sample-rate   :the sample rate of the segment needed to save
note:  
        1) the directory parameter need to be absolute path in case of unknown error"


concurrent_num=1
min_time_length_ms=3000
overlap_time_length_ms=1500
target_sample_rate=8000

. parse_options.sh
. thread_pool.sh
. path.sh

if [[ $# -ne 2 ]]; then
    echo "$0  <noisy_dir> <output_dir> "
    exit 1
fi


noisy_dir=$1
output_dir=$2

if [[ ! -e $output_dir ]]; then
    mkdir -p $output_dir
fi

find $noisy_dir -name "*.wav" > $output_dir/noisy.list.tmp

ThreadPoolInit $concurrent_num
while read line
do
    a=($line) #../noise/wind9.wav
    name_wav=`echo $line | awk 'BEGIN{FS="/"}{print $NF}'`#wind9.wav
    name=`echo $name_wav | awk 'BEGIN{FS="."}{print $1}'`#wind9

    if [[ ! -d $output_dir/$name]]; then
        printf "execute segmentation task: %s\n" $line
        ThreadPoolEnqueue python $SE/tools/noise_segment.py ${a[*]} $output_dir >> $output_dir/log 2>&1
    else
        echo "already exist, pass noise segment task: $line"
    fi

done < $output_dir/noisy.list.tmp
ThreadPoolWaitFinish
rm $output_dir/*.tmp
echo "noise segmentation done!"






