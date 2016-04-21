import os 
from snakemake.remote.HTTP import RemoteProvider as HTTPRemoteProvider
HTTP = HTTPRemoteProvider()
configfile: "config.yaml"



rule all:
	input:
		expand("{basedir}/{sample}.html", sample = config["samples"], basedir= config["basedir"])


rule html:
	input:
		"{basedir}/{sample}.feature_variation.bedgraph.png",
		"{basedir}/{sample}.wgs_variation.bedgraph.png"

	output:
		"{basedir}/{sample}.html"
	shell:
		"cp -r templates/* {wildcards.basedir} ;"
		"python3 scripts/create_single_report.py {wildcards.sample} --basedir {wildcards.basedir} --template templates > {output}"


		
rule report:
	input:
		"{basedir}/{sample}.sorted.bed.gz.tbi"
	output:
		"{basedir}/{sample}.pdf"
	shell:
		"touch {output}"

rule tabix:
	input:
		"{basedir}/{sample}.sorted.bed"
	output:
		"{basedir}/{sample}.sorted.bed.gz",
		"{basedir}/{sample}.sorted.bed.gz.tbi"
	shell:
		"bgzip -f {input} && "
		"tabix -f -p bed {input}.gz"

rule wgs_variation:
	input:
		"{basedir}/{sample}.sorted.bed.gz",
	output:
		"{basedir}/{sample}.wgs_variation.bedgraph"
	shell:
		"python3 scripts/wgs_variation.py {input} --g features/hg19_chromosoms.bed --window 100000 -a uniq> {output} 2> /dev/null" 

rule plot_wgs_variation:
	input:
		"{basedir}/{sample}.wgs_variation.bedgraph"
	output:
		"{basedir}/{sample}.wgs_variation.bedgraph.png"
	shell:
		"Rscript scripts/variation_plot.r {input}"
	


rule feature_variation:
	input:
		"{basedir}/{sample}.sorted.bed.gz",
	output:
		"{basedir}/{sample}.feature_variation.bedgraph"
	shell:
		"python3 scripts/feature_variation.py {input} -f features/features.bed > {output} 2> /dev/null" 

rule plot_feature_variation:
	input:
		"{basedir}/{sample}.feature_variation.bedgraph"
	output:
		"{basedir}/{sample}.feature_variation.bedgraph.png"
	shell:
		"Rscript scripts/variation_plot.r {input}"
	


rule sortuniq:
	input:
		"{basedir}/{sample}.bed.gz"
	output:
		"{basedir}/{sample}.sorted.bed"
	shell:
		"zcat {input}|sort -u|bedtools sort -i stdin > {output}"

rule clean:
	params: basedir = config["basedir"]
	shell:
		"rm -f {params.basedir}/*.sorted.bed.gz; "
		"rm -f {params.basedir}/*.sorted.bed.gz.tbi; "
		"rm -f {params.basedir}/*.pdf ; " 
		"rm -f {params.basedir}/*.bedgraph ; "
		"rm -f {params.basedir}/*.png ; "

		" exit 0"

