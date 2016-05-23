library(RColorBrewer)

filename = "exons.coverage"

args <- commandArgs(trailingOnly = TRUE)
filename = args[1]
output   = args[2]

data = read.csv(filename, sep="\t", header=F)
genome = subset(data, V1=="genome")


png(output, width = 480, height = 480)
par(mar=c(5,5,5,5))
pie(genome$V5, col = c("#4BC0C0","#FFCE56"), lty=1, 
    labels = paste0(c("uncover\n", "cover\n"), round(genome$V5 * 100,2), "%"), 
    border = c("white"), 
    main = basename(output)
    )

