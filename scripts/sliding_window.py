import argparse 
import tabix 
import os 
from common import * 

def sliding_window(tabix_file, genom, window ):
	sizes 	= chromosom_sizes(genom)
	tx 		= tabix.open(tabix_file)

	for chromosom in sizes:
		for position in range(0,sizes[chromosom] - window, window):
			start  			= position
			end    			= position + window 
			count  			= count_mutation_ratio_std(tx, chromosom, start , end)
			distinct_count  = count_mutation_ratio_uniq(tx, chromosom, start ,end,3)

			print(chromosom,start,end,count, distinct_count, sep="\t")



	# for position in range(0, sizes[chromosom] - window):
	# 	start  = position
	# 	end    = position + window 
	# 	middle = start + window/2 
		
	# 	count_mutation_ratio_std(tx, chromosom:str, start , end:int):

		
	
			

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