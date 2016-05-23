
library(fmsb)
library(RColorBrewer)

args <- commandArgs(trailingOnly = TRUE)
filename = args[1]
output   = args[2]

color_theme = "Pastel1"

raw    = read.csv(filename, header = T, sep = "\t") 
total  = 100

maxmin = subset(raw,F)

maxmin[1,] = rep(100, ncol(maxmin))
maxmin[2,] = rep(0, ncol(maxmin))
# 
dat = raw[,1:ncol(raw)] * 100 
# 
dat <- rbind(maxmin,dat)
# 
png(output)
# 
if (nrow(dat) > 3)
{
  bgColor = NULL;
} else
{
  bgColor = adjustcolor(brewer.pal(nrow(dat),color_theme), alpha.f = 0.5)
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
           pcol  = brewer.pal(nrow(dat),color_theme),
          vlcex = 0.9,
           seg=3,
          paxislabels = rep("salut",6),
           title=basename(filename));


legend("topright", NULL, legend=colnames(raw), fil=brewer.pal(nrow(dat),color_theme))


