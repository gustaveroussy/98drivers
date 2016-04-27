
library(fmsb)
library(RColorBrewer)

args <- commandArgs(trailingOnly = TRUE)
filename = args[1]

#filename = "all.txt"

raw = read.csv(filename, header = T, sep = "\t")
maxmin = subset(raw, F)
#remove first col 
maxmin[,1] = NULL 
maxmin[1,] = rep(100, ncol(maxmin))
maxmin[2,] = rep(0, ncol(maxmin))

dat = raw[,2:ncol(raw)] * 100.0

dat <- rbind(maxmin,dat)

png(paste0(dirname(filename),"/",sub("bedgraph","png",basename(filename))))

if (nrow(dat) > 5)
{
  bgColor = NULL;
} else 
{
  bgColor = adjustcolor(brewer.pal(nrow(dat),"Pastel1"), alpha.f = 0.5)
}

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


legend("topright",as.vector(raw[,1]), fill =brewer.pal(nrow(dat),"Pastel1"))

