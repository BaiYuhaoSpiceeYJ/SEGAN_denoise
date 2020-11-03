#!/bin/bash
#author: dj date: 2020.09.18

help_message="This script is designed to resample the wav from a given directory recursively, usage example: 
        $0  <noisy_dir> <output_dir> 
option param:
        --concurrent-num    :the concurrent number for adding noise parallelly
        --sample-rate   :the target sample rate 
note:  
        1) the directory parameter needs to be absolute path in case of unknown error"

sample_rate=8000
concurrent_num=1

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
    a=($line)

    resample_name=`echo $line | sed -r 's/.*\/(.*).wav/\1_resample.wav/'`
    resample_name=$output_dir/$resample_name
    if [[ ! -f $resample_name ]]; then
        echo "execute resample task: $line"
        ThreadPoolEnqueue python $SE/tools/resample.py --target-sample-rate $sample_rate ${a[*]} $resample_name >> $output_dir/log 2>&1
    else
        echo "already exist, pass resample task: $line"
    fi

done < $output_dir/noisy.list.tmp

ThreadPoolWaitFinish
rm $output_dir/*.tmp
echo "resample done!"






