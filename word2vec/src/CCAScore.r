require("CCA")

distRep1 <- read.delim('CCAFileOne.tsv', sep='\t', header=F); 

distRep2 <- read.delim('CCAFileTwo.tsv', sep='\t', header=F); 

ccaEngFre <- cc(distRep1, distRep2); 

avgCCA <- mean(ccaEngFre$cor); print(avgCCA);

print(paste("Avg CCA Score:", avgCCA))