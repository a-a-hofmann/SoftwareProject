from collections import defaultdict
from datetime import datetime

from influxdb import InfluxDBClient


# InfluxDB connections settings
host = 'localhost'
port = 8086
user = 'root'
password = 'root'
dbname = 'mydb'

client = InfluxDBClient(host, port, user, password, dbname)

#clear database at starting
client.drop_database(dbname)
client.create_database(dbname)


#function witch transform the input data in JSON and update the database


#update the worload table giving with src and dst mac adresse and workload
def update_workload(src, workload):
	json_body = [
		 {
			"measurement": "workload",
			"tags": {
				"src_host": src
				},
			"time": datetime.now(),
			"fields": {
				"workload": workload
				}
		}

    	]
	client.write_points(json_body)


#update the latency table giving with src and dst mac adresse and latency
def update_latency(src, dst, latency, max_latency):
	json_body = [
		 {
			"measurement": "latency",
			"tags": {
				"src_host": src,
				"dst_host": dst
				},
			"time": datetime.now(),
			"fields": {
				"latency": latency,
				"max_latency": max_latency
				}
		}

    	]
	client.write_points(json_body)
def update_jitter(src, dst, jitter, max_jitter):
	json_body = [
		 {
			"measurement": "jitter",
			"tags": {
				"src_host": src,
				"dst_host": dst
				},
			"time": datetime.now(),
			"fields": {
				"jitter": jitter,
				"max_jitter": max_jitter
				}
		}

    	]
	client.write_points(json_body)
def update_pkt_loss(src, dst, pkt_loss, max_loss):
	json_body = [
		 {
			"measurement": "pkt_loss",
			"tags": {
				"src_host": src,
				"dst_host": dst
				},
			"time": datetime.now(),
			"fields": {
				"pkt_loss": pkt_loss,
				"max_loss": max_loss
				}
		}

    	]
	client.write_points(json_body)

#update the consume table with src and dst mac adresse and
def update_total_consumption(proportional, baseline, constant):
	json_body = [
		 {
			"measurement": "network consumption",
			"tags": {
				"tag": 1
				},
			"time": datetime.now(),
			"fields": {
				"proportional": int(proportional),
				"baseline": int(baseline),
				"constant": int(constant)
				}
		}

    	]
	client.write_points(json_body)


def update_monitoring_stats(flow_stats_straight, flow_stats_adaptive, port_stats_straight, port_stats_adaptive):
	json_body = [
		 {
			"measurement": "monitoring",
			"tags": {
				"key": 1
				},
			"time": datetime.now(),
			"fields": {
				"flow_stats_straight": flow_stats_straight,
				"flow_stats_adaptive": flow_stats_adaptive,
				"port_stats_straight": port_stats_straight,
				"port_stats_adaptive": port_stats_adaptive
				}
		}

    	]
	client.write_points(json_body)
#update the consume table with src and dst mac adresse and
def update_user_consumption(src, consumption):
	json_body = [
		 {
			"measurement": "consumption",
			"tags": {
				"src_host": src,
				},
			"time": datetime.now(),
			"fields": {
				"total_consumption": consumption
				}
		}

    	]
	client.write_points(json_body)

#update the consume table with src and dst mac adresse and
def update_user_tokens(macaddr, ntokens, nrenews, threshold):
	json_body = [
		 {
			"measurement": "tokens",
			"tags": {
				"src_host": macaddr
				},
			"time": datetime.now(),
			"fields": {
				"network tokens": ntokens,
				"number renews": nrenews,
				"threshold": threshold
				}
		}

    	]
	client.write_points(json_body)

def update_switch_consumption(switch, proportional, baseline, constant):
	json_body = [
		 {
			"measurement": "consumption",
			"tags": {
				"switch": switch
				},
			"time": datetime.now(),
			"fields": {
				"proportional": proportional,
				"baseline": baseline,
				"constant": constant

				}
		}

    	]
	client.write_points(json_body)

def update_system_utilization(cpu, mem):
	json_body = [
		 {
			"measurement": "system",
			"tags": {
				"cpu": 1
				},
			"time": datetime.now(),
			"fields": {
				"cpu value": cpu,
				"mem value": mem
				}

		}

    	]
	client.write_points(json_body)
