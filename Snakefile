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
		expand("{resultdir}/{sample}.wgs_variation.bedgraph.png", resultdir= config["resultdir"], sample = samples),
		expand("{resultdir}/{sample}.feature_variation.bedgraph.png", resultdir= config["resultdir"], sample = samples),


# =================================== REPORT 

rule html:
	input:
		"{resultdir}/{sample}.feature_variation.bedgraph.png",
		"{resultdir}/{sample}.wgs_variation.bedgraph.png",
		"{resultdir}/{sample}.wgs_peak.bedgraph",
		"{resultdir}/{sample}.stat"


	output:
		"{resultdir}/{sample}.html"
	shell:
		"cp -r templates/* {wildcards.resultdir} ;"
		"python3 scripts/create_single_report.py {wildcards.sample} --basedir {wildcards.resultdir} --template templates > {output}"


		
rule report:
	input:
		"{resultdir}/{sample}.sorted.bed.gz.tbi"
	output:
		"{resultdir}/{sample}.pdf"
	shell:
		"touch {output}"

rule stat:
	input:
		"{resultdir}/{sample}.sorted.bed.gz"
	output:
		"{resultdir}/{sample}.stat"
	shell:
		"python3 scripts/stats.py {input} > {output}"

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
		"{resultdir}/{sample}.wgs_variation.max.bed",

	shell:
		"python3 scripts/variation.py wgs {input} --g features/genom.bed --window 100000 -a uniq> {output[0]} 2> /dev/null;"
		"source scripts/max_bedgraph.sh {output[0]} {config[wgs_variation_limit]} > {output[1]} " 


rule wgs_peaks:
	input:
		"{resultdir}/{sample}.sorted.bed.gz"
	output:
		"{resultdir}/{sample}.wgs_peak.bedgraph"
	shell:
		"source scripts/detect_peaks.sh {input} {config[wgs_peaks_limit]} > {output}"





rule plot_wgs_variation:
	input:
		"{resultdir}/{sample}.wgs_variation.bedgraph"
	output:
		"{resultdir}/{sample}.wgs_variation.bedgraph.png"
	shell:
		"Rscript scripts/variation_plot.r {input}"
	
rule wgs_signature:
	input:
		"{resultdir}/{sample}.sorted.bed.gz",
	output:
		"{resultdir}/{sample}.wgs_signature.bedgraph"
	shell:
		"python3 scripts/wgs_signature.py {input} --g features/genom.bed --window 100000 -a uniq  > {output} 2> /dev/null" 


rule feature_variation:
	input:
		"{resultdir}/{sample}.sorted.bed.gz",
	output:
		"{resultdir}/{sample}.feature_variation.bedgraph",

	shell:
		"python3 scripts/variation.py feature {input} -f {config[features]} > {output} 2> /dev/null" 




rule plot_feature_variation:
	input:
		"{resultdir}/{sample}.feature_variation.bedgraph"
	output:
		"{resultdir}/{sample}.feature_variation.bedgraph.png"
	shell:
		"Rscript scripts/variation_plot.r {input}"
	

# =================================== ANALYSIS   

rule clean:
	shell:
		"rm -rf {config[resultdir]}"
		" exit 0"

