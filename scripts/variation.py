#!/env/python3  
import sys 
import argparse 
import tabix 
import csv 
from common import * 

def compute_feature_variation(file, feature):
	print("feature")


def compute_wgs_variation(file, genom, window):
	print("wgs")
			
	# # Create tabix object
	# tx = tabix.open(tabix_file)

	# # Loop over features 
	# with open(feature_file) as file:
	# 	reader = csv.reader(file, delimiter = "\t")
	# 	for line in reader:
	# 		chromosom 	= line[0]
	# 		start 		= int(line[1])
	# 		end			= int(line[2])
	# 		categorie	= line[3]
	# 		try:
	# 			ratio = -1 
	# 			if algorithm == "uniq":
	# 				ratio = count_mutation_ratio_uniq(tx, chromosom, start, end)
	# 			if algorithm == "std":
	# 				ratio = count_mutation_ratio(tx, chromosom, start, end)
	# 		except Exception as e:
	# 			print("cannot query {}:{}-{}".format(chromosom,start,end), file=sys.stderr)
	# 			print(e, file=sys.stderr)
				
	# 		else:
	# 			print(chromosom, start, end, ratio, categorie, sep="\t")


	

parser     = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help', dest="command")


wgs_parser = subparsers.add_parser("wgs", help="wgs")
wgs_parser.add_argument('file', type=str, help="tabix file")
wgs_parser.add_argument('--genom', type=str, help="")
wgs_parser.add_argument('--window', type=int, help="")

feature_parser = subparsers.add_parser("feature", help="feature")
feature_parser.add_argument('file', type=str, help="tabix file")
feature_parser.add_argument('--feature', type=str, help="")

args = parser.parse_args()


if args.command == "wgs":
	compute_wgs_variation(args.file, args.genom, args.window)

if args.command == "feature":
	compute_feature_variation(args.file, args.feature)




