#!/bin/bash
#author: dj date: 2020.07.16



#################################################
####  thread pool implemention  begin  ##########

#init a thread pool with size param1. 
#example: thread_pool_init 3
ThreadPoolInit(){
    local N=$1
    local fifo="/tmp/$$.fifo"
    #creat a fifo pipeline
    mkfifo $fifo
    #creat a fd and bind it to fifo pipeline
    exec {FD}<>$fifo
    rm $fifo
    # creat concurrent positions 
    for i in $(seq $N); do
        echo >&$FD
    done    
}

#enqueue a task into threadpool
#example: ThreadPoolEnqueue func param1 param2 ...
ThreadPoolEnqueue(){
    _func=$1
    shift
    read -u $FD
    {
        $_func $*
        echo >&$FD
    }&
}

#wait all tasks in theadpool done and free threadpool
ThreadPoolWaitFinish(){
    wait
    exec {FD}>&-
}

####  thread pool implemention end  ##########
##############################################






###### test example ######

# test_fun(){
#     sleep 2
#     echo $1
# }
# ThreadPoolInit 3

# ThreadPoolEnqueue test_fun 1
# ThreadPoolEnqueue test_fun 2
# ThreadPoolEnqueue test_fun 3

# ThreadPoolWaitFinish

