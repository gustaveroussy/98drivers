#!/env/python3 
import sys 
import argparse 
import tabix 
import os 
from common import * 
#==========================================================================
def compute_signature(file, feature, algorithm):
	# Get chromosoms sizes 
	tx    = tabix.open(file)

	# print header 

	print("track type=\"bedGraph name={name}\" description=\"feature signature\"".format(name=os.path.basename(file)))

	# Loop over features 
	with open(feature) as file:
		reader = csv.reader(file, delimiter = "\t")
		for line in reader:
			chromosom 	= line[0]
			start 		= int(line[1])
			end			= int(line[2])
			categorie	= line[3]

			try:
				result = count_transition_transversion(tx, chromosom,start, end)

			except Exception as e:
				print(e, file=sys.stderr)
				print("cannot query {}:{}-{}".format(chromosom,start,end), file=sys.stderr)

			else:
				print(chromosom, start, end, result["transversion"], result["transition"], categorie,sep="\t")
		
	


			# try:
			# 	ratio = 0 
			# 	if algorithm == "uniq":
			# 		ratio = count_mutation_ratio_uniq(tx, chromosom, start, end)
			# 	if algorithm == "std":
			# 		ratio = count_mutation_ratio(tx, chromosom, start, end)
			# except Exception as e:
			# 	print(e, file=sys.stderr)
			# 	print("cannot query {}:{}-{}".format(chromosom,start,end), file=sys.stderr)
			# else:
			# 	print(chromosom, start, end, ratio, "wgs",sep="\t")





#==========================================================================
	
parser = argparse.ArgumentParser(
	description="Computation wgs signature ", 
	usage="python3 wgs_variation.py --f feature.bed --a tt file.bed.gz"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")
parser.add_argument("-f","--feature", type=str, help="feature in bed format", required=True)
parser.add_argument("-a","--algorithm", type=str, choices=["tt","alt", "ra" ], help="'std':mutationCount/window. 'uniq':mutationCount/window*uniqPatient", default="std")

args = parser.parse_args()

# Start algo 
compute_signature(args.file, args.feature, args.algorithm)