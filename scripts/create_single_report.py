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
	with open(file,"r") as file:
		reader = csv.reader(file, delimiter="\t")

		for line in reader : 
			data.append(line)
	return data



#====================================================================================
def create_single_report(name, basedir, template_dir):

	j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)

	
	print(j2_env.get_template("single_report.html").render(
	sample   		= name,
	stat            = read_dict("{}.stat".format(name)),
	clusters        = read_table("{}.cluster.annotate.entropy.bed".format(name)),
	peaks           = read_table("{}.peaks.annotate.bed".format(name))
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