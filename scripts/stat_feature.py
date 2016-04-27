#!/env/python3 
import sys 
import argparse 
import tabix 
import os 
import csv 
import gzip
from common import * 
#==========================================================================
def compute_stats(file):

	with open(file, "r") as file:
		feature_data = {}

		reader = csv.reader(file, delimiter="\t")
		for line in reader:
			chromosom 	= line[0]
			start 		= int(line[1])
			end 		= int(line[2])
			size  		= end - start 
			feature		= line[3]
			name 		= line[4] 

			if feature not in feature_data:
				feature_data[feature] = {"count": 0, "size": 0 }

			feature_data[feature]["count"] += 1 
			feature_data[feature]["size"]  += size 
			


		print("feature", "count", "size", sep ="\t")
		for key in feature_data:
			print(key, feature_data[key]["count"], feature_data[key]["size"], sep="\t")









	
#==========================================================================
	
parser = argparse.ArgumentParser(
	description="Compute stats from feature bed file", 
	usage="python3 stat_feature.py feature.bed"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")

args = parser.parse_args()

# Start algo 
compute_stats(args.file)