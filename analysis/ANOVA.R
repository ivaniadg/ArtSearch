install.packages("HH", dependencies = TRUE)

lceh <- read.csv("pre_summarized_lceh.csv", sep = ",")
likert(Question~., lceh, as.percent = TRUE, rightAxis = FALSE, auto.key=list(space="right", columns=1,
                                                                                reverse=TRUE, padding.text=2), main="Answers from the questionnaire (LC+EH)")


lces <- read.csv("pre_summarized_lces.csv", sep = ",")
likert(Question~., lces, as.percent = TRUE, rightAxis = FALSE, auto.key=list(space="right", columns=1,
                                                                                reverse=TRUE, padding.text=2), main="Answers from the questionnaire (LC+ES)")


hceh <- read.csv("pre_summarized_hceh.csv", sep = ",")
likert(Question~., hceh, as.percent = TRUE, rightAxis = FALSE, auto.key=list(space="right", columns=1,
                                                                             reverse=TRUE, padding.text=2), main="Answers from the questionnaire (HC+EH)")

hces <- read.csv("pre_summarized_hces.csv", sep = ",")
likert(Question~., hces, as.percent = TRUE, rightAxis = FALSE, auto.key=list(space="right", columns=1,
                                                                             reverse=TRUE, padding.text=2), main="Answers from the questionnaire (HC+ES)")

