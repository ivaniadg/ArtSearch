install.packages("semTools", dependencies = TRUE)
library(lavaan)
library(semPlot)
library(semTools)
library(effectsize)
answers <- read.csv("questionnaire_parsed.csv", sep = ",")

questions <- c("Q1" ,"Q2", "Q3", "Q4", "Q5" ,"Q7" ,"Q9", "Q10", "Q11","Q12", "Q13","Q14" ,"Q15")

questions <- c("Q3", "Q4", "Q5" ,"Q7" ,"Q9", "Q10", "Q11","Q12", "Q13")

efa <- efa(data = answers[,questions], nfactors = 1:7)
summary(efa)


model1 <- '
  Accuracy =~ Q1
  Control =~ Q3 + Q5
  Explanations =~ Q2 + Q7 + Q9
  Usability =~ Q10 + Q4
  Trust =~ Q12 + Q13
  UseIntentions =~ Q15 + Q14
  '

fit1 <- cfa(model1,data = answers, ordered=questions)

summary(fit1, fit.measures = TRUE)


modindices(fit1, sort = TRUE, maximum.number = 5)
interpret(fit1)
reliability(fit)


semPaths(fit1,
         what = "std", # this argument controls what the color of edges represent. In this case, standardized parameters
         whatLabels = "est", # This argument controls what the edge labels represent. In this case, parameter estimates
         style = "lisrel", # This will plot residuals as arrows, closer to what we use in class
         residScale = 8, # This makes the residuals larger
         theme = "colorblind", # qgraph colorblind friendly theme
         nCharNodes = 0, # Setting this to 0 disables abbreviation of nodes
         reorder = FALSE, # This disables the default reordering
         legend.cex = 0.5, # Makes the legend smaller
         rotation = 2, # Rotates the plot
         layout = "tree3", # tree layout options are "tree", "tree2", and "tree3"
         cardinal = "lat cov", # This makes the latent covariances connet at a cardinal center point
         curvePivot = TRUE, # Changes curve into rounded straight lines
         sizeMan = 4, # Size of manifest variables
         sizeLat = 10, # Size of latent variables
         mar = c(2,5,2,5.5), # Figure margins
)






model2 <- '
Explanations =~ Q2 + Q7 + Q9
Control =~ Q3 + Q5
UseIntentions =~ Q14 + Q15
'

fit2 <- cfa(model=model2,data=answers, check.gradient = FALSE)


summary(fit2, fit.measures = TRUE)


interpret(fit2)

reliability()








