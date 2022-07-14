# Title     : CorrelationGraph.R
# Objective : Correlation graph
# Created by: greyhypotheses
# Created on: 12/07/2022


source(file = 'R/missing/DegreeOfCorrelation.R')


#' Correlation graph
#'
#' @description draws a correlation raster using Cramer's V degree of correlation values
#'
#' @param variables: a set of categorical variables names
#' @param data: the data set
#'
CorrelationGraph <- function (variables, data) {

  # the correlation of each variable with all others
  design <- mapply(FUN = DegreeOfCorrelation, reference = variables,
                   MoreArgs = list(variables = variables, frame = data))
  measures <- dplyr::bind_rows(design)

  # matrix graph, colors = c('#E46726', 'white', 'black'),
  ggcorrplot::ggcorrplot(corr = measures,
                         type = 'upper',
                         ggtheme = ggplot2::theme_minimal(),
                         outline.color = 'white',
                         lab = TRUE,
                         lab_size = 3,
                         lab_col = 'grey',
                         digits = 2) +
    scale_fill_gradient2(breaks = c(0, 1), limit = c(0, 1)) +
    labs(fill = "Cramer's V\n")

}