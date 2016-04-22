#!/env/python3 
import sys 
import argparse 
import tabix 
import os 
import csv 
import gzip
from common import * 
#==========================================================================
def detect_peaks(file, count):
	# Get chromosoms sizes 
	

	with gzip.open(file,'r') as file:
		reader = csv.reader(io.TextIOWrapper(file, newline=""), delimiter='\t')
		output = []
		hit = 0
		last = None
		for row in reader:
			chromosom = row[0]
			start = row[1]
			end = row[2]

			if (chromosom,start) == last:
				hit +=1 

			else:
				if hit >= count:
					print(chromosom, start, end, hit)
				
				last = (chromosom,start)
				hit  = 0











	# print header 


	
#==========================================================================
	
parser = argparse.ArgumentParser(
	description="Detect position with high repetition at same position", 
	usage="python3 detect_peaks.py -c 40 -g genom.bed file.bed.gz"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")
parser.add_argument("-c","--count", type=int, help="how many hits", default=10)

args = parser.parse_args()

# Start algo 
detect_peaks(args.file, args.count)