# Title     : DegreeOfCorrelation.R
# Objective : Correlation analysis w.r.t. categorical variables
# Created by: greyhypotheses
# Created on: 12/07/2022



#' Returns a table of test statistic, p, & Cramér's V values
#'
#' @param variables: The list of categorical variables that will be compared with the reference variable
#' @param reference: The categorial reference variable
#' @param frame: The table of data
DegreeOfCorrelation <- function(variables, reference, frame) {

  estimates <- data.frame()
  for (variable in variables) {

    # contingency table, by default 'table' excludes NA counts (for NA counts ... useNA = 'always')
    frequencies <- table(frame[[variable]], frame[[reference]])

    # What is the degree of association between the elements of the fields?
    cramercinq <- rcompanion::cramerV(frequencies, y = NULL, ci = FALSE, conf = 0.95, type = 'bca',
                                      R = 1000, histogram = FALSE, digits = 4, bias.correct = TRUE)

    # Add the estimates to the table of estimates
    estimates[1, variable] <- as.numeric(cramercinq)
  }

  skeleton <- t(data.frame(unlist(estimates)))
  rownames(skeleton) <- reference
  T <- data.frame(skeleton)

  return(list(item = T))

}