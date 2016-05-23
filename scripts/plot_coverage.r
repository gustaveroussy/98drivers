color = "#4bc0c0"
color_light = adjustcolor(color, alpha.f = 1)


args <- commandArgs(trailingOnly = TRUE)
filename = args[1]
output   = args[2]


data = read.table(filename,sep="\t", as.is=T, header = F)
sortedData = sort(data$V4)


png(output)
par(bty = 'n', col.axis = "darkgray") 
plot(sortedData,
     pch=20, 
     lwd=2,
     type="l",
     cex=0.2, 
     col=color_light,
     ylab = "Number of mutation per Mb",
     bg="#A6D5D533",
     main = "Number of somatic mutations "
     )

abline(v=seq.int(0,max(sortedData),1000), h=seq.int(0,max(sortedData),1000), col="gray90" )

axis(1, labels = FALSE, col = "darkgray")
axis(2, labels = FALSE, col = "darkgray")
dev.off()