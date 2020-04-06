# Name: Kyle Strokes
# Date: 4/3/19
# ISTA 116 Section C || Jacob Heller
# Lab Assignment 11
# Collaborator: Elaine Mancillas

download.file("http://www.openintro.org/stat/data/nc.RData", destfile = "nc.RData")
load("nc.RData")
nc <- na.omit(nc)

#1
# H0 = pregnancy lasts 40 weeks; p = 40
# Ha = pregnancy does not lasts 40 weeks; p != 40

#2
histogram <- hist(nc$weeks)
# There is a left skew of the data but it resembles some normalitity. To preform a hypothesis test it must be normally distributed, but because of the central limit theorem we can test on this data.

#3
nc_mean <- mean(nc$weeks)
se <- sd(nc$weeks)/sqrt(800)

#4
critical <- qnorm(1 - (1 - 0.99) / 2) * se

#5
lower_bound <- nc_mean - critical
upper_bound <- nc_mean + critical
# No the null hypothesis of 40 does not lie between 38.2 and 38.7

#6
z <- (nc_mean - 40) / se

#7
p_val <- pnorm(z) * 2
# It is a two sided test because the alternative hypothesis says != and does not specify > or < so we take both sides. I can conclude that we reject the null hypothesis because p value is very small.

#8
cutoff <- qnorm(0.05, 39+(6/7), se)

#9
prob_of_1day <- pnorm(cutoff, (39 + 6/7) , se)
# I am not satisfied with this power because of 0.05% of the observed data falls beyond the rejection value

#10
prob_of_1week <- pnorm(cutoff, 39 , se)
# I am satisfied with this power because of 99.9% of the observed data falls beyond the rejection value