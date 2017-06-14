from collections import defaultdict
from datetime import datetime

from influxdb import InfluxDBClient
#from fbcontroller import *
import fbcontroller


# InfluxDB connections settings
host = 'localhost'
port = 8086
user = 'root'
password = 'root'
dbname = 'mydb'

client = InfluxDBClient(host, port, user, password, dbname)

#clear database at starting
# client.drop_database(dbname)
# client.create_database(dbname)


def get_now_timestamp():
	"""
		Gets a timestamp using a format influxdb likes.
	"""
	return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	# return fbcontroller.clockObj.get_now_timestamp()



def update_path_consumption(path):
	json_body = [
		 {
		"measurement": "test",
		"tags": {
			"path": str(path.path)
		},
		"time": get_now_timestamp(),
		"fields": {
			"value": path.total_consumption
		}
	}

		]
	client.write_points(json_body)

#update the consume table with src and dst mac adresse and
def update_node_data(node_id, workload, consumption, baseline, constant):
	json_body = [
		 {
			"measurement": "node consumptions",
			"tags": {
				"node_id": node_id
				},
			"time": get_now_timestamp(),
			"fields": {
				"workload": float(workload),
				"consumption": float(consumption),
				"baseline": float(baseline),
				"constant": float(constant)
				}
		}

    	]
	client.write_points(json_body)

#update the consume table with src and dst mac adresse and
def update_total_consumption_with_policy(proportional, always_on_energy_efficiency, baseline, constant, policy_change):
	json_body = [
		 {
			"measurement": "network consumption with policy",
			"tags": {
				"tag": 1
				},
			"time": get_now_timestamp(),
			"fields": {
				"proportional": proportional,
				"always_on_energy_efficiency": always_on_energy_efficiency,
				"baseline": baseline,
				"constant": constant,
				"policy_change": policy_change
				}
		}

    	]
	client.write_points(json_body)


#update the worload table giving with src and dst mac adresse and workload
def update_workload(src, workload):
	json_body = [
		 {
			"measurement": "workload",
			"tags": {
				"src_host": src
				},
			"time": get_now_timestamp(),
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
			"time": get_now_timestamp(),
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
			"time": get_now_timestamp(),
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
			"time": get_now_timestamp(),
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
			"time": get_now_timestamp(),
			"fields": {
				"proportional": float(proportional),
				"baseline": float(baseline),
				"constant": float(constant)
				}
		}

    	]
	client.write_points(json_body)


def update_total_consumption_node_subset(proportional, baseline, constant):
	json_body = [
		 {
			"measurement": "network consumption node subset",
			"tags": {
				"tag": 1
				},
			"time": get_now_timestamp(),
			"fields": {
				"proportional": proportional,
				"baseline": baseline,
				"constant": constant
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
			"time": get_now_timestamp(),
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
			"time": get_now_timestamp(),
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
			"time": get_now_timestamp(),
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
			"time": get_now_timestamp(),
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
			"time": get_now_timestamp(),
			"fields": {
				"cpu value": cpu,
				"mem value": mem
				}

		}

    	]
	client.write_points(json_body)
