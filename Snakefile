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



rule all:
	input:
		expand("{resultdir}/{sample}.html", resultdir= config["resultdir"], sample = samples),
		expand("{resultdir}/{sample}.wgs_variation.bedgraph.png", resultdir= config["resultdir"], sample = samples),
		expand("{resultdir}/{sample}.feature_variation.bedgraph.png", resultdir= config["resultdir"], sample = samples),
		expand("{resultdir}/{sample}.wgs_signature.bedgraph", resultdir= config["resultdir"], sample = samples)



rule html:
	input:
		"{resultdir}/{sample}.feature_variation.bedgraph.png",
		"{resultdir}/{sample}.wgs_variation.bedgraph.png"

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

rule tabix:
	input:
		"{resultdir}/{sample}.sorted.bed"
	output:
		"{resultdir}/{sample}.sorted.bed.gz",
		"{resultdir}/{sample}.sorted.bed.gz.tbi"
	shell:
		"bgzip -f {input} && "
		"tabix -f -p bed {input}.gz"

rule wgs_variation:
	input:
		"{resultdir}/{sample}.sorted.bed.gz",
	output:
		"{resultdir}/{sample}.wgs_variation.bedgraph"
	shell:
		"python3 scripts/wgs_variation.py {input} --g features/genom.bed --window 100000 -a uniq> {output} 2> /dev/null" 

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
		"python3 scripts/wgs_signature.py {input} --g features/genom.bed --window 100000 > {output} 2> /dev/null" 


rule feature_variation:
	input:
		"{resultdir}/{sample}.sorted.bed.gz",
	output:
		"{resultdir}/{sample}.feature_variation.bedgraph"
	shell:
		"python3 scripts/feature_variation.py {input} -f {config[features]} > {output} 2> /dev/null" 




rule plot_feature_variation:
	input:
		"{resultdir}/{sample}.feature_variation.bedgraph"
	output:
		"{resultdir}/{sample}.feature_variation.bedgraph.png"
	shell:
		"Rscript scripts/variation_plot.r {input}"
	


rule sortuniq:
	params : basedir = config["basedir"]
	input:
		config["basedir"] + "/{sample}.bed.gz"
	output:
		"{resultdir}/{sample}.sorted.bed"
	shell:
		"zcat {input}|sort -u|bedtools sort -i stdin > {output}"

rule clean:
	params: resultdir = config["resultdir"]
	shell:
		"rm -rf {resultdir}"
		" exit 0"

