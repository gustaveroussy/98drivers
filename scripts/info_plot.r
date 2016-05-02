library(RColorBrewer)


#filename = "test.feature.info"


args <- commandArgs(trailingOnly = TRUE)
filename = args[1]
output   = args[2]

raw      = read.csv(filename, header = T, sep = "\t")

raw      = raw[order(raw$feature),]

niceplot = function(data,names, main)
{
  par(lwd=1.5)
  
  barplot(data, 
          names.arg = names,
          col = adjustcolor(brewer.pal(nrow(raw),"Pastel2"), alpha.f = 0.5),
          border= brewer.pal(nrow(raw),"Pastel2"),
          space =0.2, 
          axes = F,
          col.axis = "grey10", 
          main=main)
  axis(2, col="light gray", tck = 1, las = 2 , col.axis = "grey10" )
  
  
}


png(output)
par(mfrow=c(1,3))


niceplot(raw$size, raw$feature, "size in bases")
niceplot(raw$mutation_count , raw$feature, "raw mutation count" )
niceplot(raw$mutation_count/raw$size, raw$feature, "ratio")





