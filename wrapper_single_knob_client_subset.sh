#!/bin/bash

####################################################################################################
# This script is used as a wrapper for the single knob experiments of the client configuration that
# appear to have great variability. 
# We assume server configuration remains the same and we just change the client configuration.
# Possible configurations are the following:
# DEFAULT: cstates-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# C1: c1-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# C0: c0-on/intel-pstate-on/tickless-off/smt-on/turbo-on/uncore-dynamic/core-powersave/
# IP_OFF: cstates-on/intel-pstate-off/tickless-off/smt-on/turbo-on/uncore-dynamic/core-ondemand/
# IP_OFF-FG_US: cstates-on/intel-pstate-off/tickless-on/smt-on/turbo-on/uncore-dynamic/core-userspace/
# IP_OFF-FG_PE: cstates-on/intel-pstate-off/tickless-on/smt-on/turbo-on/uncore-dynamic/core-performance/

# Create Result Dir
ssh ganton12@node0 "mkdir ~/data/hdsearch-client-single-knob-variability"

cd ~/HDSearch-Multinode-Client-Conf/client-conf-scripts/

#### Exp1: Set DEFAULT client configuration: ####
~/HDSearch-Multinode-Client-Conf/client-conf-scripts/set-client-configuration.sh main 3101001 node0 ~/HDSearch-Multinode-Client-Conf/client-conf-scripts/ node0,~/data/hdsearch-client-single-knob-variability/DEFAULT

# Run experiment

ssh ganton12@node0 "cd ~/HDSearch-Multinode-Client-Conf/; nohup python3 ./run_experiment.py hdsearch-client-single-knob-variability/DEFAULT >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp3: Set C1 client configuration: #### 

~/HDSearch-Multinode-Client-Conf/client-conf-scripts/set-client-configuration.sh main 1101001 node0 ~/HDSearch-Multinode-Client-Conf/client-conf-scripts/ node0,~/data/hdsearch-client-single-knob-variability/C1

# Run experiment

ssh ganton12@node0 "cd ~/HDSearch-Multinode-Client-Conf/; nohup python3 ./run_experiment.py hdsearch-client-single-knob-variability/C1 >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp4: Set C0 client configuration: #### 

~/HDSearch-Multinode-Client-Conf/client-conf-scripts/set-client-configuration.sh main 0101001 node0 ~/HDSearch-Multinode-Client-Conf/client-conf-scripts/ node0,~/data/hdsearch-client-single-knob-variability/C0

# Run experiment

ssh ganton12@node0 "cd ~/HDSearch-Multinode-Client-Conf/; nohup python3 ./run_experiment.py hdsearch-client-single-knob-variability/C0 >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp5: Set IP_OFF client configuration: #### 

~/HDSearch-Multinode-Client-Conf/client-conf-scripts/set-client-configuration.sh main 3001301 node0 ~/HDSearch-Multinode-Client-Conf/client-conf-scripts/ node0,~/data/hdsearch-client-single-knob-variability/IP_OFF

# Run experiment

ssh ganton12@node0 "cd ~/HDSearch-Multinode-Client-Conf/; nohup python3 ./run_experiment.py hdsearch-client-single-knob-variability/IP_OFF >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp10: Set IP_OFF-FG_US client configuration: #### 

~/HDSearch-Multinode-Client-Conf/client-conf-scripts/set-client-configuration.sh main 3001201 node0 ~/HDSearch-Multinode-Client-Conf/client-conf-scripts/ node0,~/data/hdsearch-client-single-knob-variability/IP_OFF-FG_US

# Run experiment

ssh ganton12@node0 "cd ~/HDSearch-Multinode-Client-Conf/; nohup python3 ./run_experiment.py hdsearch-client-single-knob-variability/IP_OFF-FG_US >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done

#### Exp11: Set IP_OFF-FG_PE client configuration: #### 

~/HDSearch-Multinode-Client-Conf/client-conf-scripts/set-client-configuration.sh main 3001101 node0 ~/HDSearch-Multinode-Client-Conf/client-conf-scripts/ node0,~/data/hdsearch-client-single-knob-variability/IP_OFF-FG_PE

# Run experiment

ssh ganton12@node0 "cd ~/HDSearch-Multinode-Client-Conf/; nohup python3 ./run_experiment.py hdsearch-client-single-knob-variability/IP_OFF-FG_PE >> ~/nohup.out 2>&1 &"

sleep 105m

while [[ `ssh ganton12@node0 "ps aux | grep run_experiment | wc -l"` -gt 2 ]]; 
do

    sleep 5m

done