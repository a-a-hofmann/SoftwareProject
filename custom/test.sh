#!/bin/bash
#for((i = 0; i <= 100; i++))

while true
do
time=$(($RANDOM%5 + 1))
pause=$(($RANDOM%5 + 1))

bandwidth=$(($RANDOM%2 + 1))
mbps="m"
printf "Running with $bandwidth$mbps mbps\n"
echo `iperf -c 10.0.0.6 -u -b $bandwidth$mbps -t $time -p $1`
printf "\n"
sleep $pause

done