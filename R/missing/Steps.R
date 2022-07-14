# Title     : Steps.R
# Objective : Null correlation calculation steps
# Created by: greyhypotheses
# Created on: 14/07/2022



#' Steps
#'
#' @description Degree of association calculation steps.
#'
#' @param file: The name, file path, of a file encoding missing data
#'              state per field/column.
#'
Steps <- function (file) {

  source(file = 'R/missing/DegreeOfCorrelation.R')


  # the ISO2 code
  name <- base::basename(file)
  ISO2 <- base::strsplit(name, ".csv")[[1]]


  # reading-in a data file
  frame <- read.csv(file = file, encoding = 'UTF-8')


  # ascertaining factors
  case <-function(x, frame){
    T <- data.frame(dplyr::if_else(frame[x] == 'True', TRUE, FALSE))
    names(T) <- x
    T[x] <- factor(T[[x]], levels = c(FALSE, TRUE))
    return(list(T))
  }
  states <- mapply(x = colnames(frame), FUN = case, MoreArgs = list(frame = frame))
  states <- dplyr::bind_cols(states)


  # determining the degree of association between each pairing of factor variables
  variables <- c('year', 'longitude', 'latitude', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence', 'coordinates')
  design <- mapply(FUN = DegreeOfCorrelation, reference = variables,
                   MoreArgs = list(variables = variables, frame = states))
  measures <- dplyr::bind_rows(design)


  # appending country ISO 2 code
  measures$iso2 <- ISO2


  # structuring
  measures <- dplyr::mutate(measures, variable = rownames(measures), .before = 1)
  rownames(measures) <- NULL


  return(list(measures))

}