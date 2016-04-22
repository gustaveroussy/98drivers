#!/env/python3 

import sys 
import argparse 
import os 
from jinja2 import Environment, FileSystemLoader

#====================================================================================
def create_single_report(sample, basedir, template_dir):

	j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)
	print(j2_env.get_template("single_report.html").render(sample = sample))



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