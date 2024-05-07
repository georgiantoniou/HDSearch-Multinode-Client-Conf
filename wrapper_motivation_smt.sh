#!/bin/bash

####################################################################################################
# This script is used as a wrapper to investigate whether performance of specific feautures of the
# server side are misinderpreted due to variabilities caused by the hardware configuration of the 
# client side. In thi script we examine SMT/noSMT with 2 client configurations DEFAULT and 
# C0 + governor Performance + Ticks. Total 4  experiments:
# 
# DEFAULT-S-SMT_ON: cstates-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# DEFAULT-S-SMT_OFF: cstates-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# C0-FG_PE-TICKS_ON-UNC_FIXED-S-SMT_ON: c0-on/intel-pstate-off/tickless-off/smt-on/turbo-on/uncore-fixed/core-performance/
# C0-FG_PE-TICKS_ON-UNC_FIXED-S-SMT_OFF: c0-on/intel-pstate-off/tickless-off/smt-on/turbo-on/uncore-fixed/core-performance/

# Create Result Dir
ssh ganton12@node0 "mkdir ~/data/hdsearch-motivation-smt"
cd ~/HDSearch-Multinode-Client-Conf/client-conf-scripts/

#### Exp1-2: Set Server Side SMT ON /SMTOFF client side Default: ####

## Client Side DEFAULT ##
~/HDSearch-Multinode-Client-Conf/client-conf-scripts/set-client-configuration.sh main 3101001 node0 ~/HDSearch-Multinode-Client-Conf/client-conf-scripts/ node0,~/data/hdsearch-motivation-smt/DEFAULT

# Make space for image to load
ssh ganton12@node0 "sudo ~/HDSearch-Multinode-Client-Conf/scripts/change-storage-location-docker.sh"

## Run experiment
ssh ganton12@node0 "cd ~/HDSearch-Multinode-Client-Conf/; nohup python3 ./run_experiment.py hdsearch-motivation-smt/DEFAULT >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

### Exp3-4: Set Server Side SMT ON/OFF client side C0-FG_PE-TICKS_ON-UNC_FIXED: ####

## Client Side C0-FG_PE-TICKS_ON-UNC_FIXED ##
~/HDSearch-Multinode-Client-Conf/client-conf-scripts/set-client-configuration.sh main 0001111 node0 ~/HDSearch-Multinode-Client-Conf/client-conf-scripts/ node0,~/data/hdsearch-motivation-smt/C0-FG_PE-TICKS_ON-UNC_FIXED

# Make space for image to load
ssh ganton12@node0 "sudo ~/HDSearch-Multinode-Client-Conf/scripts/change-storage-location-docker.sh"

## Run experiment
ssh ganton12@node0 "cd ~/HDSearch-Multinode-Client-Conf/; nohup python3 ./run_experiment.py hdsearch-motivation-smt/C0-FG_PE-TICKS_ON-UNC_FIXED >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done
