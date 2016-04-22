filename = "/home/bioinfo/Dev/gustaveRoussy/datatest/results/Pancreas.wgs_signature.bedgraph"

data = read.table(filename, sep="\t", header=F, skip=1, dec = ".")





test = head(data[,c(4,5)], 500)



barplot(t(as.matrix(test)))


