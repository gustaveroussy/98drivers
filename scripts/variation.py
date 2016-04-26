#!/env/python3  
import sys 
import argparse 
import tabix 
import csv 
import os 
from common import * 

def compute_feature_variation(tabix_file, feature_file, algorithm):
	''' compute mutation count per feature ''' 
	
	# Create tabix object
	tx = tabix.open(tabix_file)

	# Loop over features 
	with open(feature_file) as file:
		reader = csv.reader(file, delimiter = "\t")

		for line in reader:
			chromosom 	= line[0]
			start 		= int(line[1])
			end			= int(line[2])
			categorie	= line[3]
			try:
				score = count_mutation(tx, chromosom, start, end, algorithm)

			except Exception as e:
				print("cannot query {}:{}-{}".format(chromosom,start,end), file=sys.stderr)
				print(e, file=sys.stderr)
				
			else:
				print(chromosom, start, end, score, categorie, sep="\t")


def compute_wgs_variation(file, genom, window,algorithm):
	''' compute mutation count per window '''
	# Get chromosoms sizes 
	sizes = chromosom_sizes(genom)
	tx    = tabix.open(file)

	# print header 
	print("track type=\"bedGraph name={name}\" description=\"wgs variation\"".format(name=os.path.basename(file)))

	for chromosom in sizes.keys():
		for position in range(0, sizes[chromosom]- window, window ):
			start = position
			end   = position + window 
			try:
				score = count_mutation(tx, chromosom, start, end, algorithm)
			
			except Exception as e:
				print(e, file=sys.stderr)
				print("cannot query {}:{}-{}".format(chromosom,start,end), file=sys.stderr)
			else:
				print(chromosom, start, end, score, "wgs",sep="\t")

	

parser     = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help', dest="command")


wgs_parser = subparsers.add_parser("wgs", help="wgs")
wgs_parser.add_argument('file', type=str, help="tabix file")
wgs_parser.add_argument('-g','--genom', type=str, help="")
wgs_parser.add_argument('-w','--window', type=int, help="")
wgs_parser.add_argument('-a','--algorithm', type=str, choices=("std", "uniq","bartlett"), help="", default="std")


feature_parser = subparsers.add_parser("feature", help="feature")
feature_parser.add_argument('file', type=str, help="tabix file")
feature_parser.add_argument('-f','--feature', type=str, help="")
feature_parser.add_argument('-a','--algorithm', type=str, choices=("std", "uniq","bartlett"), help="", default="std")

args = parser.parse_args()


if args.command == "wgs":
	compute_wgs_variation(args.file, args.genom, args.window, args.algorithm)

if args.command == "feature":
	compute_feature_variation(args.file, args.feature, args.algorithm)




