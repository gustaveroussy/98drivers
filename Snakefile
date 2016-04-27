import os 
import glob
from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider
HTTP = HTTPRemoteProvider()
configfile: "config.yaml"

# Create inputs from filename in basedir 
samples = [re.sub(r'\.bed.gz','',i) for i in os.listdir(config["basedir"]) if re.match(r'.+.bed.gz', i) and os.path.isfile(os.path.join(config["basedir"],i))]


# Create output dir 
if not os.path.exists(config["resultdir"]):
    os.makedirs(config["resultdir"])


# =================================== ALL FINAL FILES YOU WANT 
rule all:
	input:
		expand("{resultdir}/{sample}.html", resultdir= config["resultdir"], sample = samples),
		config["resultdir"]+"/feature.info"		


# =================================== REPORT 

rule html:
	input:
		"{resultdir}/{sample}.wgs_variation.png",
		"{resultdir}/{sample}.wgs_signature.png",
		"{resultdir}/{sample}.wgs_peak.max.bedgraph",
		"{resultdir}/{sample}.wgs_variation.max.bedgraph",
		"{resultdir}/{sample}.info",
		"{resultdir}/feature.info"
		


	output:
		"{resultdir}/{sample}.html"
	shell:
		"cp -r templates/* {wildcards.resultdir} ;"
		"python3 scripts/create_single_report.py {wildcards.sample} --basedir {wildcards.resultdir} --template templates > {output}"


rule stat_variant:
	input:
		"{resultdir}/{sample}.sorted.bed.gz"
	output:
		"{resultdir}/{sample}.info"
	shell:
		"python3 scripts/stat_variant.py {input} > {output}"

rule stat_feature:
	input:
		config["features"]
	output:
		"{resultdir}/feature.info"
	shell:
		"python3 scripts/stat_feature.py {input} > {output}"

# =================================== TABIX 

rule tabix:
	input:
		"{resultdir}/{sample}.sorted.bed"
	output:
		"{resultdir}/{sample}.sorted.bed.gz",
		"{resultdir}/{sample}.sorted.bed.gz.tbi"
	shell:
		"bgzip -f {input} && "
		"tabix -f -p bed {input}.gz"

# =================================== SORT AND FILTER  

rule sortuniq:
	params : basedir = config["basedir"]
	input:
		config["basedir"] + "/{sample}.bed.gz"
	output:
		"{resultdir}/{sample}.sorted.bed"
	shell:
		"zcat {input}|sort -u|bedtools sort -i stdin > {output}"

# =================================== ANALYSIS   

rule wgs_variation:
	input:
		"{resultdir}/{sample}.sorted.bed.gz",
	output:
		"{resultdir}/{sample}.wgs_variation.bedgraph",

	shell:
		"python3 scripts/variation.py wgs {input} --g features/genom.bed --window 100000 -a uniq> {output} 2> /dev/null;"


rule wgs_variation_max:
	input:
		"{resultdir}/{sample}.wgs_variation.bedgraph",
	output:
		"{resultdir}/{sample}.wgs_variation.max.bedgraph",

	shell:
		"source scripts/max_bedgraph.sh {input} {config[wgs_variation_limit]} > {output} " 



rule wgs_peaks_max:
	input:
		"{resultdir}/{sample}.sorted.bed.gz"
	output:
		"{resultdir}/{sample}.wgs_peak.max.bedgraph"
	shell:
		"source scripts/detect_peaks.sh {input} {config[wgs_peaks_limit]} > {output}"



rule plot_wgs_variation:
	input:
		"{resultdir}/{sample}.wgs_variation.bedgraph"
	output:
		"{resultdir}/{sample}.wgs_variation.png"
	shell:
		"Rscript scripts/variation_plot.r {input}"
	
rule wgs_signature:
	input:
		"{resultdir}/{sample}.sorted.bed.gz",
	output:
		"{resultdir}/{sample}.wgs_signature.bedgraph"
	shell:
		"python3 scripts/signature.py {input}  > {output} 2> /dev/null" 

rule feature_signature:
	input:
		"{resultdir}/{sample}.sorted.bed.gz",
	output:
		"{resultdir}/{sample}.feature_signature.bedgraph"
	shell:
		"python3 scripts/signature.py {input} -f {config[features]} > {output} 2> /dev/null" 



rule plot_signature:
	input:
		"{resultdir}/{sample}.wgs_signature.bedgraph",
		"{resultdir}/{sample}.feature_signature.bedgraph",
	output:
		"{resultdir}/{sample}.wgs_signature.png",
		"{resultdir}/{sample}.feature_signature.png",

	shell:
		"Rscript scripts/signature_plot.r {input[0]}  > {output[0]};" 
		"Rscript scripts/signature_plot.r {input[1]}  > {output[1]};" 


# rule feature_variation:
# 	input:
# 		"{resultdir}/{sample}.sorted.bed.gz",
# 	output:
# 		"{resultdir}/{sample}.feature_variation.bedgraph",

# 	shell:
# 		"python3 scripts/variation.py feature {input} -f {config[features]} > {output} 2> /dev/null" 




# rule plot_feature_variation:
# 	input:
# 		"{resultdir}/{sample}.feature_variation.bedgraph"
# 	output:
# 		"{resultdir}/{sample}.feature_variation.bedgraph.png"
# 	shell:
# 		"Rscript scripts/variation_plot.r {input}"
	

# =================================== ANALYSIS   

rule clean:
	shell:
		"rm -rf {config[resultdir]}"
		" exit 0"

