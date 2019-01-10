#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    ANDRADATA LIMITED SET EXTRACT TOOL
    ~~~~~~~~~~~~~~
    Tool to gather some ANDRADATA in a specified folder
    :copyright: 2018 - GLINCS-AXINT, see AUTHORS for more details
    :license: Proprietary and confidential, see LICENSE for more details
"""

import os, datetime, re, csv

ANDRA_DATA_ORIGIN = 'ANDRADATA'
EXTRACT_LIST = 'extractlist.txt'
OUTPUT_FOLDER = 'output.csv'

"""
UTILS PART
"""

class SensorData:
	def __init__(self, date, value, probe, sensor):
		self.date = date
		self.value = value
		self.probe = probe
		self.sensor = sensor

def extract_data_from_date_list(extract_list, root_folder):

	data = []

	for file in os.listdir(root_folder):
		if file[-4:] == '.txt':
			date = datetime.datetime.strptime(file.strip('\n')[:-14], "%Y-%m-%d")
			
			for extract_date in extract_list:
				if date.date() == extract_date.date():
					data.extend(extract_data_from_file(ANDRA_DATA_ORIGIN, file, extract_list))
					break

	return data

def extract_data_from_file(origin, file, extract_list):
	extraction = []

	date = datetime.datetime.strptime(file.strip('\n')[:-14], "%Y-%m-%d")

	hours = [x for x in extract_list if x.date() == date.date()]
	
	for hour in hours:
		date_to_extract = hour.strftime('%d/%m/%Y %H:%M:%S')
		pattern = r'DRN[0-9]{4}_RAY_[0-9]{2}	%s	[0-9]*	0' % date_to_extract

		with open(os.path.join(origin, file), "r") as objf:
			for line in objf:
				if re.match(pattern, line):
					data = SensorData(hour, re.findall(r'	[0-9]+	', line)[0][1:-1], re.findall(r'DRN[0-9]{4}', line)[0], re.findall(r'RAY_[0-9]{2}', line)[0][4:])
					extraction.append(data)
					break

	return extraction

def extract_extract_list(path):
	extract_list = []

	with open(path, "r") as objf:
		for line in objf:
			date = datetime.datetime.strptime(line.strip('\n').strip(" "), "%d/%m/%Y %HH")
			extract_list.append(date)

	return extract_list

def output_CSV(path, datalist):
	file = open(path, 'w')
	out = csv.writer(file, lineterminator='\n', delimiter=',', quotechar="\"", quoting=csv.QUOTE_ALL)

	out.writerow(['Date', 'Hour', 'Value', 'Probe', 'Sensor'])

	for data in datalist:
		row = [data.date.strftime('%Y-%m-%d'), data.date.strftime('%H'), data.value, data.probe, data.sensor]
		out.writerow(row)

if __name__ == '__main__':
	extract_list = extract_extract_list(EXTRACT_LIST)
	print("Liste d'extractions -> OK")

	data = extract_data_from_date_list(extract_list, ANDRA_DATA_ORIGIN)
	print("Extraction des données -> OK")

	output_CSV(OUTPUT_FOLDER, data)
	print("Impression CSV -> OK")
