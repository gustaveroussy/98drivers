
library(fmsb)
library(RColorBrewer)

args <- commandArgs(trailingOnly = TRUE)
filename = args[1]
output   = args[2]
# 
#filename = "p.info"


raw    = read.csv(filename, header = T, sep = "\t")
subraw = raw[c("CA","CG","CT","TA","TC","TG")] / raw$canno_mutation_count
total  = raw["canno_mutation_count"]

maxmin = subset(subraw,F)

maxmin[1,] = rep(100, ncol(maxmin))
maxmin[2,] = rep(0, ncol(maxmin))
# 
dat = subraw[,1:ncol(subraw)] * 100 
# 
dat <- rbind(maxmin,dat)
# 
 png(output)
# 
if (nrow(dat) > 5)
{
  bgColor = NULL;
} else
{
  bgColor = adjustcolor(brewer.pal(nrow(dat),"Pastel1"), alpha.f = 0.5)
}

par(mfrow=c(1,1))
radarchart(dat,
           axistype=0,
           pty=16 ,
           plty=1,
           plwd = 3,
           axislabcol="grey",
           cglty=1,
           cglwd = 0.4,
           cglcol = "gray",
           pfcol = bgColor,
           pcol  = brewer.pal(nrow(dat),"Pastel1"),
          vlcex = 0.9,
           seg=3,
          paxislabels = rep("salut",6),
           title=basename(filename))
# 
# 
# legend("topright",as.vector(raw[,1]), fill =brewer.pal(nrow(dat),"Pastel1"))

