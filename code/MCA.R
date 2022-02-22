library(FactoMineR)

farmers <- read.csv("../results/farmers.csv")
exposures <- farmers[9:14]
exposures <- as.data.frame(lapply(exposures, factor))
variable_exposures <- exposures[exposures$mixed_or_applied == 1,]
expo_mca <- MCA(variable_exposures[,-1], graph=FALSE)

pdf(file="../results/MCA_exposure.pdf")
plotellipses(expo_mca)
dev.off()
