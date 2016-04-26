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


def count_mutation_ratio_std(tabix, chromosom:str, start , end:int):
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

def count_mutation_ratio_bartlett(tabix, chromosom:str, start , end:int):
	size = end - start
	score = 0  
	for record in tabix.query(chromosom, start, end):
		s = int(record[1]) - start 
		score += bartlett_window_coeff(s, size)

	return score / size * 100 

def count_mutation(tabix, chromosom:str, start , end:int, algorithm = "std"):
	if algorithm == "std":
		return count_mutation_ratio_std(tabix,chromosom, start, end)

	if algorithm == "uniq":
		return count_mutation_ratio_uniq(tabix,chromosom, start, end)

	if algorithm =="bartlett":
		return count_mutation_ratio_bartlett(tabix,chromosom,start,end)

	return -1 



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



def bartlett_window_coeff(x , width ):
	N = width  
	L = N - 1 
	return 1 - abs((x - (N-1)/2) / (L/2)) 





