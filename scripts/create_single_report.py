#!/env/python3 

import sys 
import argparse 
import os 
import csv 
from jinja2 import Environment, FileSystemLoader


def read_bedgraph(file):
	table = []
	with open(file, "r") as file:
		reader = csv.reader(file,delimiter="\t")
		next(reader)
		for line in reader:
			table.append(line)	
	return table 

def read_dict(file):
	dictionnary = {}
	with open(file, "r") as file:
		reader = csv.reader(file,delimiter="\t")
		for line in reader:
			dictionnary[line[0]] = line[1]
	return dictionnary

def read_table(file):
	data = []
	with open(file, "r") as file:
		reader = csv.reader(file,delimiter="\t")
		header = next(reader)

		for line in reader:
			item = {}
			for index in range(len(header)):
				item[header[index]] = line[index]

			data.append(item)

	return data




#====================================================================================
def create_single_report(sample, basedir, template_dir):

	j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)

	# Read wgs_max_score 


	wgs_info      = read_table("{basedir}/{sample}.wgs.info".format(sample = sample, basedir = basedir))
	features_info = read_table("{basedir}/{sample}.all.info".format(sample = sample, basedir = basedir))
	peaks_data    = read_table("{basedir}/{sample}.wgs.peaks.annotated.bed".format(sample = sample, basedir = basedir))



	print(j2_env.get_template("test.html").render(
	sample   		= sample,
	wgs_info 		= wgs_info,
	features_info 	= features_info,
	peaks_data       = peaks_data
		))



#====================================================================================
parser = argparse.ArgumentParser(
	description="Create a single report per sample, after all file has been generated.", 
	usage="python3 create_single_report.py Pancreas"
	)

parser.add_argument("sample", type=str, help="ex:Pancreas")
parser.add_argument("--basedir", type=str, help="Where data are ")
parser.add_argument("--template_dir", type=str)


args = parser.parse_args()

create_single_report(args.sample, args.basedir, args.template_dir)