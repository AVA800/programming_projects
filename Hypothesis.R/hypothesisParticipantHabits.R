# Alejandro Venegas Ataca
# Hypothesis of habits in a group of participants. The dataset was provided by Rowan University.

library("openxlsx")
xlsxFilename='retinol.xlsx'
retinolData=read.xlsx(xlsxFilename,sheet=1,startRow=1,colNames=TRUE,
                       rowNames=FALSE,
                       skipEmptyRows = TRUE,
                       skipEmptyCols=TRUE)

# Checking if dataset was read correctly
head(retinolData)
names(retinolData)

# Is there a difference in the Plasma beta-carotene levels between the two genders?
# I will use Two Sample T-test to analyze if there a difference in the Plasma beta-carotene levels between the two genders because we have 1 sample for males, and 1 sample for females. But, previous to do that, I will check statistical assumptions.

# Displaying QQ-plots and histograms to check statistical assumptions

# Checking QQ-plot of "Male-BetaPlasma"
x=retinolData[,13]
g=retinolData[,2]
x1=subset(x,g=="Male")
MyTitle= "Male-BetaPlasma QQPlot"
qqnorm(x1,main=MyTitle)
qqline(x1,col="red")

# Checking  Histogram "Male-BetaPlasma"
range(x1,na.rm=TRUE)
ClassEndpoints1=seq(21,751,50)
MyTitle = " Male-BetaPlasma Histogram"
MyXlab = "BetaPlasma"
MyYlab = " Frequency"
hist(x1,freq=FALSE,main=MyTitle)
xnorm = seq(21,751,50)
ynorm = dnorm(xnorm,mean=mean(x1,na.rm=TRUE),
              sd=sd(x1,na.rm=TRUE))
lines(xnorm,ynorm,col="red")

# Checking QQ-plot of "Female-BetaPlasma"
x=retinolData[,13]
g=retinolData[,2]
x1=subset(x,g=="Female")
MyTitle= "Female-BetaPlasma QQPlot"
qqnorm(x1,main=MyTitle)
qqline(x1,col="red")

# Checking  Histogram "Female-BetaPlasma"
range(x1,na.rm=TRUE)
ClassEndpoints1=seq(0,1415,200)
MyTitle = "Female-BetaPlasma Histogram"
MyXlab = "BetaPlasma"
MyYlab = "Frequency"
hist(x1,freq=FALSE,main=MyTitle)
xnorm = seq(0,1415,200)
ynorm = dnorm(xnorm,mean=mean(x1,na.rm=TRUE),
              sd=sd(x1,na.rm=TRUE))
lines(xnorm,ynorm,col="red")

# INTERPRETATION: Graphs do not suggest that assumptions were violated. The variable "BetaPlasma" is numeric and normality in the 2 samples is acceptable because "Male-BetaPlasma QQ-plot" is some linear, and "Female-BetaPlasma QQ-plot" is linear with some outliers. If assumptions would be violated, I would use "Wilcoxon"

# Displaying 2 sample T-test to analyze if there a difference in the Plasma beta-carotene levels between the two genders
aggregate(x~g,FUN="sd",na.rm=TRUE)

# As RoT=188.85/133.6=1.41<2  I will Use var.equal = TRUE
t.test (x~g,conf.level =.99,
        alternative="two.sided",
        var.equal=TRUE)

# CONCLUSION: The data does not indicate a difference in the Plasma beta-carotene levels between the two genders because the p-value of the Two Sample T-test is large(p-value=0.117>0.05(alpha))

# Is there a relationship (difference) between the calory intake of a person and their smoking habits?
# I will use ANOVA sample means because it will let me know if we have any difference in at least 2 groups (we have 3 smoking status). But, previous to do that, I will check statistical assumptions.

# Plotting QQ-plot of residuals
x=retinolData[,6]
g=retinolData[,3]
AModRes=aov(x~g)
summary(AModRes)
par(mfrow = c(1,1))
plot(AModRes,2)

# Assumptions were not violated. We have numeric data and QQ-plot shows us a straight line with some outliers. In consequence, normality is acceptable.

# Testing Hypothesis "Is there a relationship (difference) between the calory intake of a person and their smoking habits?".
AModRes=aov(x~g)
summary(AModRes)

# INTERPRETATION: We can weakly assume that there are not differences between the calory intake of a person and their smoking habits because the p-value of the ANOVA sample means is some large (0.0821>0.05(alpha)).
