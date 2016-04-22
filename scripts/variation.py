#!/env/python3  
import sys 
import argparse 
import tabix 
import csv 
from common import * 

def compute_variation(
		tabix_file,
		feature_file, 
		algorithm="std"):
			
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


	
parser = argparse.ArgumentParser(
	description="Compute mutation per feature. You can select how mutation are count by using algorithm", 
	usage="python3 feature_variation.py --f feature.bed --a uniq file.bed.gz"
	)

parser.add_argument("file", 			type=str, help="bed.gz file indexed with tabix")
parser.add_argument("-f","--feature", 	type=str, help="feature in bed format. (chr,start,end, type)", required=True)
parser.add_argument("-a","--algorithm", type=str, help="'std':mutationCount/window. 'uniq':mutationCount/window*uniqPatient",choices=["std","uniq"], default="std")

args = parser.parse_args()

# Start algo 
compute_feature_variation(args.file, args.feature, args.algorithm)