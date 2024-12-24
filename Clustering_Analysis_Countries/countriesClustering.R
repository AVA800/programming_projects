# Alejandro Venegas Ataca

# Reading dataset "countriesData.xlsx"
#install.packages('backports')
library("openxlsx")
library(cluster)
library ("FactoMineR")
library ("factoextra")
library(ggplot2)
library('backports')

xlsxFilename='countriesData.xlsx'
countriesData=read.xlsx(xlsxFilename,sheet=1,startRow=1,colNames=TRUE,
                        rowNames=FALSE,
                        skipEmptyRows = TRUE,
                        skipEmptyCols=TRUE)

# Checking dataset
head(countriesData)

# Extracting the categorical variable "country"
CNumeric=countriesData[,2:8]

# Plotting PCA plot to analyze the number of clusters
PCA.Res=PCA(CNumeric,graph=F,ncp=2,scale.unit=TRUE)
fviz_pca_ind(PCA.Res,repel= TRUE)

# INTERPRETATION: The PCA plot shows us 5 possible clusters (k). Based on the Rule of Thumb, I used ncp=2 because dim1+sum2=80.7%

# Stardardizing numeric data
CNumeric_std=as.data.frame(scale(CNumeric))

# Creating distance matrix
d=dist(x=CNumeric_std,method='euclidean')

# Performing agglomerative clustering with hclust
results=hclust(d,method='ward.D')

# Ploting dendogram
plot(results)

# INTERPRETATION:The dendogram support the idea of number of clusters (k)=5 because we see 5 groups.

# Creating clusters and assigning data into clusters
c=cutree(results,k=5)

# Ploting PCA plot
PCA.Res=PCA(CNumeric,graph=F,ncp=2,scale.unit=TRUE)
fviz_pca_ind(PCA.Res,habillage=factor(c),repel= TRUE)

# INTERPRETATION: The new PCA plot confirm that number of clusters(k) is 5. Based on the Rule of Thumb, I used ncp=2 because dim1+sum2=80.7%

#Performing KMEANS
#Define the optimal number of clusters
set.seed(13)

# Determining and visualizing the optimal number of clusters through "within cluster sums of squares"(wss), and "average silhouette"
fviz_nbclust(CNumeric_std,kmeans,method = 'wss',k.max =8) 

fviz_nbclust(CNumeric_std,kmeans,method ='silhouette',k.max =8)
             
# INTERPRETATION: Both graphs show us that the optimal number of clusters is 4.

# Run kmeans with 4 clusters
results_k1=kmeans(x=CNumeric_std,centers=4,nstart=15)

# Plotting cluster plot
fviz_cluster(results_k1,data=CNumeric_std,labelsize=15,repel=TRUE)

# INTERPRETATION: The cluster plot of K-means show us 4 clusters