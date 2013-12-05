// This R script does CCA analysis on 2 sets of distributed representations 
// of words

require(CCA)

distRep1 <- read.delim("endWordsMat.tsv", sep="\t", header=F)

distRep2 <- read.delim("freWordsMat.tsv", sep="\t", header=F)

ccaEngFre <- cc(distRep1, distRep2)

// printing correlations
ccaEngFre$cor