
import requests

from ispConfig import resthttp_url as base_url, \
	resthttp_network_uri as network_uri, \
	resthttp_devices_uri as devices_uri, \
	resthttp_requests_headers as requests_headers
from urllib3.exceptions import InsecureRequestWarning

import json
import csv

def getShapedDevicesJson():
	url = base_url + '/' + devices_uri.strip('/')
	print(url)
	r = requests.get(url, headers=requests_headers, verify=False, timeout=60)
	return r.json()

def getNetworkJson():
	url = base_url + '/' + network_uri.strip('/')
	print(url)
	r = requests.get(url, headers=requests_headers, verify=False, timeout=60)
	return r.json()

def createShaper():

	requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
	print('Fetching from http integration')

	network = getNetworkJson()

	with open('network.json', 'w') as f:
		json.dump(network, f, indent=4)

	# devices = getNetworkJson()
	devices = getShapedDevicesJson()

	# print(devices)
	with open('ShapedDevices.csv', 'w', newline='') as csvfile:
		wr = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
		wr.writerow(['Circuit ID', 'Circuit Name', 'Device ID', 'Device Name', 'Parent Node', 'MAC', 'IPv4', 'IPv6',
			'Download Min Mbps', 'Upload Min Mbps', 'Download Max Mbps', 'Upload Max Mbps', 'Comment'])
		for row in devices:
			wr.writerow([
				row['circuit_id'],
				row['circuit_name'],
				row['device_id'],
				row['device_name'],
				row['parent_node'],
				row['mac'],
				row['IPv4'],
				row['IPv6'],
				row['ingress_min_mbps'],
				row['egress_min_mbps'],
				row['ingress_max_mbps'],
				row['exgress_max_mbps'],
				''
			])


def importFromRestHttp():
	createShaper()

if __name__ == '__main__':
	importFromRestHttp()
