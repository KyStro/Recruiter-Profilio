# Name: Kyle Strokes
# Date: 4/24/19
# ISTA 116 Section C || Jacob Heller
# Lab Assignment 14
# Collaborator: Elaine Mancillas

download.file("http://www.openintro.org/stat/data/mlb11.RData", destfile = "mlb11.RData")
load("mlb11.RData")

#1
runs_from_at_bat <- plot(runs~at_bats, data = mlb11)
# Yes there seems to be a positive correlation between runs and at-bats

#2
cor(mlb11$at_bats, mlb11$runs)
# R value of 0.61 tells us that there is a moderate correlation

#3
plot_ss(x = mlb11$at_bats, y = mlb11$runs)
#201859
#136445
#125033.3
#141310.3
# I was able to get down to 125033.3 sum of residuals

#4
lm_runs_bats <- lm(runs~at_bats, data = mlb11)
# runs = 0.6305(at_bats) - 2789.2429
# This gives a different slope and y intercept then my estimates because it is the actual line of best fit

#5
summary(lm_runs_bats)
# (Multiple R-squared) 0.3729 is the R^2 value which explains the variability of runs explained by at bats

#6
plot(lm_runs_bats)
# The points are close to 0 but the scale is on 50 which is alot of error
# But the points do not lie on the normal distribution
# Variance is same throughout, but error is alot
# The conditions are not really met

#7
plot(runs~homeruns, data = mlb11)
lm_hr_bats <- lm(runs~homeruns, data = mlb11)
summary(lm_hr_bats)
# runs = 1.835(homeruns) + 415.239

#8
cor(mlb11$homeruns, mlb11$runs)
# homeruns are a better indicator of runs because the R value is 0.791 and the at bats R value is only 0.61

#9
cor(mlb11$hits, mlb11$runs)
summary(lm(runs~hits, data = mlb11))

cor(mlb11$bat_avg, mlb11$runs)
summary(lm(runs~bat_avg, data = mlb11))

cor(mlb11$strikeouts, mlb11$runs)
summary(lm(runs~strikeouts, data = mlb11))

cor(mlb11$stolen_bases, mlb11$runs)
summary(lm(runs~stolen_bases, data = mlb11))

cor(mlb11$wins, mlb11$runs)
summary(lm(runs~wins, data = mlb11))
# Batting avgerage gives the best predictor for runs with a R value of 0.81

#10
model <- lm(runs ~ at_bats + hits + homeruns + bat_avg + strikeouts + stolen_bases + wins, data = mlb11)
summary(model)
# It explains more than the single variables, this is probably because alot of variables go into this statistic
