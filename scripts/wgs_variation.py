#!/env/python3 
import sys 
import argparse 
import tabix 
import os 
from common import * 
#==========================================================================
def compute_variation(
		tabix_file,
		hg19_size_file,
		window = 10000,
		algorithm="std"):
			
	# Get chromosoms sizes 
	sizes = chromosom_sizes(hg19_size_file)
	tx    = tabix.open(tabix_file)

	# print header 

	print("track type=\"bedGraph name={name}\" description=\"wgs variation\"".format(name=os.path.basename(tabix_file)))


	for chromosom in sizes.keys():
		for position in range(0, sizes[chromosom]- window, window ):
			start = position
			end   = position + window 
			try:
				ratio = 0 
				if algorithm == "uniq":
					ratio = count_mutation_ratio_uniq(tx, chromosom, start, end)
				if algorithm == "std":
					ratio = count_mutation_ratio(tx, chromosom, start, end)
			except Exception as e:
				print(e, file=sys.stderr)
				print("cannot query {}:{}-{}".format(chromosom,start,end), file=sys.stderr)
			else:
				print(chromosom, start, end, ratio, "wgs",sep="\t")



#==========================================================================
	
parser = argparse.ArgumentParser(
	description="Compute mutation per window range. You can select how mutation are count by using algorithm", 
	usage="python3 wgs_variation.py --g hg19_chromosoms.bed --w 1000 --a uniq file.bed.gz"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")
parser.add_argument("-g","--genom", type=str, help="chromosom size range in bed format. (chr,0,size). see hg19_chromosoms.bed", required=True)
parser.add_argument("-w", "--window", type=int, help="window size in base", default=1000)
parser.add_argument("-a","--algorithm", type=str, choices=["std","uniq"], help="'std':mutationCount/window. 'uniq':mutationCount/window*uniqPatient", default="std")

args = parser.parse_args()

# Start algo 
compute_variation(args.file, args.genom, args.window, args.algorithm)