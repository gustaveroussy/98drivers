
args <- commandArgs(trailingOnly = TRUE)
filename = args[1]

# filename = "/home/bioinfo/Dev/gustaveRoussy/datatest/Pancreas.feature_variation"

data = read.table(filename, sep="\t", header=F, skip=1, dec = ".")

data$V5 = as.factor(data$V5)
data = subset(data, V4 > 0)

png(paste0(dirname(filename),"/",sub("bedgraph","png",basename(filename)) ))
boxplot(log10(data$V4+1)  ~ data$V5, main = basename(filename))
invisible(dev.off())
