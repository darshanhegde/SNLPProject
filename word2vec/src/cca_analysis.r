// This R script does CCA analysis on 2 sets of distributed representations 
// of words

require(CCA)

years = c("1850", "1870", "1890", "1910", "1930", "1950", "1970", "1990", "2009");

all_year_combs = combn(years, 2)

for(idx in 1:(length(all_year_combs)/2)){

	year1 = all_year_combs[1,idx];
	
	year2 = all_year_combs[2,idx];
	
	print(paste("computing CCA for: ", year1, " ", year2));

	distRep1 <- read.delim(paste("pair_", year1, "_", year2, "_", year1, ".tsv", sep=""), sep="\t", header=F);

	distRep2 <- read.delim(paste("pair_", year1, "_", year2, "_", year2, ".tsv", sep=""), sep="\t", header=F);
	
	ccaEngFre <- cc(distRep1, distRep2);

	avgCCA <- mean(ccaEngFre$cor);
	
	print(paste(year1, " ", year2, " ", as.character(avgCCA)))

}

