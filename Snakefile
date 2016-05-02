import config 
import re 
import os 

# # Create sample names
# samples = [] 
# for filename in os.listdir(config.basedir):
# 	path = os.path.join(config.basedir, filename)
# 	if re.match(r'.+.bed.gz', filename) and os.path.isfile(path):
# 		samples.append(re.sub(r'\.bed.gz','',filename))



# # Create unknown feature 
# shell("rm -f {featuredir}/unknown.bed".format(featuredir = config.featuredir))

# Create feature names
features = []
paths = []


for filename in os.listdir(config.featuredir):
	path = os.path.join(config.featuredir, filename)
	if re.match(r'.+.bed', filename) and os.path.isfile(path) and filename != "unknown.bed":
		features.append(re.sub(r'\.bed','',filename))
		paths.append(path)


shell("cat {file} > {featuredir}/unknown.bed".format(file = " ".join(paths), featuredir = config.featuredir ))
features.append("unknown")


# Create output dir 
if not os.path.exists("output/"):
    os.makedirs("output/")








# rule all:
# 	input:
# 		#expand("{outputdir}/{sample}.{feature}.info", outputdir = config.outputdir, feature = features,sample = samples),
# 		expand("{outputdir}/Bone.info.plot", outputdir = config.outputdir, sample = samples) 



rule html:
	input :
		"{sample}.bed.gz",
		"output/{sample}.wgs.peaks.annotated.bed",
		lambda w : expand("output/{sample}.{feature}.signature.png", feature = features, sample = w.sample)

	output:
		"output/{sample}.html" 
	shell:
		"cp -r templates/* output/;"
		"python3 scripts/create_single_report.py {wildcards.sample} --basedir output --template templates > {output}"



# Filter and sort  
rule sortuniq:
	input:
		"{sample}.bed.gz"
	output:
		"output/{sample}.wgs.bed.gz"
	shell:
		"zcat {input}|sort -u|bedtools sort -i stdin | bgzip > {output} "


# Create tabix index 
rule tabix : 
	input: 
		"output/{sample}.wgs.bed.gz"	
	output:
		"output/{sample}.wgs.bed.gz.tbi" 
	shell:
		"tabix -p bed {input}"


# Split source file into sub file for each features 
rule create_feature:
	input : 
		src     = "output/{sample}.wgs.bed.gz" ,
		fpath   = "output/{feature}.sorted.bed"
	output : 
		"output/{sample}.{feature}.bed.gz"

	run:
		if wildcards.feature == "unknown":
			shell("bedtools subtract -a {input.src} -b {input.fpath} |bgzip > {output}")
		else:
			shell("bedtools intersect -a {input.src} -b {input.fpath} |bgzip > {output}")


# Lanch analysis on each bed.gz 
rule analysis:
	input:
		"output/{sample}.{feature}.bed.gz"
	output:
		"output/{sample}.{feature}.info"
	shell:
		"python3 scripts/analysis.py {input} > {output}"


# Plot signature for each features 
rule plot_signature:
	input: 
		"output/{sample}.{feature}.info"
	output:
		"output/{sample}.{feature}.signature.png"
	shell:
		"Rscript scripts/signature_plot.r {input} {output}" 




# Concatenate analyis feature info into one file 
rule cat_info: 
	input:
		lambda w : expand("output/{sample}.{feature}.info", feature = features, sample = w.sample)
	output:
		"output/{sample}.all.info"
	shell:
		"awk 'FNR>1 || NR ==1' {input} > {output}"


# sort features 
rule sort_feature:
	input:
		"features/{feature}.bed"
	output:
		"output/{feature}.sorted.bed"
	shell:
		"bedtools sort -i {input} > {output} ; "


# compute coverage features 
rule coverage_feature:
	input:
		"output/{feature}.sorted.bed"
	output:
		"output/{feature}.coverage"
	shell:
		"bedtools genomecov -i {input} -max 1 > {output}"


# detect peaks 
rule detect_peak:
	input:
		"output/{sample}.wgs.bed.gz"
	output:
		"output/{sample}.wgs.peaks.bed"
	shell: # Detect peaks with more than 4 patients same 
		"source scripts/detect_peaks.sh {input} 4 > {output}"

rule annotate_peak:
	input:
		peak    = "output/{sample}.wgs.peaks.bed",
		fpath   =expand("output/{feature}.sorted.bed", feature=features)
	
	params:
		fnames  = " ".join(features)
	output:
		"output/{sample}.wgs.peaks.annotated.bed"
	shell: 
		"bedtools annotate -names {params.fnames} -i {input.peak} -files {input.fpath} > {output}"



rule show_features:
	run:
		print(features)



rule clean :
	shell:
		"rm -rf output/"


# rule plot_info : 
# 	input:
# 		expand("{outputdir}/Bone.{feature}.info", outputdir = config.outputdir, feature = features)

# 	output:
# 		config.outputdir+"/Bone.info.plot"