#!/usr/bin/env python3 
import gzip 
import csv 
import io
import sys
import re 
import tabix 


def chromosom_sizes(hg19_size_file):
	''' Return chromosom size range ''' 
	results = {}
	with open(hg19_size_file) as file:
		reader = csv.reader(file, delimiter="\t")
		for line in reader:
			results[line[0]] = int(line[2])
	return results


def count_mutation_ratio(tabix, chromosom:str, start , end:int):
	''' count hit / size feature ''' 
	hit  = 0
	size = end - start   
	for i in tabix.query(chromosom, start, end):
		hit+=1 

	return float(hit) / float(size) * 100

def count_mutation_ratio_uniq(tabix, chromosom:str, start , end:int, patientField = 3):
	''' count hit / size * uniqPatient ''' 
	hit = 0
	size = end - start  
	uniqList = set()

	for record in tabix.query(chromosom, start, end):
		uniqList.add(record[patientField])
		hit+=1 

	return (float(hit) / float(size)) * len(uniqList) * 100


def cannonic_mutation(mutation : tuple):
	complement = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
	ref  = mutation[0]
	alt  = mutation[1]


	if ref in ('A', 'G'):
		ref = complement[ref]
		alt = complement[alt]

	return (ref, alt)




def count_transition_transversion(tabix, chromosom:str, start , end:int):
	''' count transition & transversion ''' 
	hit = 0
	size = end - start  

	if size <= 0:
		raise Exception("region length is too small ")

	transversion_count = 0.0 
	transition_count   = 0.0
	bases = ('A','T','C','G')

	transition   = (('C','T'), ('T','C'))
	transversion = (('C','A'), ('T','G'), ('T','A'), ('C','G'))


	for record in tabix.query(chromosom, start, end):
		ref = record[4].upper()
		alt = record[5].upper()
		
		if ref in bases and alt in bases:
			mutation = cannonic_mutation((ref,alt))

			if mutation in transition:
				transition_count += 1 
				hit +=1 
			if mutation in transversion:
				transversion_count += 1 
				hit += 1
		
	return {"transversion":transversion_count/hit*100, "transition" : transition_count/hit*100 }




# GENOM_RANGE_FILE = "/home/bioinfo/DATA/genom/hg19.genome"
# REFSEQ_FILE      = "/home/bioinfo/DATA/refseq/refGene_unique.txt.gz"

# #-----------------------------------------------------------------------------------
# def create_transcript_feature():
# 	''' this function extract exon, introns, cds , 5UTR, 3UTR from refSeqFile ''' 

# 	with gzip.open(REFSEQ_FILE,'r') as file:
# 		reader = csv.reader(io.TextIOWrapper(file, newline=""), delimiter='\t')
# 		output = []
# 		for row in reader:
# 			binn        = row[0]
# 			name        = row[1]
# 			chrom 		= row[2]
# 			strand 		= row[3]
# 			txStart 	= int(row[4])
# 			txEnd 		= int(row[5])
# 			cdsStart 	= int(row[6])
# 			cdsEnd 		= int(row[7])
# 			exonCount 	= int(row[8])
# 			exonStarts 	= [int(i) for i in row[9].split(",") if i is not '']
# 			exonEnds   	= [int(i) for i in row[10].split(",") if i is not '']
# 			score	  	= row[11]
# 			name2	    = row[12]

# 			exonsList 	       	= []
# 			intronsList         = []
# 			cds                 = (cdsStart, cdsEnd)
# 			transcript   		= (txStart, txEnd)
# 			utr5 				= (txStart,cdsStart)
# 			utr3 				= (cdsEnd, txEnd)

# 			# Create exon intervalls
# 			for i in range(exonCount):
# 				start = exonStarts[i]
# 				end   = exonEnds[i]
# 				exonsList.append((start,end-1))

# 			exons      = RangeSet(exonsList)
# 			introns    = RangeSet([(txStart,txEnd-1)])-exons

# 			output.append((chrom,transcript[0],transcript[1], "transcript", name2))
# 			output.append((chrom,utr5[0],utr5[1], "utr5",name2))
# 			output.append((chrom, utr3[0], utr3[1], "utr3" ,name2))
# 			output.append((chrom, cds[0], cds[1], "cds",name2))

# 			for e in exons:
# 				output.append((chrom,e[0],e[1], "exons",name2))

# 			for i in introns:
# 				output.append(( chrom,i[0],i[1], "introns", name2))

# 	return output
# #-----------------------------------------------------------------------------------

# def create_genom_range():
# 	''' Return chromosome size from genoms ''' 
# 	results = []
# 	with open(GENOM_RANGE_FILE,"r") as reader:
# 		for line in reader:
# 			row = line.rstrip().split("\t")
# 			# Only chrom 1 to 22 
# 			if re.match('chr\d{1,2}$',row[0]):
# 				results.append((row[0],int(row[2])))
# 	return results
# #-----------------------------------------------------------------------------------
# def count_mutation_ratio(tabix, chromosom:str, start , end:int):
# 	''' count hit / size feature ''' 
# 	hit  = 0
# 	size = end - start + 1  
# 	for i in tabix.query(chromosom, start, end):
# 		hit+=1 

# 	return float(hit) / float(size) 
# #-----------------------------------------------------------------------------------
# def count_mutation_ratio_normalized(tabix, chromosom:str, start , end:int, patientField = 3):
# 	''' count hit / size * uniqPatient ''' 
# 	hit = 0
# 	size = end - start + 1  
# 	uniqList = set()

# 	for record in tabix.query(chromosom, start, end):
# 		uniqList.add(record[patientField])
# 		hit+=1 

# 	return (float(hit) / float(size)) * len(uniqList)
# #-----------------------------------------------------------------------------------
# def regionOf(gene:str):
# 	''' return region from gene Name ''' 
# 	with gzip.open(REFSEQ_FILE,'r') as file:
# 		reader = csv.reader(io.TextIOWrapper(file, newline=""), delimiter='\t')
# 		for row in reader:
# 			if gene.upper() ==  row[12]:
# 				return (row[2],row[4],row[5])
		
# 	return None

# #----------------------------------------------------------------------------



