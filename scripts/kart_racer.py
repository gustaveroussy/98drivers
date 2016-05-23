#!/env/python3 

import sys 
import argparse 
import os 
import csv 
import tabix 
import gzip 
import io
from collections import Counter

def chromosom_sizes(hg19_size_file):
	''' Return chromosom size range ex: size["chr13"] = 234324 ''' 
	results = {}
	with open(hg19_size_file) as file:
		reader = csv.reader(file, delimiter="\t")
		for line in reader:
			results[line[0]] = int(line[1])
	return results


def kart_racer(sample, genom, base_speed = 0, deceleration = 1, acceleration = 1, allow_negative = False):


	# get chromosom size 
	sizes 		= chromosom_sizes(genom)
	# get tabix variant file 
	tabix_file 	= tabix.open(sample) 
	# current speed 
	speed       = 0.0 + base_speed

	# test on chromosom 17
	chromosom = "chr17"
	size = sizes[chromosom]
	
	# Loop over genoms 
	for pos in range(0, size):

		# get how many mutation at one position 
		count = len([c for c in tabix_file.query(chromosom, pos, pos + 2)]) 
		
		if count > 0 : 
			speed += count * acceleration
		else:
			if speed > 0:
				speed -= deceleration
			else:
				speed = 0.0


		print(chromosom, pos, pos +1,  speed, sep="\t")




if __name__ == '__main__':

	parser = argparse.ArgumentParser(
		description="Compute speed of mutation ", 
		usage="kart_racer.py file.bed.gz -g hg19.sizes -a 1 -b 0.1 "
		)

	parser.add_argument("sample", type=str, help="tabix file")
	parser.add_argument("-g","--genom", type=str, help="genom size ")
	parser.add_argument("-b","--base_speed", type=int, default = 0)
	parser.add_argument("-d","--deceleration", type=float, default = 0.01, help="decrease speed by x each empty base")
	parser.add_argument("-a","--acceleration", type=float, default = 1, help="accelerate by 1 each variant")



	args = parser.parse_args()

	kart_racer(args.sample, args.genom, args.base_speed , args.deceleration , args.acceleration, False )

