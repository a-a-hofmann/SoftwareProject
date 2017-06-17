#!/bin/bash
while true
do
bandwidth=5
mbps="m"
echo -e "Running with $bandwidth$mbps mbps\n"
echo -e `iperf -c 10.0.0.6 -u -b $bandwidth$mbps -p $1`
echo -e "\n"

done
