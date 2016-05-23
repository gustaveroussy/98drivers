

# filename = "peaks_range.tsv"
# 
# r = read.table(filename, header = T, as.is = T)
# r = r[1:10,]
# par(mfrow = n2mfrow(nrow(r)))
# par(mar = c(1,1,1,1))
# for (index in 1:nrow(r))
# {
#   

 png("test.png", width = 300, height = 300)
  par(mfrow=c(1,1), xpd=NA)
  par(mar = c(0,0,0,0),xaxs="i", yaxs="i", oma = c(0,0,0,0))
  line = r [index,]
  x.dat = as.numeric(line[,-c(1,2)])
  bgcol = "#4bc0c0"
  barplot(x.dat, space =0, col = adjustcolor(bgcol,0.5), border= bgcol,axes=FALSE)
  x.est <- fitdistr(x.dat, "exponential")$estimate
  lines(spline(x.dat), lwd=4, lty=1, col="#FF6384") 
  
  #legend("topright", paste(r[index,1],r[index,2],sep = "-"), bty = "n") 
  #legend("topright",paste("\npeaks",r[index,3]), bty = "n") 
  
  dev.off()
  
# }


