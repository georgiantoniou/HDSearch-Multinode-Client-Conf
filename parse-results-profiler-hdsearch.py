import os
import pandas as pd
import json
import statistics
import csv 
import sys
import math
import re

#Need to Check confidence interval theory

qps_list = [500, 1000, 2000, 4000]
z=1.96 # from taming performance variability paper
n=0

def print_all_metrics(stats_dir, overall_raw_measurements, overall_statistics, filename):

    header = ["exp_name","configuration","qps", "metric", "avg", "median", "stdev", "cv", "ci-min", "ci-max"]
   
    for exp_name in overall_raw_measurements:
        for conf_list in overall_raw_measurements[exp_name]:
            for id,conf in enumerate(list(conf_list.keys())):
                for qps in qps_list:
                    for metric in overall_raw_measurements[exp_name][id][conf][qps]:
                        size = len(overall_raw_measurements[exp_name][id][conf][qps][metric])
                        break
                    break
                break
            break
        break
    
    for i in range(0,size):
        header.append("M" + str(i+1))
   
    filename = os.path.join(stats_dir, filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)

        for exp_name in overall_raw_measurements:
            for conf_list in overall_raw_measurements[exp_name]:
                for id,conf in enumerate(list(conf_list.keys())):
                    for metric in overall_statistics[exp_name][id][conf][qps_list[0]]:
                        for qps in qps_list:
                            row = []
                            row.append(exp_name)
                            row.append(conf)
                            row.append(qps)
                            row.append(metric)
                            row.append(overall_statistics[exp_name][id][conf][qps][metric]["avg"])
                            row.append(overall_statistics[exp_name][id][conf][qps][metric]["median"])
                            row.append(overall_statistics[exp_name][id][conf][qps][metric]["stdev"])
                            row.append(overall_statistics[exp_name][id][conf][qps][metric]["cv"])
                            row.append(overall_statistics[exp_name][id][conf][qps][metric]["ci"]["min"])
                            row.append(overall_statistics[exp_name][id][conf][qps][metric]["ci"]["max"])
                            for meas in overall_raw_measurements[exp_name][id][conf][qps][metric]:
                                row.append(meas)
                            
                            writer.writerow(row)

def print_residency_merged(stats_dir, overall_raw_measurements, overall_statistics, metric, filename):
    header = ["exp_name","configuration","qps", "metric", "C0", "C1", "C1E", "C6"]
      
    filename = os.path.join(stats_dir, filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)

    # Print Bucket Statistics

        for exp_name in overall_raw_measurements:
            for conf_list in overall_raw_measurements[exp_name]:
                for id,conf in enumerate(list(conf_list.keys())):
                    for qps in qps_list:
                        row = []
                        row.append(exp_name)
                        row.append(conf)
                        row.append(qps)
                        row.append(metric)
                        row.append(overall_statistics[exp_name][id][conf][qps]['bucket-C0-res']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['bucket-C1-res']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['bucket-C1E-res']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['bucket-C6-res']["avg"])
                        writer.writerow(row)
    
    # Print Midtier Statistics

        for exp_name in overall_raw_measurements:
            for conf_list in overall_raw_measurements[exp_name]:
                for id,conf in enumerate(list(conf_list.keys())):
                    for qps in qps_list:
                        row = []
                        row.append(exp_name)
                        row.append(conf)
                        row.append(qps)
                        row.append(metric)
                        row.append(overall_statistics[exp_name][id][conf][qps]['midtier-C0-res']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['midtier-C1-res']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['midtier-C1E-res']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['midtier-C6-res']["avg"])
                        writer.writerow(row)
    

def print_transition_merged(stats_dir, overall_raw_measurements, overall_statistics, metric, filename):
    
    header = ["exp_name","configuration","qps", "metric", "C0", "C1", "C1E", "C6"]

    filename = os.path.join(stats_dir, filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)

        for exp_name in overall_raw_measurements:
            for conf_list in overall_raw_measurements[exp_name]:
                for id,conf in enumerate(list(conf_list.keys())):
                    for qps in qps_list:
                        row = []
                        row.append(exp_name)
                        row.append(conf)
                        row.append(qps)
                        row.append(metric)
                        row.append(overall_statistics[exp_name][id][conf][qps]['bucket-C0-tr']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['bucket-C1-tr']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['bucket-C1E-tr']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['bucket-C6-tr']["avg"])
                        writer.writerow(row)
        
        # Midtier

        for exp_name in overall_raw_measurements:
            for conf_list in overall_raw_measurements[exp_name]:
                for id,conf in enumerate(list(conf_list.keys())):
                    for qps in qps_list:
                        row = []
                        row.append(exp_name)
                        row.append(conf)
                        row.append(qps)
                        row.append(metric)
                        row.append(overall_statistics[exp_name][id][conf][qps]['midtier-C0-tr']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['midtier-C1-tr']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['midtier-C1E-tr']["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps]['midtier-C6-tr']["avg"])
                        writer.writerow(row)

def print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, metric, filename):

    header = ["exp_name","configuration","qps", "metric", "avg", "median", "stdev", "cv", "ci-min", "ci-max"]
   
    for exp_name in overall_raw_measurements:
        for conf_list in overall_raw_measurements[exp_name]:
            for id,conf in enumerate(list(conf_list.keys())):
                for qps in qps_list:
                    size = len(overall_raw_measurements[exp_name][id][conf][qps][metric])
                break
            break
        break
    
    for i in range(0,size):
        header.append("M" + str(i+1))
   
    filename = os.path.join(stats_dir, filename)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)

        for exp_name in overall_raw_measurements:
            for conf_list in overall_raw_measurements[exp_name]:
                for id,conf in enumerate(list(conf_list.keys())):
                    for qps in qps_list:
                        row = []
                        row.append(exp_name)
                        row.append(conf)
                        row.append(qps)
                        row.append(metric)
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["avg"])
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["median"])
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["stdev"])
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["cv"])
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["ci"]["min"])
                        row.append(overall_statistics[exp_name][id][conf][qps][metric]["ci"]["max"])
                        for meas in overall_raw_measurements[exp_name][id][conf][qps][metric]:
                            row.append(meas)
                        
                        writer.writerow(row)

def confidence_interval_mean (metric_measurements):
    temp_list  = metric_measurements.copy()
    temp_list.sort()
     
    min_i = math.floor((n-z*math.sqrt(n)) / 2)
    max_i = math.ceil(1 + (n+z*math.sqrt(n)) / 2) 
    return temp_list[min_i+1-1], temp_list[max_i-1]

def coefficient_of_variation(metric_measurements):
    return statistics.stdev(metric_measurements) / statistics.mean(metric_measurements)

def standard_deviation(metric_measurements):
    return statistics.stdev(metric_measurements)

def median(metric_measurements):
    return statistics.median(metric_measurements)

def average(metric_measurements):
    return statistics.mean(metric_measurements)

def average_ignore_zeros(metric_measurements):
    return statistics.mean([i for i in metric_measurements if i!=0] or [0])

def calculate_stats_single_instance(instance_stats, instance_raw_measurements):

    for qps in instance_raw_measurements[list(instance_raw_measurements.keys())[0]]:
        instance_stats[qps] = {}
        for metric in instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps]:
            
            if "residency" not in metric: 
                if instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric]:
                    instance_stats[qps][metric] = {}
                    #calculate statistics   
                    print(metric) 
                    if "package-0" in metric or "package-1" in metric or "dram-0" in metric or "dram-1" in metric:
                        instance_stats[qps][metric]['avg'] = average_ignore_zeros(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
                    else:
                        instance_stats[qps][metric]['avg'] = average(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
                    instance_stats[qps][metric]['median'] = median(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
                    instance_stats[qps][metric]['stdev'] = standard_deviation(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
                    if instance_stats[qps][metric]['median'] > 0:
                        instance_stats[qps][metric]['cv'] = coefficient_of_variation(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
                    else:
                        instance_stats[qps][metric]['cv'] = 0
                    instance_stats[qps][metric]['ci'] = {}
                    instance_stats[qps][metric]['ci']['min'], instance_stats[qps][metric]['ci']['max'] = confidence_interval_mean(instance_raw_measurements[list(instance_raw_measurements.keys())[0]][qps][metric])
                else:
                    instance_stats[qps][metric] = {}
                    instance_stats[qps][metric]['avg'] = 0
                    instance_stats[qps][metric]['median'] = 0
                    instance_stats[qps][metric]['stdev'] = 0
                    instance_stats[qps][metric]['cv'] = 0
                    instance_stats[qps][metric]['ci'] = {}
                    instance_stats[qps][metric]['ci']['min'] = 0
                    instance_stats[qps][metric]['ci']['max'] = 0

def calculate_stats_multiple_instances(exp_name,overall_raw_measurements):

    instances_stats = {}
    for ind,instance in enumerate(overall_raw_measurements[exp_name]):
        instances_stats[list(instance.keys())[0]] = {}
        calculate_stats_single_instance(instances_stats[list(instance.keys())[0]], overall_raw_measurements[exp_name][ind])
    
    return instances_stats

def derive_datatype(datastr):
    try:
        return type(ast.literal_eval(datastr))
    except:
        return type("")

def read_timeseries(filepath):
    header = None
    timeseries = None
    with open(filepath, 'r') as f:
        header = f.readline().strip()
        timeseries = []
        data = f.readline().strip().split(',')
        datatype = derive_datatype(data[1])
        f.seek(0)
        for l in f.readlines()[1:]:
            data = l.strip().split(',')
            timestamp = int(data[0])
            value = datatype(data[1])
            timeseries.append((timestamp, value))
    return (header, timeseries)            

def add_metric_to_dict(stats_dict, metric_name, metric_value):
    head = metric_name.split('.')[0]
    tail = metric_name.split('.')[1:]
    if tail:
        stats_dict = stats_dict.setdefault(head, {})
        add_metric_to_dict(stats_dict, '.'.join(tail), metric_value)
    else:
        stats_dict[head] = metric_value

def cpu_state_usage(data, cpu_id):
    cpu_str = "CPU{}".format(cpu_id)
    state_names = ['POLL', 'C1', 'C1E', 'C6']
    state_time_perc = []
    total_state_time = 0
    time_us = 0
    state_usage_vec = []
    for state_name in state_names:
        if state_name in data[cpu_str]:
            (ts_start, val_start) = data[cpu_str][state_name]['usage'][0]
            (ts_end, val_end) = data[cpu_str][state_name]['usage'][-1]
            state_usage = int(val_end) - int(val_start)
            state_usage_vec.append(state_usage)
    return state_usage_vec

def avg_state_usage(stats, cpu_id_list):
    total_state_usage = [0]*4
    cpu_count = 0
    for cpud_id in cpu_id_list:
        cpu_count += 1
        total_state_usage = [a + b for a, b in zip(total_state_usage, cpu_state_usage(stats, cpud_id))]
    avg_state_usage = [a/b for a, b in zip(total_state_usage, [cpu_count]*len(total_state_usage))]
    return avg_state_usage

def cpu_state_time_perc(data, cpu_id):
    cpu_str = "CPU{}".format(cpu_id)
    state_names = ['POLL', 'C1', 'C1E', 'C6']
    state_time_perc = []
    total_state_time = 0
    time_us = 0
    # determine time window of measurements
    for state_name in state_names:
        if state_name in data[cpu_str]:
            (ts_start, val_start) = data[cpu_str][state_name]['time'][0]
            (ts_end, val_end) = data[cpu_str][state_name]['time'][-1]
            time_us = max(time_us, (ts_end - ts_start) * 1000000.0)
            total_state_time += int(val_end) - int(val_start)    
    time_us = max(time_us, total_state_time)
    # FIXME: time duration is currently hardcoded at 120s (120000000us)
    extra_c6_time_us = time_us - 120000000
    # calculate percentage
    for state_name in state_names:
        if state_name == 'C6':
            extra = extra_c6_time_us
        else:
            extra = 0
        if state_name in data[cpu_str]:
            (ts_start, val_start) = data[cpu_str][state_name]['time'][0]
            (ts_end, val_end) = data[cpu_str][state_name]['time'][-1]
            state_time_perc.append(((int(val_end)-int(val_start)-extra)/time_us)*100)
    # calculate C0 as the remaining time 
    state_time_perc[0] = 100 - sum(state_time_perc[1:4])
    state_names[0] = 'C0' 
    return state_time_perc

def avg_state_time_perc(stats, cpu_id_list):
    for stat in stats:
        total_state_time_perc = [0]*4
        cpu_count = 0
        for cpud_id in cpu_id_list:
            cpu_count += 1
            total_state_time_perc = [a + b for a, b in zip(total_state_time_perc, cpu_state_time_perc(stats, cpud_id))]
        avg_state_time_perc = [a/b for a, b in zip(total_state_time_perc, [cpu_count]*len(total_state_time_perc))]
    return avg_state_time_perc

def calculate_cstate_stats(instances_raw_measurements, inst_name, qps):
    # determine used C-states
    state_names = ['C0']
    check_state_names = ['C1', 'C1E', 'C6']
    for state_name in check_state_names:
        if state_name in instances_raw_measurements[inst_name][qps]['bucket-residency'][0]['CPU0']:
            state_names.append(state_name)
    
    time_perc_list = []
    for stat in instances_raw_measurements[inst_name][qps]['bucket-residency']:
        time_perc_list.append(avg_state_time_perc(stat, range(0, 20)))
   
    instances_raw_measurements[inst_name][qps]['bucket-C0-res'] = []
    instances_raw_measurements[inst_name][qps]['bucket-C1-res'] = []
    instances_raw_measurements[inst_name][qps]['bucket-C1E-res'] = []
    instances_raw_measurements[inst_name][qps]['bucket-C6-res'] = []
    metrics=['bucket-C0-res','bucket-C1-res','bucket-C1E-res','bucket-C6-res']
    
    for time_perc in time_perc_list:
        for i, res in enumerate(time_perc):
            instances_raw_measurements[inst_name][qps][metrics[i]].append(res)   

    ## Midtier residency

    state_names = ['C0']
    check_state_names = ['C1', 'C1E', 'C6']
    for state_name in check_state_names:
        if state_name in instances_raw_measurements[inst_name][qps]['midtier-residency'][0]['CPU0']:
            state_names.append(state_name)
    
    time_perc_list = []
    for stat in instances_raw_measurements[inst_name][qps]['midtier-residency']:
        time_perc_list.append(avg_state_time_perc(stat, range(0, 20)))
   
    instances_raw_measurements[inst_name][qps]['midtier-C0-res'] = []
    instances_raw_measurements[inst_name][qps]['midtier-C1-res'] = []
    instances_raw_measurements[inst_name][qps]['midtier-C1E-res'] = []
    instances_raw_measurements[inst_name][qps]['midtier-C6-res'] = []
    metrics=['midtier-C0-res','midtier-C1-res','midtier-C1E-res','midtier-C6-res']
    
    for time_perc in time_perc_list:
        for i, res in enumerate(time_perc):
            instances_raw_measurements[inst_name][qps][metrics[i]].append(res) 
    
    ## RESIDENCY DONE CALCULATE TRANSITIONS
     # determine used C-states
    state_names = ['POLL']
    check_state_names = ['C1', 'C1E', 'C6']
    for state_name in check_state_names:
        if state_name in instances_raw_measurements[inst_name][qps]['bucket-residency'][0]['CPU0']:
            state_names.append(state_name)
    
    usage_list = []
    for stat in instances_raw_measurements[inst_name][qps]['bucket-residency']:
        usage_list.append(avg_state_usage(stat, range(0, 20)))
    
    instances_raw_measurements[inst_name][qps]['bucket-C0-tr'] = []
    instances_raw_measurements[inst_name][qps]['bucket-C1-tr'] = []
    instances_raw_measurements[inst_name][qps]['bucket-C1E-tr'] = []
    instances_raw_measurements[inst_name][qps]['bucket-C6-tr'] = []
    metrics=['bucket-C0-tr','bucket-C1-tr','bucket-C1E-tr','bucket-C6-tr']
    
    for usage_el in usage_list:
        for i, res in enumerate(usage_el):
            instances_raw_measurements[inst_name][qps][metrics[i]].append(res)

    ## Midtier 

    state_names = ['POLL']
    check_state_names = ['C1', 'C1E', 'C6']
    for state_name in check_state_names:
        if state_name in instances_raw_measurements[inst_name][qps]['midtier-residency'][0]['CPU0']:
            state_names.append(state_name)
    
    usage_list = []
    for stat in instances_raw_measurements[inst_name][qps]['midtier-residency']:
        usage_list.append(avg_state_usage(stat, range(0, 20)))
    
    instances_raw_measurements[inst_name][qps]['midtier-C0-tr'] = []
    instances_raw_measurements[inst_name][qps]['midtier-C1-tr'] = []
    instances_raw_measurements[inst_name][qps]['midtier-C1E-tr'] = []
    instances_raw_measurements[inst_name][qps]['midtier-C6-tr'] = []
    metrics=['midtier-C0-tr','midtier-C1-tr','midtier-C1E-tr','midtier-C6-tr']
    
    for usage_el in usage_list:
        for i, res in enumerate(usage_el):
            instances_raw_measurements[inst_name][qps][metrics[i]].append(res)

    return 

def parse_client_turbostat(client_turbostat_file):
    
    data_dict = {}

    # Open the turbostat output file for reading
    with open(client_turbostat_file, 'r') as file:

        # Read all lines from the file
        lines = file.readlines()

    # Extract header and data rows
    header = lines[0].split()
    data_rows = [line.split() for line in lines[1:]]
    
    # Iterate over data rows
    for row in data_rows:
        
        if "Package" in row or not row:
            continue

        # Extract core and data values
        if row[2] == "-":
            core = -1
        else:
            core = int(row[2])
        
        data_values = {header[i]: float(row[i]) for i in range(3, len(row))}

        # Check if the core already exists in the dictionary
        #print(str(j) + " " + str(core))
        if core in data_dict:
            # Append new values to the existing dictionary
            existing_values = data_dict[core]
            for key, value in data_values.items():
                existing_values[key].append(value)
        else:
            # Create a new entry with the current values
            data_dict[core] = {key: [value] for key, value in data_values.items()}

    # Calculate averages for each metric and core
    averages_dict = {}
    for core, values in data_dict.items():
        averages_dict[core] = {key: statistics.mean(value) for key, value in values.items()}
    
    return averages_dict

def parse_cstate_stats(stats_dir):
    stats = {}
    prog = re.compile('(.*)\.(.*)\.(.*)')
    for f in os.listdir(stats_dir):
        m = prog.match(f)
        if m:
            stats_file = os.path.join(stats_dir, f)
            cpu_id = m.group(1)
            state_name = m.group(2)
            metric_name = m.group(3)
            (metric_name, timeseries) = read_timeseries(stats_file)
            add_metric_to_dict(stats, metric_name, timeseries)
    return stats

def parse_power_rapl(power_dir, filename):

    prev_stats, cur_stats = 0, 0
    with open(power_dir + "/" + filename, 'r') as file:
        
        header = next(file) 
        prev_stats = next(file)
        cur_stats = next(file)
        

    final_power =  (int(cur_stats.split(',')[1]) - int(prev_stats.split(',')[1])) / (int(cur_stats.split(',')[0]) - int(prev_stats.split(',')[0])) / 1000000
    
    if final_power < 0:
        return 0
    
    return final_power


def parse_client_time(client_stats_file):
    stats = {}    
    with open(client_stats_file, 'r') as f:
        for l in f:
            if l.startswith('Average Response Time(ms):'):
                stats['avg'] = l.split()[3]
            if "Total response time" in l:
                # next reads all the tail latencies: 10th, 20th, 30th, 40th, 50th, 60th, 70th, 80th, 90th, 95th, 99th, 99.9th
                tail_latencies = next(f).split()[0:] 
                stats['tail'] = tail_latencies
    return stats


def parse_client_throughput(client_stats_file):
    
    with open(client_stats_file, 'r') as f:
        for l in f:
            if l.startswith('Achieved QPS:'):
                return (float(l.split()[2]))


def parse_single_instance_stats(stats,stats_dir, qps):
    
    if "throughput" not in stats:
        stats['throughput'] = []
        stats['avg'] = []
        stats['99th'] = []
        stats['bucket-package-0'] = []
        stats['bucket-package-1'] = []
        stats['bucket-dram-0'] = []
        stats['bucket-dram-1'] = []
        stats['bucket-residency'] = []
        stats['midtier-package-0'] = []
        stats['midtier-package-1'] = []
        stats['midtier-dram-0'] = []
        stats['midtier-dram-1'] = []
        stats['midtier-residency'] = []
    
    if "client-pkg-0" not in stats:
        stats['client-pkg-0'] = []
        stats['client-pkg-1'] = []
        stats['client-C1-res-hw-all'] = []
        stats['client-C6-res-hw-all'] = []
        stats['client-C0-res-hw-all'] = []
        stats['client-C1-res-sw-all'] = []
        stats['client-C1E-res-sw-all'] = []
        stats['client-C6-res-sw-all'] = []
        stats['client-C0-res-sw-all'] = []
        stats['client-C1-res-hw-s0'] = []
        stats['client-C6-res-hw-s0'] = []
        stats['client-C0-res-hw-s0'] = []
        stats['client-C1-res-sw-s0'] = []
        stats['client-C1E-res-sw-s0'] = []
        stats['client-C6-res-sw-s0'] = []
        stats['client-C0-res-sw-s0'] = []
        stats['client-C1-res-hw-s1'] = []
        stats['client-C6-res-hw-s1'] = []
        stats['client-C0-res-hw-s1'] = []
        stats['client-C1-res-sw-s1'] = []
        stats['client-C1E-res-sw-s1'] = []
        stats['client-C6-res-sw-s1'] = []
        stats['client-C0-res-sw-s1'] = []
        stats['client-C1-tr-all'] = []
        stats['client-C1E-tr-all'] = []
        stats['client-C6-tr-all'] = []
        stats['client-C1-tr-s0'] = []
        stats['client-C1E-tr-s0'] = []
        stats['client-C6-tr-s0'] = []
        stats['client-C1-tr-s1'] = []
        stats['client-C1E-tr-s1'] = []
        stats['client-C6-tr-s1'] = []

    # Check if client turbostat in files parse turbostat as well with the rest
    client_turbostat_file = os.path.join(stats_dir, 'turbostat_client')
    if os.path.exists(client_turbostat_file):
        temp = parse_client_turbostat(client_turbostat_file)
        if "PkgWatt" in temp[0]:
            stats['client-pkg-0'].append(temp[0]['PkgWatt'])
        else:
            stats['client-pkg-0'].append(0)

        if "PkgWatt" in temp[10]:
            stats['client-pkg-1'].append(temp[10]['PkgWatt'])
        else:
            stats['client-pkg-1'].append(0)

        if r"CPU%c1" in temp[-1]:
            stats['client-C1-res-hw-all'].append(temp[-1][r'CPU%c1'])
        else:
            stats['client-C1-res-hw-all'].append(0)

        if r"CPU%c6" in temp[-1]:
            stats['client-C6-res-hw-all'].append(temp[-1][r'CPU%c6'])
        else:
            stats['client-C6-res-hw-all'].append(0)
        
        stats['client-C0-res-hw-all'].append(100-stats['client-C6-res-hw-all'][-1] - stats['client-C1-res-hw-all'][-1])

        if "C1%" in temp[-1]:
            stats['client-C1-res-sw-all'].append(temp[-1]['C1%'])
        else:
            stats['client-C1-res-sw-all'].append(0)
        
        if "C1E%" in temp[-1]:
            stats['client-C1E-res-sw-all'].append(temp[-1]['C1E%'])
        else:
            stats['client-C1E-res-sw-all'].append(0)

        if "C6%" in temp[-1]:
            stats['client-C6-res-sw-all'].append(temp[-1]['C6%'])
        else:
            stats['client-C6-res-sw-all'].append(0)
        
        stats['client-C0-res-sw-all'].append(100-stats['client-C6-res-sw-all'][-1] - stats['client-C1-res-sw-all'][-1] - stats['client-C1E-res-sw-all'][-1])

        # Socket 0 Residency
        if r"CPU%c1" in temp[0]:
            stats['client-C1-res-hw-s0'].append(temp[0][r'CPU%c1'])
        else:
            stats['client-C1-res-hw-s0'].append(0)

        if r"CPU%c6" in temp[0]:
            stats['client-C6-res-hw-s0'].append(temp[0][r'CPU%c6'])
        else:
            stats['client-C6-res-hw-s0'].append(0)
        
        stats['client-C0-res-hw-s0'].append(100-stats['client-C6-res-hw-s0'][-1] - stats['client-C1-res-hw-s0'][-1])

        if "C1%" in temp[0]:
            stats['client-C1-res-sw-s0'].append(temp[0]['C1%'])
        else:
            stats['client-C1-res-sw-s0'].append(0)
        
        if "C1E%" in temp[0]:
            stats['client-C1E-res-sw-s0'].append(temp[0]['C1E%'])
        else:
            stats['client-C1E-res-sw-s0'].append(0)

        if "C6%" in temp[0]:
            stats['client-C6-res-sw-s0'].append(temp[0]['C6%'])
        else:
            stats['client-C6-res-sw-s0'].append(0)
        
        stats['client-C0-res-sw-s0'].append(100-stats['client-C6-res-sw-s0'][-1] - stats['client-C1-res-sw-s0'][-1] - stats['client-C1E-res-sw-s0'][-1])

        # Socket 1 Residency
        if r"CPU%c1" in temp[10]:
            stats['client-C1-res-hw-s1'].append(temp[10][r'CPU%c1'])
        else:
            stats['client-C1-res-hw-s1'].append(0)

        if r"CPU%c6" in temp[10]:
            stats['client-C6-res-hw-s1'].append(temp[10][r'CPU%c6'])
        else:
            stats['client-C6-res-hw-s1'].append(0)
        
        stats['client-C0-res-hw-s1'].append(100-stats['client-C6-res-hw-s1'][-1] - stats['client-C1-res-hw-s1'][-1])

        if "C1%" in temp[10]:
            stats['client-C1-res-sw-s1'].append(temp[10]['C1%'])
        else:
            stats['client-C1-res-sw-s1'].append(0)
        
        if "C1E%" in temp[10]:
            stats['client-C1E-res-sw-s1'].append(temp[10]['C1E%'])
        else:
            stats['client-C1E-res-sw-s1'].append(0)

        if "C6%" in temp[10]:
            stats['client-C6-res-sw-s1'].append(temp[10]['C6%'])
        else:
            stats['client-C6-res-sw-s1'].append(0)
        
        stats['client-C0-res-sw-s1'].append(100-stats['client-C6-res-sw-s1'][-1] - stats['client-C1-res-sw-s1'][-1] - stats['client-C1E-res-sw-s1'][-1])

        # Transitions
        if "C1" in temp[-1]:
            stats['client-C1-tr-all'].append(temp[-1]['C1'])
        else:
            stats['client-C1-tr-all'].append(0)
        
        if "C1E" in temp[-1]:
            stats['client-C1E-tr-all'].append(temp[-1]['C1E'])
        else:
            stats['client-C1E-tr-all'].append(0)

        if "C6" in temp[-1]:
            stats['client-C6-tr-all'].append(temp[-1]['C6'])
        else:
            stats['client-C6-tr-all'].append(0)

        # Socket 0 Transitions
        if "C1" in temp[0]:
            stats['client-C1-tr-s0'].append(temp[0]['C1'])
        else:
            stats['client-C1-tr-s0'].append(0)
        
        if "C1E" in temp[0]:
            stats['client-C1E-tr-s0'].append(temp[0]['C1E'])
        else:
            stats['client-C1E-tr-s0'].append(0)

        if "C6" in temp[0]:
            stats['client-C6-tr-s0'].append(temp[0]['C6'])
        else:
            stats['client-C6-tr-s0'].append(0)
        
        # Socket 1 Residency
        if "C1" in temp[10]:
            stats['client-C1-tr-s1'].append(temp[10]['C1'])
        else:
            stats['client-C1-tr-s1'].append(0)
        
        if "C1E" in temp[10]:
            stats['client-C1E-tr-s1'].append(temp[10]['C1E'])
        else:
            stats['client-C1E-tr-s1'].append(0)

        if "C6" in temp[10]:
            stats['client-C6-tr-s1'].append(temp[10]['C6'])
        else:
            stats['client-C6-tr-s1'].append(0)
        

    client_stats_file = os.path.join(stats_dir, 'hdsearch_client')
    stats['throughput'].append(parse_client_throughput(client_stats_file))
    
    client_time_stats = {}
    client_time_stats = parse_client_time(client_stats_file)
    print(client_time_stats)
    print(client_stats_file)
    stats['avg'].append(float(client_time_stats['avg']))
    stats['99th'].append(float(client_time_stats['tail'][-2]))
    
    # Calculate power + residency for both bucket + midtier

    power_dir = os.path.join(stats_dir, 'hdsearch/bucket_node2')
    stats['bucket-package-0'].append(parse_power_rapl(power_dir, "package-0"))
    stats['bucket-package-1'].append(parse_power_rapl(power_dir, "package-1"))
    stats['bucket-dram-0'].append(parse_power_rapl(power_dir, "dram-0"))
    stats['bucket-dram-1'].append(parse_power_rapl(power_dir, "dram-1"))
    
    power_dir = os.path.join(stats_dir, 'hdsearch/midtier_node1')
    stats['midtier-package-0'].append(parse_power_rapl(power_dir, "package-0"))
    stats['midtier-package-1'].append(parse_power_rapl(power_dir, "package-1"))
    stats['midtier-dram-0'].append(parse_power_rapl(power_dir, "dram-0"))
    stats['midtier-dram-1'].append(parse_power_rapl(power_dir, "dram-1"))


    residency_dir = os.path.join(stats_dir, 'hdsearch/bucket_node2')
    stats['bucket-residency'].append(parse_cstate_stats(residency_dir))

    residency_dir = os.path.join(stats_dir, 'hdsearch/midtier_node1')
    stats['midtier-residency'].append(parse_cstate_stats(residency_dir))


def parse_multiple_instances_stats(exp_dir, pattern='.*'):
    
    instances_raw_measurements = {}
    exp_name = exp_dir.split("/")[-1]
    
    dirs = list(os.listdir(exp_dir))
    dirs.sort()

    for conf in dirs:   
        
        instance_dir = os.path.join(exp_dir, conf)
        
        #check if experiment run is a directory and contains a directory with the name memcached and contains turbo in name
        if "turbo" not in conf or not os.path.isdir(instance_dir) or not os.path.isdir(os.path.join(instance_dir, "hdsearch")):
            continue
        
        instance_name = conf[:conf.rfind('-')]
        qps = int(instance_name.split("=")[-1])
        instance_name = instance_name[:instance_name.rfind('-')]
       
        if not os.path.isdir(exp_dir):
            continue

        if instance_name not in instances_raw_measurements:
            instances_raw_measurements[instance_name] = {}
        if qps not in instances_raw_measurements[instance_name]:
            instances_raw_measurements[instance_name][qps] = {}
       
        parse_single_instance_stats(instances_raw_measurements[instance_name][qps],instance_dir, qps)
        
    # calculate statistics for residency in order to find the average per CPU etc....
    for inst_name in instances_raw_measurements:
        for qps in instances_raw_measurements[inst_name]:
            calculate_cstate_stats(instances_raw_measurements, inst_name, qps)

    return instances_raw_measurements

def parse_multiple_exp_stats(stats_dir, pattern='.*'):

    # extract data
    overall_raw_measurements = {}
    for f in os.listdir(stats_dir):
        exp_dir = os.path.join(stats_dir, f)
        if not os.path.isdir(exp_dir):
            continue

        #get configuration for experiment and parse raw data 
        overall_raw_measurements.setdefault(f, []).append(parse_multiple_instances_stats(exp_dir))
    
    #parse statistics
    overall_statistics = {}
    for exp_name in overall_raw_measurements:
        overall_statistics.setdefault(exp_name, []).append(calculate_stats_multiple_instances(exp_name,overall_raw_measurements))

  
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "throughput", "overall_throughput_time.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "avg", "overall_average_time.csv")
    print_single_metric(stats_dir, overall_raw_measurements, overall_statistics, "99th", "overall_99th_time.csv")
    print_all_metrics(stats_dir, overall_raw_measurements, overall_statistics, "all-metrics.csv")

    return overall_raw_measurements


def main(argv):
    stats_root_dir = argv[1]
    stats = parse_multiple_exp_stats(stats_root_dir)
        
if __name__ == '__main__':
    main(sys.argv)
