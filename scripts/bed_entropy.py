#!/env/python3 
import sys 
import argparse 
import tabix 
import os 
import csv 
import gzip
import entropy

#==========================================================================
def compute_entropy(region_file:str, tabix_file:str):
	
	tx = tabix.open(tabix_file)

	with open(region_file) as regions:
		reader = csv.reader(regions, delimiter="\t")
		for region in reader:
			# avoid header line # 
			if str(region[0]).startswith("#") == True:
				print("\t".join(region),"entropy",sep="\t")
			else:
				chromosome 	= region[0]
				start 		= int(region[1])
				end 		= int(region[2])
				size 		= end - start 
				serie 		= [0] * size 


				for record in tx.query(chromosome, start,end):
					t_start = int(record[1])
					t_end   = int(record[2])
					index   = t_start - start 
					serie[index]+=1

				serie_str = "".join(str(i) for i in serie)
				e = entropy.shannon_entropy(serie_str)

				print("\t".join(region), e, sep="\t")





	
#==========================================================================
	
parser = argparse.ArgumentParser(
	description="Compute entropy from region and tabix file", 
	usage="python3 entropy.py --region region.bed file.bed.gz"
	)

parser.add_argument("file", type=str, help="bed.gz file indexed with tabix")
parser.add_argument("-r","--region", type=str, help="region file where entropy is compute")

args = parser.parse_args()

# Start algo 
compute_entropy(args.region, args.file)