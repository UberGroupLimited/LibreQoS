import time
import datetime
from LibreQoS import refreshShapers, refreshShapersUpdateOnly
from graphInfluxDB import refreshBandwidthGraphs, refreshLatencyGraphs
from ispConfig import influxDBEnabled, automaticImportUISP, automaticImportSplynx, automaticImportRestHttp
if automaticImportUISP:
	from integrationUISP import importFromUISP
if automaticImportSplynx:
	from integrationSplynx import importFromSplynx
if automaticImportRestHttp['enabled']:
	from integrationRestHttp import importFromRestHttp

from apscheduler.schedulers.background import BlockingScheduler

ads = BlockingScheduler()

def importFromCRM():
	if automaticImportUISP:
		try:
			importFromUISP()
		except:
			print("Failed to import from UISP")
	elif automaticImportSplynx:
		try:
			importFromSplynx()
		except:
			print("Failed to import from Splynx")
	elif automaticImportRestHttp['enabled']:
		try:
			importFromRestHttp()
		except:
			print("Failed to import from RestHttp")

def graphHandler():
	try:
		refreshBandwidthGraphs()
	except:
		print("Failed to update bandwidth graphs")
	try:
		refreshLatencyGraphs()
	except:
		print("Failed to update latency graphs")

def importAndShapeFullReload():
	importFromCRM()
	refreshShapers()

def importAndShapePartialReload():
	importFromCRM()
	refreshShapersUpdateOnly()

if __name__ == '__main__':
	importAndShapeFullReload()

	ads.add_job(importAndShapePartialReload, 'interval', minutes=30)

	if influxDBEnabled:
		ads.add_job(graphHandler, 'interval', seconds=10)

	ads.start()
