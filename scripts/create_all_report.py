#!/env/python3 

import sys 
import argparse 
import os 
import csv 
from jinja2 import Environment, FileSystemLoader

#====================================================================================
def create_single_report(pages, basedir, template_dir):

	j2_env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True)

	print(pages, file = sys.stderr)
	
	print(j2_env.get_template("all_report.html").render(
		pages = pages

		))



#====================================================================================
parser = argparse.ArgumentParser(
	description="Create all report from all html page", 
	usage="python3 create_all_report.py Pancreas.html Truc.html Test.html"
	)

parser.add_argument("pages", type=str, nargs="+", help="ex:Pancreas")
parser.add_argument("--basedir", type=str, help="Where data are ")
parser.add_argument("--template_dir", type=str)

args = parser.parse_args()

create_single_report(args.pages, args.basedir, args.template_dir)