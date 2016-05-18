import config 
import os
#Convert icgc tabular snp to bed file 
#chr start end patient reference alternative 

rule icgc2bed:
	input:
		"{name}.tsv.gz"
	output:
		"{name}.unsorted.bed.gz"
	shell:
		"icgc2bed {input}|gzip > {output}"

# sort unsorted.bed.gz file and bgzip for tabix 
rule sort_bed:
	input:
		"{name}.unsorted.bed.gz"
	output:
		"{name}.bed.gz"
	shell:
		"zcat {input}|sort -u|bedtools sort -i stdin | bgzip > {output}"

# Create tabix index 
rule tabix:
	input:
		"{name}.bed.gz"
	output:
		"{name}.bed.gz.tbi"
	shell:
		"tabix -p bed {input}"

rule detect_cluster:
	input:
		"{name}.bed.gz"
	output:
		"{name}.cluster.bed"
	shell:
		"bedtools merge -d {config.c_distance} -i {input} -c 4 -o count,count_distinct | sort -k 4,5 -r -n> {output}"

rule detect_peaks:
	input:
		"{name}.cluster.bed"
	output:
		"{name}.peaks.bed"
	shell:
		"cat {input}|awk '$3-$2<{config.p_width} && $4 > {config.p_count} && $5 > {config.p_distinct_count} {{print $0}}'>{output}"


rule annotate_peaks:
	input:
		"{name}.peaks.bed"
	output:
		"{name}.peaks.annotate.bed"

	params:
		# Get features path in one line separated by tabular 
		feature_paths = "\t".join(file for file in config.features),
		# Get feature names in one line separated by tabular
		feature_names = "\t".join(os.path.basename(file)[:-4] for file in config.features),

	shell:
		# print first header
		"echo -e '#chromosome\tstart\tend\tcount\t{params.feature_names}'> {output};" 
		# annotate peaks 
		"bedtools annotate -counts -i {input} -files {params.feature_paths} >> {output}" 


rule annotate_cluster:
	input:
		"{name}.cluster.bed"
	output:
		"{name}.cluster.annotate.bed"
	params:
		# Get features path in one line separated by tabular 
		feature_paths = "\t".join(file for file in config.features),
		# Get feature names in one line separated by tabular
		feature_names = "\t".join(os.path.basename(file)[:-4] for file in config.features),

	shell:
		# Print first header
		"echo -e '#chromosome\tstart\tend\tfraction\t{params.feature_names}'> {output};" 
		# annotate only cluster allowed by config 
		"cat {input}|awk '$4 > {config.c_count} && $5 > {config.p_count}'|bedtools annotate -i stdin -files {params.feature_paths} >> {output}" 




# rule create_feature:
# 	input:
# 		src="{name}.wgs.vcf.gz",
# 		fpath="features/{feature}.bed"
# 	output:
# 		"{name}.{feature}.vcf.gz"
# 	shell:
# 		"bedtools intersect -a {input.src} -b {input.fpath} |bgzip > {output};"


