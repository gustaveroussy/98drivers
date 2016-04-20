import os 

configfile: "config.yaml"

rule all:
	input:
		expand("{basedir}/{sample}.pdf", sample = config["samples"], basedir= config["basedir"]) 
		
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



rule sortuniq:
	input:
		"{basedir}/{sample}.bed.gz"
	output:
		"{basedir}/{sample}.sorted.bed"
	shell:
		"zcat {input}|sort -u|bedtools sort -i stdin > {output}"

rule clear:
	params: basedir = config["basedir"]
	shell:
		"rm -f {params.basedir}/*.pdf &&"
		"rm -f {params.basedir}/*.sorted.bed.gz && "
		"rm -f {params.basedir}/*.sorted.bed.gz.tbi && "
