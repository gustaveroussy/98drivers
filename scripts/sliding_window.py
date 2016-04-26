import argparse 
import tabix 
import os 
from common import * 

def sliding_window(tabix_file, genom, window ):
	sizes = chromosom_sizes(genom)

	tx = tabix.open(tabix_file)

	chromosom = "chr12"
	print("track type=\"bedGraph name={name}\" description=\"sliding window\"".format(name=os.path.basename(tabix_file)))

	for position in range(0, sizes[chromosom] - window):
		start  = position
		end    = position + window 
		middle = start + window/2 
		score  = 0 

		#percent = start / sizes[chromosom] * 100 

		# if int(percent * 100) % 2 : 
		# 	print(round(percent, 2), "%") 


		for record in tx.query(chromosom, start, end):
			s      = int(record[1]) - start 
			score += bartlett_window_coeff(s, window)
				
		
		if score != 0:
			print(chromosom,middle,middle+1,score, sep="\t")

			





			




parser = argparse.ArgumentParser(
	description="wgs sliding window ", 
	usage=""
	)

parser.add_argument("file", 			type=str, help="bed.gz file indexed with tabix")
parser.add_argument("-g","--genom", 	type=str, help="", required=True)
parser.add_argument("-w","--window", 	type=int, help="", default=1000)

args = parser.parse_args()

# # Start algo 
# compute_feature_variation(args.file, args.feature, args.algorithm)

sliding_window(args.file, args.genom, args.window)