#!/env/python3 
import sys 
import argparse 
import tabix 
import os 
import csv 
import gzip
from common import * 
#==========================================================================
def wgs_signature(file):
	with gzip.open(file,'r') as file:
		reader = csv.reader(io.TextIOWrapper(file, newline=""), delimiter='\t')
		bases = ['A','C','G','T']

		mutations   = {
					('C','T'): 0,
					('T','G'): 0,
					('T','A'): 0,
					('T','C'): 0,
					('C','A'): 0,
					('C','G'): 0
					}

		hit       = 0
		for row in reader:
			chromosom = row[0]
			start     = row[1]
			end       = row[2]
			ref       = row[4].upper()
			alt       = row[5].upper()


			if ref in bases and alt in bases and ref != alt:
				ref, alt = cannonic_mutation((ref,alt))
				hit += 1

				if (ref,alt) in mutations:
					mutations[(ref,alt)]  += 1 
				


		print("feature","CT","CG","CA","TC","TA","TG", sep="\t")
		print("wgs",
			mutations[('C','T')]/ hit,
			mutations[('C','G')]/ hit,
			mutations[('C','A')]/ hit,
			mutations[('T','C')]/ hit,
			mutations[('T','A')]/ hit,
			mutations[('T','G')]/ hit, sep="\t")

 

#==========================================================================

def feature_signature(file, feature):

	with open(feature, "r") as feature_file:
		tx = tabix.open(file)
		bases = ['A','C','G','T']
		mutation_content   = {
					('C','T'): 0,
					('T','G'): 0,
					('T','A'): 0,
					('T','C'): 0,
					('C','A'): 0,
					('C','G'): 0
					}

		mutations = { }
		hits = {}

		reader = csv.reader(feature_file, delimiter="\t")
		# Loop over features 
		for line in reader:
			chromosom = line[0]
			start     = int(line[1])
			end       = int(line[2])
			feature   = line[3]

			if feature not in mutations:
				mutations[feature] = dict(mutation_content)
				hits[feature] = 0

			# For each features, ask tabix 
			try: 
				records = tx.query(chromosom,start, end)
				for record in records : 
					ref = record[4].upper()
					alt = record[5].upper()

					if ref in bases and alt in bases and ref != alt:
						ref,alt = cannonic_mutation((ref,alt))

						mutations[feature][(ref,alt)] += 1 
						hits[feature] += 1	

			except Exception as e :
				print(e, file = sys.stderr)
				print("cannot tabix ", chromosom, start, end, file = sys.stderr)


		print("feature","CT","CG","CA","TC","TA","TG", sep="\t")
		for key in mutations: 
			print(key,
			mutations[key][('C','T')]/ hits[key],
			mutations[key][('C','G')]/  hits[key],
			mutations[key][('C','A')]/  hits[key],
			mutations[key][('T','C')]/  hits[key],
			mutations[key][('T','A')]/  hits[key],
			mutations[key][('T','G')]/  hits[key], sep="\t")	








parser = argparse.ArgumentParser(
	description="Compute signature", 
	usage="python3 signature.py file.bed.gz"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")
parser.add_argument("-f","--feature", type=str, help="compute feature", default=None)

args = parser.parse_args()

if args.feature is None:
	wgs_signature(args.file)

else:
	feature_signature(args.file, args.feature)