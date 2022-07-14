# Title     : interface.R
# Objective : Interface
# Created by: greyhypotheses
# Created on: 14/07/2022

source(file = 'R/missing/Steps.R')


# data sources
files <- list.files(path = file.path(getwd(), 'warehouse', 'missing', 'disaggregates'),
                    full.names = TRUE)


# in parallel
cores <- parallel::detectCores() - 2
doParallel::registerDoParallel(cores = cores)
clusters <- parallel::makeCluster(cores)
X <- parallel::clusterMap(clusters, fun = Steps, files, USE.NAMES = FALSE)
parallel::stopCluster(clusters)
rm(clusters, cores)

correlations <- dplyr::bind_rows(X)


# storage
storage <- file.path(getwd(), 'warehouse', 'missing', 'correlation', 'cramer.csv')
if (file.exists(storage)) {
  base::unlink(x = storage, recursive = TRUE)
}
dir.create(path = base::dirname(storage), recursive = TRUE)


# write
utils::write.table(x = correlations,
                   file = storage,
                   append = FALSE,
                   sep = ',',
                   row.names = FALSE,
                   col.names = TRUE,
                   fileEncoding = 'UTF-8')