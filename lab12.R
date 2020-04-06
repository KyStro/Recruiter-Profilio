# Name: Kyle Strokes
# Date: 4/10/19
# ISTA 116 Section C || Jacob Heller
# Lab Assignment 12
# Collaborator: Elaine Mancillas

download.file("http://www.openintro.org/stat/data/nc.RData", destfile = "nc.RData")
load("nc.RData")

#1
weight_by_habit <- by(nc$weight, nc$habit, mean)

#2
num_each <- by(nc$weight, nc$habit, length)
hist_each <- by(nc$weight, nc$habit, hist)
# Both samples are random which implies independence, also nonsmoker a little skew but the smaple size is large enough, smoker also has a little skew which is fine

#3
#H0: There is no difference in birth weights between nonsmoking mothers and smoking mothers. Smoking Mom BW = Non smoking mom BW 
#HA: There is a difference in birth weights between nonsmoking mothers and smoking mothers. Smoking Mom BW != non smoking mom BW

#4
t.test(nc$weight~nc$habit)

#5
#I would be surprised if the mean difference was 0.8 because it is outside of the 95% confidence interval

#6
t.test(nc$weeks)
# I wouldn't be surprised because 38.5 does fall in the 95% CI

#7
t.test(nc$weeks, conf.level = 0.9)
# I would be surprised because 38.5 does not fall in the 90% CI. It is different because the CI is smaller thats why the confidence is lower by 5%

#8
each_num2 <- by(nc$gained, nc$mature, length)
each_hist2 <- by(nc$gained, nc$mature, hist)
t.test(nc$gained~nc$mature)
# the p-value is 0.1704 so we cannot deny the null hypothesis, so there is no difference in weight gaine by mature and young mothers

#9
mage_young_cut <- by(nc$mage, nc$mature, max)
#34
mage_mature_cut <- by(nc$mage, nc$mature, min)
#35
# The cutoff for the mother age for young and mature is 34

#10
#H0: the gender does not affect weight
#HA: the gender does affect weight
each_num3 <- by(nc$weight, nc$gender, length)
each_hist3 <- by(nc$weight, nc$gender, hist)
t.test(nc$weight~nc$gender)
# the p-value is extremely low so we can reject the null hyothesis because the probability of seeing these results is so low. Gender does effect weight