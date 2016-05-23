import config 
import os
#Convert icgc tabular snp to bed file 
#chr start end patient reference alternative 

# Get features base names
features_base_names = [os.path.basename(i)[:-4] for i in config.features]

# Create output directory 



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
		"zcat {input}|sort -u|bedtools sort -i stdin | bgzip > {output};"
		"tabix -p bed {output}"

# Create tabix index 
rule tabix:
	input:
		"{name}.bed.gz"
	output:
		"{name}.bed.gz.tbi"
	shell:
		"tabix -p bed {input}"


# Count mutation rate 
rule count :
	input:
		"{name}.bed.gz",
	output:
		"{name}.count"
	shell:
		"python3 scripts/sliding_window.py {input} -g {config.genome_sizes} -w {config.mutation_range} > {output}"

# Compute signature 
rule signature:
	input:
		"{name}.bed.gz"
	output:
		"{name}.signature"
	shell:
		"python3 scripts/signature.py {input} > {output}"

rule plot_count:
	input:
		"{name}.count"
	output:
		"{name}.count.png"
	shell:
		"Rscript scripts/plot_coverage.r {input} {output}"

rule plot_signature:
	input:
		"{name}.signature"
	output:
		"{name}.signature.png"
	shell:
		"Rscript scripts/plot_signature.r {input} {output}"

# Compute stats 
rule stats:
	input:
		"{name}.bed.gz"
	output:
		"{name}.stat"
	shell:
		"python3 scripts/stats.py {input} > {output}"


# Split features
rule split:
	input:
		src  ="{name}.bed.gz",
		fpath="features/{feature_name}.bed"
	output:
		"{name}.{feature_name}.bed.gz"
	shell:
		"bedtools intersect -a {input.src} -b {input.fpath} |bgzip > {output}"

# Compute feature count 
rule feature_count:
	input:
		expand("{fpath}", fpath=config.features)
	output:
		"features.coverage"
	run:
		for f in input:
			name = os.path.basename(f)[:-4]
			shell("echo '{name}\t'$(bedtools sort -i {f}|bedtools merge -i stdin|awk '{{print $3-$2}}'|paste -sd+|bc) >> {output}")




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
		"echo -e '#chromosome\tstart\tend\tcount\tcannCount\t{params.feature_names}'> {output};" 
		# annotate peaks 
		"bedtools annotate -counts -i {input} -files {params.feature_paths} >> {output}" 


rule annotate_cluster:
	input:
		"{name}.cluster.bed"
	output:
		"{name}.cluster.annotate.bed",
	params:
		# Get features path in one line separated by tabular 
		feature_paths = "\t".join(file for file in config.features),
		# Get feature names in one line separated by tabular
		feature_names = "\t".join(os.path.basename(file)[:-4] for file in config.features),

	shell:
		# Print first header
		"echo -e '#chromosome\tstart\tend\tcount\tcannCount\t{params.feature_names}'> {output};" 
		# annotate only cluster allowed by config 
		"cat {input}|awk '$4 > {config.c_count} && $5 > {config.p_count}'|bedtools annotate -i stdin -files {params.feature_paths} >> {output}" 

rule annotate_entropy_cluster:
	input:
		src="{name}.bed.gz",
		region="{name}.cluster.annotate.bed"

	output:
		"{name}.cluster.annotate.entropy.bed",
	shell:
		"python3 scripts/bed_entropy.py {input.src} -r {input.region} > {output}"
	

rule create_report:
	input:
		"{name}.stat",
		"{name}.cluster.annotate.entropy.bed",
		"{name}.peaks.annotate.bed",
		"{name}.signature.png",
		"{name}.count.png"

	output:
		"{name}.html"
	shell:
		"python3 scripts/create_single_report.py {wildcards.name} --basedir . --template_dir templates > {output};"
		



	


# rule create_feature:
# 	input:
# 		src="{name}.wgs.vcf.gz",
# 		fpath="features/{feature}.bed"
# 	output:
# 		"{name}.{feature}.vcf.gz"
# 	shell:
# 		"bedtools intersect -a {input.src} -b {input.fpath} |bgzip > {output};"


