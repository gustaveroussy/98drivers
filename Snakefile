import config 
import re 
import os 

# Create sample names
samples = [] 
for filename in os.listdir(config.basedir):
	path = os.path.join(config.basedir, filename)
	if re.match(r'.+.bed.gz', filename) and os.path.isfile(path):
		samples.append(re.sub(r'\.bed.gz','',filename))



# Create unknown feature 
shell("rm -f {featuredir}/unknown.bed".format(featuredir = config.featuredir))

# Create feature names
features = []
paths = []
for filename in os.listdir(config.featuredir):
	path = os.path.join(config.featuredir, filename)
	if re.match(r'.+.bed', filename) and os.path.isfile(path):
		features.append(re.sub(r'\.bed','',filename))
		paths.append(path)

features.append("unknown")

shell("cat {file} > {featuredir}/unknown.bed".format(file = " ".join(paths), featuredir = config.featuredir ))


# Create output dir 
if not os.path.exists(config.outputdir):
    os.makedirs(config.outputdir)








rule all:
	input:
		#expand("{outputdir}/{sample}.{feature}.info", outputdir = config.outputdir, feature = features,sample = samples),
		expand("{outputdir}/Bone.info.plot", outputdir = config.outputdir, sample = samples) 




rule sortuniq:
	input:
		config.basedir + "/{sample}.bed.gz"
	output:
		"{outputdir}/{sample}.wgs.bed.gz"
	shell:
		"zcat {input}|sort -u|bedtools sort -i stdin | bgzip > {output} "



rule analysis:
	input:
		"{outputdir}/{sample}.{feature}.bed.gz"
	output:
		"{outputdir}/{sample}.{feature}.info"
	shell:
		"python3 scripts/analysis.py {input} > {output}"





rule create_feature: 
	input:
		"{outputdir}/{sample}.wgs.bed.gz",
	output:
		"{outputdir}/{sample}.{feature}.bed.gz",

	run:
		if wildcards.feature == "unknown":

			shell("bedtools subtract -a {input} -b {config.featuredir}/{wildcards.feature}.bed|bgzip > {output}")
		else:
			shell("bedtools intersect -a {input} -b {config.featuredir}/{wildcards.feature}.bed|bgzip > {output}")


rule plot_signature:
	input: 
		"{outputdir}/{sample}.{feature}.info"
	output:
		"{outputdir}/{sample}.{feature}.signature.png"
	shell:
		"Rscript scripts/signature_plot.r {input} {output}" 


rule plot_info : 
	input:
		expand("{outputdir}/Bone.{feature}.info", outputdir = config.outputdir, feature = features)

	output:
		config.outputdir+"/Bone.info.plot"