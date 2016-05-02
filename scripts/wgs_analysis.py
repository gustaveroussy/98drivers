#!/env/python3 
import sys 
import argparse 
import tabix 
import os 
import csv 
import gzip
from common import * 

#==============================================================================
def wgs_analysis(file):

	basename 			= os.path.basename(file).split(".")[0]
	info_filename 		= "{basename}.info".format(basename=basename)
	signature_filename 	= "{basename}.signature".format(basename=basename)
	peak_filename 		= "{basename}.peak".format(basename=basename)


	with gzip.open(file,'r') as file:
		reader 			= csv.reader(io.TextIOWrapper(file, newline=""), delimiter='\t')
		output = compute_info(reader)

		for key in sorted(output.keys()):
			print(key, end="\t")

		print("feature")

		for key in sorted(output.keys()):
			print(output[key], end="\t")

		print("wgs")
	
#==============================================================================
def sum_dict(a, b):
	return { k: a[k] + b[k] for k in set(a) & set(b) }

#==============================================================================
def feature_analysis(file, feature_filename):

	# Open feature file 
	with open(feature_filename) as feature_file:
		feature_reader 	= csv.reader(feature_file, delimiter="\t")
		features 		= set()
		tx  			= tabix.open(file)
		output          = {}
		sizes           = {}

		# Loop over feature file 
		for line in feature_reader:
			chromosom 	= line[0]
			start 		= int(line[1])
			end 		= int(line[2])
			feature 	= line[3]
			size        = end - start 
			# For each feature line, compute info in the range 
			# Sum feature info by feature name into a dictionnary output 
			try:
				records = tx.query(chromosom,start, end)
				result  = compute_info(records)

				if feature not in output : 
					output[feature] = result
					sizes[feature]  = size

				else:
					output[feature] = sum_dict(output[feature],result)
					sizes[feature]  += size
			except:
				print("cannot query ", chromosom, start, end, file = sys.stderr)

	# Print header 
	random_feature = list(output.keys())[0]
	for key in sorted(output[random_feature].keys()):
		print(key, end="\t")
	print("feature", "size", sep="\t")

	# Print data 
	for feature in output.keys():
		for key in sorted(output[feature].keys()):
			print(output[feature][key], end="\t")
		print(feature, sizes[feature], sep = "\t")


		

parser = argparse.ArgumentParser(
	description="Start variant analysis on whole genom", 
	usage="python3 wgs_analysis.py file.bed.gz"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")
parser.add_argument("-f","--feature", type=str, help="destination", default=None)

args = parser.parse_args()

if args.feature is None:
	wgs_analysis(args.file)
else:
	feature_analysis(args.file, args.feature)