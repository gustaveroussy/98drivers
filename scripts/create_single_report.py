#!/env/python3 

import sys 
import argparse 
import os 
import csv 
from jinja2 import Environment, FileSystemLoader


def read_table(file):
	table = []
	with open(file, "r") as file:
		reader = csv.reader(file,delimiter="\t")
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



#====================================================================================
def create_single_report(sample, basedir, template_dir):

	j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)

	# Read wgs_max_score 


	print(j2_env.get_template("single_report.html").render(
	sample = sample, 
	wgs_max_table = read_table("{basedir}/{sample}.wgs_variation.max.bed".format(basedir=basedir, sample=sample)),
	peak_table    = read_table("{basedir}/{sample}.wgs_peak.bedgraph".format(basedir=basedir, sample=sample)),
	stats         = read_dict("{basedir}/{sample}.stat".format(basedir=basedir, sample=sample))
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