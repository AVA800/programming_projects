# Alejandro Venegas Ataca

# Reading dataset "statesData.xlsx"
#install.packages('backports')
library("openxlsx")
library(cluster)
library ("FactoMineR")
library ("factoextra")
library(ggplot2)
library('backports')

xlsxFilename='statesData.xlsx'
statesData=read.xlsx(xlsxFilename,sheet=1,startRow=1,colNames=TRUE,
                    rowNames=FALSE,
                    skipEmptyRows = TRUE,
                    skipEmptyCols=TRUE)

# Checking dataset
head(statesData)

# Extracting categorical variables
CNumeric=statesData[,2:8]
head(CNumeric)

# Plotting PCA plot to analyze the number of clusters
PCA.Res=PCA(CNumeric,graph=F,ncp=2,scale.unit=TRUE)
fviz_pca_ind(PCA.Res,repel= TRUE)

# INTERPRETATION: The PCA plot shows us around 6 clusters (k)

# Stardardizing numeric data
CNumeric_std=as.data.frame(scale(CNumeric))

# Creating distance matrix
d=dist(x=CNumeric_std,method='euclidean')

# Performing Hierarchical method with hclust
results=hclust(d,method='complete')

# Plotting dendrogram
plot(results)

# INTERPRETATION:The dendrogram brings us a better idea of number of clusters (k)=4 because we see 4 groups.

# Creating clusters and assigning data into clusters
c=cutree(results,k=4)

# Plotting PCA plot
PCA.Res=PCA(CNumeric,graph=F,ncp=2,scale.unit=TRUE)
fviz_pca_ind(PCA.Res,habillage=factor(c),repel= TRUE)


# Performing KMEANS
#Define the optimal number of clusters
set.seed(13)

# Determining and visualizing the optimal number of clusters through "within cluster sums of squares"(wss), and "average silhouette"
fviz_nbclust(CNumeric_std,kmeans,method = 'wss',k.max =8)

fviz_nbclust(CNumeric_std,kmeans,method ='silhouette',k.max =8)


# INTERPRETATION: Both graphs show us that the optimal number of clusters is 2.

# Run kmeans with 2 clusters
results_k1=kmeans(x=CNumeric_std,centers=2,nstart=15)

# Plotting cluster plot
fviz_cluster(results_k1,data=CNumeric_std,labelsize=15,repel=TRUE)

# INTERPRETATION: The cluster plot of K-means show us 2 clusters