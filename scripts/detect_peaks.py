#!/env/python3 
import sys 
import argparse 
import tabix 
import os 
from common import * 
#==========================================================================
def detect_peaks(file, genom, count):
	# Get chromosoms sizes 
	tx    = tabix.open(file)
	sizes = chromosom_sizes(genom)
	# print header 

	for chromosom in sizes.keys():
		for position in range(0, sizes[chromosom]):
			start = position
			end   = position + 1 
			try:
				hit = 0 
				for record in tx.query(chromosom, start, end):
					hit += 1

				if hit >= count: 
					print(chromosom, start, end, hit, sep="\t")

			except Exception as e:
				print(e, file=sys.stderr)
				print("cannot query {}:{}-{}".format(chromosom,start,end), file=sys.stderr)

	
#==========================================================================
	
parser = argparse.ArgumentParser(
	description="Detect position with high repetition at same position", 
	usage="python3 detect_peaks.py -c 40 -g genom.bed file.bed.gz"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")
parser.add_argument("-g","--genom", type=str, help="genom chromosom size ", required=True)
parser.add_argument("-c","--count", type=int, help="how many hits", default=10)

args = parser.parse_args()

# Start algo 
detect_peaks(args.file, args.genom, args.count)