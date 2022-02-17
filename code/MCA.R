library(FactoMineR)

farmers <- read.csv("../results/farmers.csv")
exposures <- farmers[9:14]
exposures <- as.data.frame(lapply(exposures, factor))
expo_mca <- MCA(exposures)

pdf(file="../results/MCA_exposure.pdf")
plotellipses(expo_mca)
dev.off()
