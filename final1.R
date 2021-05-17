# load packages
library(plm)
library(lmtest)
library(texreg)
library(aod)
library(stargazer)
# clear the environment
rm(list = ls())

# read data
M14 <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallMax13r.csv")
A14 <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallAny13r.csv")
normal14 <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regall13r.csv")

Max7 <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallMax6r.csv")
Any7 <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallAny6r.csv")

Max1 <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallMax0r.csv")
Any1 <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallAny0r.csv")

Max21 <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallMax20r.csv")
Any21 <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallAny20r.csv")

Max28 <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallMax27r.csv")
Any28 <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/regallAny27r.csv")

#countMaxNo <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/countMaxNo.csv")
countMaxYes <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/countMaxYes.csv")
#countAnyNo <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/countAnyNo.csv")
countAnyYes <- read.csv("C:/Users/wuxin/OneDrive/Desktop/QTEM/final/countAnyYes.csv")


Any14 <- merge(A14, countAnyYes,by = "Code")
Max14 <- merge(M14, countMaxYes,by = "Code")
Mix14 <- merge(M14,countAnyYes, by = "Code")


# fixed effects model1: test for all policies
# one way
# individual effect tests effects that vary across country but constant over time (so-called time invariant effects, such as GDP per capita, unemployment rate etc.)
individual_effects1 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+factor(public_information_campaigns)+factor(restrictions_internal_movements)+factor(close_public_transport), 
                     data = normal14, 
                     index = c("Code", "Day.t..14"), 
                     model = "within", 
                     effect = "individual")

summary(individual_effects1)


plmtest(individual_effects1, effect="individual") # test individual effect

# time effects model test any effects that vary across time but are constant across countries.
time_effects1 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+factor(public_information_campaigns), 
                    data = normal14, 
                    index = c("Code", "Day.t..14"), 
                    model = "within", 
                    effect = "time")

summary(time_effects1)

plmtest(time_effects1, effect="time") #there are time-fixed effects present in our model

# two way
twoway_effects1 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+factor(public_information_campaigns)+factor(restrictions_internal_movements), 
                      data = normal14, 
                      index = c("Code", "Day.t..14"), 
                      model = "within", 
                      effect = "twoways")

summary(twoway_effects1)

screenreg(list(individual_effects1, time_effects1, twoway_effects1), 
          custom.model.names = c("State Fixed Effects", 
                                 "Time Fixed Effects", 
                                 "Twoway Fixed Effects"))
# test for serial correlation
pcdtest(twoway_effects1)
# test for cross sectional dependence
pbgtest(twoway_effects1)


twoway_effects_hac1 <- coeftest(twoway_effects1, 
                               vcov = vcovHC(twoway_effects1, 
                                             method = "arellano", 
                                             type = "HC3"))

screenreg(list(twoway_effects1, twoway_effects_hac1),
          custom.model.names = c("Twoway Fixed Effects", 
                                 "Twoway Fixed Effects (HAC)"))

twoway_effects_pcse1 <- coeftest(twoway_effects1, 
                                vcov = vcovBK(twoway_effects1, 
                                              type="HC3", 
                                              cluster = "group")) 

twoway_effects_pcse1

screenreg(list(individual_effects1, time_effects1, twoway_effects1,twoway_effects_hac1,twoway_effects_pcse1), 
          custom.model.names = c("State Fixed Effects", 
                                 "Time Fixed Effects", 
                                 "Twoway Fixed Effects",
                                 "Twoway Fixed Effects (HAC)",
                                 "Twoway Fixed Effects (PCSE)"))
##################################################################################################################################################################################################

# fixed effects model2: selection of variables
# one way
# individual effect: delete public information campaign
individual_effects2 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(restrictions_internal_movements)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(close_public_transport)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy), 
                           data = normal14, 
                           index = c("Code", "Day.t..14"), 
                           model = "within", 
                           effect = "individual")

summary(individual_effects2)


plmtest(individual_effects2, effect="individual") # test individual effect

# individual effect: delete public information campaign, close public transport
individual_effects3 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(restrictions_internal_movements)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy), 
                           data = normal14, 
                           index = c("Code", "Day.t..14"), 
                           model = "within", 
                           effect = "individual")

summary(individual_effects3)


plmtest(individual_effects3, effect="individual") # test individual effect

# individual effect: delete public information campaign, close public transport,restriction internal movements
individual_effects4 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy), 
                           data = normal14, 
                           index = c("Code", "Day.t..14"), 
                           model = "within", 
                           effect = "individual")

summary(individual_effects4)


plmtest(individual_effects4, effect="individual") # test individual effect

# individual effect: delete public information campaign,restriction internal movements
individual_effects5 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(close_public_transport)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy), 
                           data = normal14, 
                           index = c("Code", "Day.t..14"), 
                           model = "within", 
                           effect = "individual")

summary(individual_effects5)


plmtest(individual_effects5, effect="individual") # test individual effect

screenreg(list(individual_effects2, individual_effects3, individual_effects4,individual_effects5), 
          custom.model.names = c("no info campaign", 
                                 "no info & close transport", 
                                 "no info, close, restriction internal",
                                 "no info & restriction internal"))
# choose to delete public information campaign, close public transport and restriction internal movements
#####################################################################################################################################################################################################
# based on selected variables, compare all models (time effects, with both state and time effect, etc)
time_effects2 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy), 
                     data = normal14, 
                     index = c("Code", "Day.t..14"), 
                     model = "within", 
                     effect = "time")

summary(time_effects2)

plmtest(time_effects2, effect="time") #there are time-fixed effects present in our model

# two way
twoway_effects2 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy), 
                       data = normal14, 
                       index = c("Code", "Day.t..14"), 
                       model = "within", 
                       effect = "twoways")

summary(twoway_effects2)

screenreg(list(individual_effects4, time_effects2, twoway_effects2), 
          custom.model.names = c("State Fixed Effects", 
                                 "Time Fixed Effects", 
                                 "Twoway Fixed Effects"))
# test for serial correlation
pcdtest(twoway_effects2)
# test for cross sectional dependence
pbgtest(twoway_effects2)


twoway_effects_hac2 <- coeftest(twoway_effects2, 
                                vcov = vcovHC(twoway_effects2, 
                                              method = "arellano", 
                                              type = "HC3"))

screenreg(list(twoway_effects2, twoway_effects_hac2),
          custom.model.names = c("Twoway Fixed Effects", 
                                 "Twoway Fixed Effects (HAC)"))

twoway_effects_pcse2 <- coeftest(twoway_effects2, 
                                 vcov = vcovBK(twoway_effects2, 
                                               type="HC3", 
                                               cluster = "group")) 

twoway_effects_pcse2

screenreg(list(individual_effects4, time_effects2, twoway_effects2,twoway_effects_hac2,twoway_effects_pcse2), 
          custom.model.names = c("State Fixed Effects", 
                                 "Time Fixed Effects", 
                                 "Twoway Fixed Effects",
                                 "Twoway Fixed Effects (HAC)",
                                 "Twoway Fixed Effects (PCSE)"))
##############################################################################################################################################################################################
# include group dummy
# individual effect
individual_effects6 <- plm(reproduction_rate ~ (factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy))*factor(cluster), 
                           data = normal14, 
                           index = c("Code", "Day.t..14"), 
                           model = "within", 
                           effect = "individual")

summary(individual_effects6)


plmtest(individual_effects6, effect="individual") # test individual effect

# include additionally time effect
# individual effect
individual_effects7 <- plm(reproduction_rate ~ (factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy))*factor(cluster)+timeIndex, 
                           data = normal14, 
                           index = c("Code", "Day.t..14"), 
                           model = "within", 
                           effect = "individual")

summary(individual_effects7)
plmtest(individual_effects7, effect="individual") # test individual effect

# present baseline results (Table 4 in paper)
stargazer(individual_effects1,individual_effects4, type="html", 
          column.labels=c("All NPIs","Selected NPIs"), title="Table 4: Selection of NPIs",out="C:/Users/wuxin/OneDrive/Desktop/QTEM/final/Table 4.doc")

##############################################################################################################################################################################################
# logistic regression to predict the group
glm.fit <- glm(factor(cluster) ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy), data = normal14, family = "binomial")
summary(glm.fit)

## CIs using profiled log-likelihood
confint(glm.fit)

## CIs using standard errors
confint.default(glm.fit)

wald.test(b = coef(glm.fit), Sigma = vcov(glm.fit), Terms = 2:5) #the overall effect of rank is statistically significant

#We can also test additional hypotheses about the differences in the coefficients for the different levels of rank
l <- cbind(0, 1,-1,0,0)
wald.test(b = coef(glm.fit), Sigma = vcov(glm.fit), L = l) #the difference between the coefficient for analysis=2 and the coefficient for analysis=3 is statistically significant.

## odds ratios only
exp(coef(glm.fit))
## odds ratios and 95% CI
exp(cbind(OR = coef(glm.fit), confint(glm.fit)))

glm.probs <- predict(glm.fit,type = "response")
glm.probs[1:8]
glm.pred <- ifelse(glm.probs > 0.5, "EU", "AP")
attach(normal14)
table(glm.pred,factor(cluster))
mean(glm.pred == factor(cluster))
detach(normal14)

######################################################################################################################################################################
# random effects
random1 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy), 
               data = Any14, 
               index = c("Code", "Day.t..14"), 
              model = "random")


random2 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy), 
               data = Max14, 
               index = c("Code", "Day.t..14"), 
               model = "random")



screenreg(list(random1, random2), 
          custom.model.names = c("Any", 
                                 "Max"))

########################################################################################################################################################################
# fixed effects for any and max, compare between fe and random 

fe1 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+timeIndex, 
               data = Any14, 
               index = c("Code", "Day.t..14"), 
               model = "within")

fe2 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+timeIndex, 
               data = Max14, 
               index = c("Code", "Day.t..14"), 
               model = "within")
fe3 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+timeIndex, 
           data = Any7, 
           index = c("Code", "Day.t..7"), 
           model = "within")
fe4 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+timeIndex, 
           data = Max7, 
           index = c("Code", "Day.t..7"), 
           model = "within")
fe5 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+timeIndex, 
           data = Any1, 
           index = c("Code", "Day.t..1"), 
           model = "within")
fe6 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+timeIndex, 
           data = Max1, 
           index = c("Code", "Day.t..1"), 
           model = "within")

fe7 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+timeIndex, 
           data = Any21, 
           index = c("Code", "Day.t..21"), 
           model = "within")

fe8 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+timeIndex, 
           data = Max21, 
           index = c("Code", "Day.t..21"), 
           model = "within")

fe9 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+timeIndex, 
           data = Any28, 
           index = c("Code", "Day.t..28"), 
           model = "within")

fe10 <- plm(reproduction_rate ~ factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy)+timeIndex, 
           data = Max28, 
           index = c("Code", "Day.t..28"), 
           model = "within")

# table 6 & 7 in paper
stargazer(fe5,fe3, fe1,fe7,fe9, type="html", 
          column.labels=c("Lag 1","Lag 7", "Lag 14","Lag 21","Lag 28"), title="Table 6: Comparison between Different Time Lags for Any-Scenario",out="C:/Users/wuxin/OneDrive/Desktop/QTEM/final/Table 6.doc")

stargazer(fe6,fe4,fe2,fe8,fe10, type="html", 
          column.labels=c("Lag 1","Lag 7", "Lag 14","Lag 21","Lag 28"), title="Table 7: Comparison between Different Time Lags for Max-Scenario",out="C:/Users/wuxin/OneDrive/Desktop/QTEM/final/Table 7.doc")





phtest(random1, fe1)
phtest(random2, fe2)

# thus decide for fe

######################################################################################################################################################################
# try to explain the difference 
individual_effects8 <- plm(reproduction_rate ~ factor(international_travel_controls)*international_travel_controlsL+factor(cancel_public_events)*cancel_public_eventsL+factor(restriction_gatherings)*restriction_gatheringsL+factor(workplace_closures)*workplace_closuresL+factor(school_closures)*school_closuresL+factor(stay_home_requirements)*stay_home_requirementsL+factor(facial_coverings)*facial_coveringsL+factor(contact_tracing)*contact_tracingL+factor(testing_policy)*testing_policyL+timeIndex, 
                           data = Any14, 
                           index = c("Code", "Day.t..14"), 
                           model = "within", 
                           effect = "individual")

summary(individual_effects8)


plmtest(individual_effects8, effect="individual") # test individual effect

individual_effects9 <- plm(reproduction_rate ~ factor(international_travel_controls)*international_travel_controlsL+factor(cancel_public_events)*cancel_public_eventsL+factor(restriction_gatherings)*restriction_gatheringsL+factor(workplace_closures)*workplace_closuresL+factor(school_closures)*school_closuresL+factor(stay_home_requirements)*stay_home_requirementsL+factor(facial_coverings)*facial_coveringsL+factor(contact_tracing)*contact_tracingL+factor(testing_policy)*testing_policyL+timeIndex, 
                           data = Max14, 
                           index = c("Code", "Day.t..14"), 
                           model = "within", 
                           effect = "individual")

summary(individual_effects9)

plmtest(individual_effects9, effect="individual") # test individual effect

summary(individual_effects7)
screenreg(list(individual_effects8,individual_effects9), 
          custom.model.names = c("Any",
                                 "Max"))
# failed

Max14_EU <- Max14[Max14$cluster == 1, ]
Max14_AP <- Max14[Max14$cluster == 0, ]


Any14_EU <- Any14[Any14$cluster == 1, ]
Any14_AP <- Any14[Any14$cluster == 0, ]

individual_effects10 <- plm(reproduction_rate ~ (factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy))*factor(cluster)+timeIndex, 
                           data = Any14, 
                           index = c("Code", "Day.t..14"), 
                           model = "within")


individual_effects11 <- plm(reproduction_rate ~ (factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy))*factor(cluster)+timeIndex, 
                              data = Max14, 
                              index = c("Code", "Day.t..14"), 
                              model = "within", 
                              effect = "individual")

# table 5 in paper
stargazer(random1,random2, fe1,fe2,individual_effects10,individual_effects11, type="html", 
          column.labels=c("Random, Any","Random, Max", "Fixed Effects, Any","Fixed Effects, Max","Any Full","Max Full"), title="Table 6: Baseline Reults ",out="C:/Users/wuxin/OneDrive/Desktop/QTEM/final/Table 5.doc")




screenreg(list(individual_effects10EU,individual_effects10AP), 
          custom.model.names = c("EU",
                                 "AP"))

# try once again
individual_effects11 <- plm(reproduction_rate ~ (factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy))*(international_travel_controlsL+cancel_public_eventsL+restriction_gatheringsL+workplace_closuresL+school_closuresL+stay_home_requirementsL+facial_coveringsL+contact_tracingL+testing_policyL)+timeIndex, 
                              data = Max14, 
                              index = c("Code", "Day.t..14"), 
                              model = "within", 
                              effect = "individual")


individual_effects11EU <- plm(reproduction_rate ~ (factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy))*(international_travel_controlsL+cancel_public_eventsL+restriction_gatheringsL+workplace_closuresL+school_closuresL+stay_home_requirementsL+facial_coveringsL+contact_tracingL+testing_policyL)+timeIndex, 
                              data = Max14_EU, 
                              index = c("Code", "Day.t..14"), 
                              model = "within", 
                              effect = "individual")


individual_effects11AP <- plm(reproduction_rate ~ (factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy))*(international_travel_controlsL+cancel_public_eventsL+restriction_gatheringsL+workplace_closuresL+school_closuresL+stay_home_requirementsL+facial_coveringsL+contact_tracingL+testing_policyL)+timeIndex, 
                              data = Max14_AP, 
                              index = c("Code", "Day.t..14"), 
                              model = "within", 
                              effect = "individual")

screenreg(list(individual_effects11,individual_effects11EU,individual_effects11AP), 
          custom.model.names = c("ALL",
                                 "EU",
                                 "AP"))

# again another try: test focus on the strength of AP
Mix14_EU <- Max14[Mix14$cluster == 1, ]
Mix14_AP <- Max14[Mix14$cluster == 0, ]
individual_effects12 <- plm(reproduction_rate ~ (factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy))*(factor(international_travel_controls)+factor(contact_tracing)+factor(testing_policy))+timeIndex, 
                            data = Any14, 
                            index = c("Code", "Day.t..14"), 
                            model = "within", 
                            effect = "individual")


individual_effects12EU <- plm(reproduction_rate ~ (factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy))*(factor(international_travel_controls)+factor(contact_tracing)+factor(testing_policy))+timeIndex, 
                            data = Any14_EU, 
                            index = c("Code", "Day.t..14"), 
                            model = "within", 
                            effect = "individual")

individual_effects12AP <- plm(reproduction_rate ~ (factor(international_travel_controls)+factor(cancel_public_events)+factor(restriction_gatherings)+factor(workplace_closures)+factor(school_closures)+factor(stay_home_requirements)+factor(facial_coverings)+factor(contact_tracing)+factor(testing_policy))*(factor(international_travel_controls)+factor(contact_tracing)+factor(testing_policy))+timeIndex, 
                            data = Any14_AP, 
                            index = c("Code", "Day.t..14"), 
                            model = "within", 
                            effect = "individual")


screenreg(list(individual_effects12,individual_effects12EU,individual_effects12AP), 
          custom.model.names = c("ALL",
                                 "EU",
                                 "AP"))
# *(international_travel_controlsL+cancel_public_eventsL+restriction_gatheringsL+workplace_closuresL+school_closuresL+stay_home_requirementsL+facial_coveringsL+contact_tracingL+testing_policyL)
########################################################################################################################################################







