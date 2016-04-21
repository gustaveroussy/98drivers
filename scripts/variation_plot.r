
args <- commandArgs(trailingOnly = TRUE)
filename = args[1]

# filename = "/home/bioinfo/Dev/gustaveRoussy/datatest/Bone.wgs_variation.bedgraph"

data = read.table(filename, sep="\t", header=F, skip=1, dec = ".")

data$V5 = as.factor(data$V5)

png(paste0(dirname(filename),"/",basename(filename),".png"))
boxplot(log10(data$V4 +1) ~ data$V5, main = basename(filename))

dev.off()