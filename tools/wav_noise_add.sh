#!/bin/bash
#author: dj date: 2020.09.17

help_message="This script is designed to add noise to the given wavs, usage example: 
        $0 <clean_dir> <noise_dir> <output_dir> 
option param:
        --min-time-length-ms    :the concurrent number for adding noise parallelly
        --random-slide-ms   :when adding noise repeatly, we randomly increase [0, random_slide_size] time step from last time end
        --min-noise-level   :the minimal noisy level
        --max-noise-level   :the maximal noisy level
note:  
        1) the directory parameter need to be absolute path in case of unknown error"

random_slide_ms=1000
min_noise_level=0.2
max_noise_level=0.5
noisy_num=1  #the number of noisy wavs need to be added to the clean wav 
concurrent_num=1

. parse_options.sh
. thread_pool.sh
. path.sh

if [[ $# -ne 3 ]]; then
    echo "$0 <clean_dir> <noise_dir> <output_dir>"
    exit 1
fi

clean_dir=$1
noisy_dir=$2
output_dir=$3

noisy_output_dir=$output_dir/noisy_add_wav
output_dir=$output_dir/noisy_add_output

if [[ ! -e $output_dir ]]; then
    mkdir $output_dir
fi

if [[ ! -e $noisy_output_dir ]]; then
    mkdir $noisy_output_dir
fi

find $clean_dir -name "*.wav" > $output_dir/clean.list.tmp
cat $output_dir/clean.list.tmp | sed -r 's/.*\/(.*).wav/\1/g' > $output_dir/clean_keys.list.tmp
paste -d "\t" $output_dir/clean_keys.list.tmp $output_dir/clean.list.tmp > $output_dir/clean.scp
find $noisy_dir -name "*.wav" > $output_dir/noisy.list.tmp
cat $output_dir/noisy.list.tmp | sed -r 's/.*\/(.*).wav/\1/g' > $output_dir/noisy_keys.list.tmp
paste -d "\t" $output_dir/noisy_keys.list.tmp $output_dir/noisy.list.tmp  > $output_dir/noisy.scp
# rm $output_dir/*.tmp

N_clean=`wc -l $output_dir/clean.scp | cut -d ' ' -f 1 `
N_noisy=`wc -l $output_dir/noisy.scp | cut -d ' ' -f 1 `

batches=$(($N_clean/$N_noisy+1))

for i in `seq 1 $batches`
do 
    cat $output_dir/noisy.list.tmp >> $output_dir/noisy_ext.list.tmp
done

#generate clean_and_noisy.list.tmp, line format: clean_key clean_wav_path noisy_wav_path
#add multiple noisy wav
touch $output_dir/noisy_ext.list.ext.tmp 
for x in `seq 1 $noisy_num`
do
    shuf -n $N_clean $output_dir/noisy_ext.list.tmp > $output_dir/noisy_shuf.list.tmp
    paste -d "\t" $output_dir/noisy_ext.list.ext.tmp $output_dir/noisy_shuf.list.tmp > $output_dir/noisy_ext.list.ext.tmp
done
paste -d "\t" $output_dir/clean.scp $output_dir/noisy_ext.list.ext.tmp > $output_dir/clean_and_noisy.list.tmp

#generate clean_add_noisy.scp from clean_and_noisy.list.tmp, line format: clean_key  clean_add_noisy_wav_path
touch $temp_dir/clean_add_noisy.scp
ThreadPoolInit $concurrent_num
while read line
do
    a=($line)
    key=${a[0]}
    unset a[0]
    noisy_name=${noisy_output_dir}/${key}"_add_noisy.wav"
    if [[ ! -f $noisy_name ]]; then
        #printf "%s\t%s\n" ${key} ${noisy_name} >> $output_dir/clean_add_noisy.scp
        echo "execute add noise task: ${a[*]}"
        ThreadPoolEnqueue python $SE/tools/wav_noise_add.py \
                                --random-slide-ms $random_slide_ms \
                                --min-noise-level $min_noise_level \
                                --max-noise-level $max_noise_level \
                                ${a[*]} $noisy_name >> $output_dir/log 2>&1
    else
        echo "already exist, pass noise add task: ${a[*]}"
    fi

done < $output_dir/add_noisy.list.tmp
ThreadPoolWaitFinish

find $noisy_output_dir -name "*.wav" > $output_dir/clean_add_noisy.list.tmp
cat $output_dir/clean_add_noisy.list.tmp | sed -r 's/.*\/(.*).wav/\1/g' > $output_dir/clean_add_noisy_keys.list.tmp
paste -d "\t" $output_dir/clean_add_noisy_keys.list.tmp $output_dir/clean_add_noisy.list.tmp > $output_dir/clean_add_noisy.scp

sort $output_dir/clean_add_noisy.scp > $output_dir/clean_add_noisy.scp.tmp
sort $output_dir/clean.scp > $output_dir/clean.scp.tmp
rm $output_dir/clean_add_noisy.scp
rm $output_dir/clean.scp
mv $output_dir/clean_add_noisy.scp.tmp $output_dir/clean_add_noisy.scp
mv $output_dir/clean.scp.tmp $output_dir/clean.scp

rm $output_dir/*.tmp
echo "noise add done!"






