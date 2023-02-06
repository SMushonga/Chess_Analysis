import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
import scipy.stats as stats
import pylab, math
import seaborn as sb

#We read in the data we've collected from chess.com to clean and analysis
player_data = pd.read_csv('player_data.csv')
player_data.drop_duplicates(inplace=True)

#Immediately we want to determine how many empty entries there are in our dataframe
#print(player_data.isnull().sum())

#Using this we can see that no column is particularly bad, so no features have to be dropped completely at this point
player_data = player_data.drop(columns=['puzzle_rush_score', 'puzzle_rush_attempts'])

#We still drop rows with any omissions - Alternatively we could fill these slots with the mean, median, mode or any other value
player_data = player_data.dropna(axis=0)
#player_data.fillna(player_data.mean(), inplace=True)

#Now that we have removed samples with "None" variables, we reset the index for aesthetics
player_data = player_data.reset_index()
player_data = player_data.drop(columns=['index'])

player_data_2 = player_data.copy()
#we createa player_data_2 for training to compare with data uncleaned

#Now we can begin to look at the data analysis by getting the summary statistics for our dataset
#print(player_data.describe())

#We want to get a better understanding of the distribution of our target variable
def winrate_dist(dist):
    winrate = dist['win_rate'].to_numpy()
    stats.probplot(winrate, dist="norm", plot=pylab)
    sb.displot(winrate, kde=False)
#Winrate does not follow the probability plot for a normal distribution with a straight line, rather has a sharp upwardly spike at the higher end values 
#This indicates that their are significant outliers at the top end of our data and the slight S shape also indicates a short tail besides the outliers

#Looking at the distribution, we can see it is right/positively skewed, with some extremely outliers with extremely high winrates
#This indicates to me that we may have to split the data and use two models to accurately predict winrate

#Now that we've looked at the targets, let's analyse the feature - firstly, do the features themselves have outliers
#For the plotting purposes, normalised data works better
def check_feature_outlier(dist):
    normalised_df=(dist-dist.mean())/dist.std()
    plot.boxplot(normalised_df)
    sb.displot(normalised_df, kde=False)

#Attributes 2,5,8 - the rd of the time controls, denoting the paramater that determines how 'certain' yor rating is - are positively skewed like our target. This indicates a potentially good feature
#These attribute may also aallow us to have an attribute we use to choose which model to apply if we train two different data sets


#Now we analyse the relationships inbetween the features
def relationships_features(dist):
    print(dist.corr())
    sb.heatmap(dist.corr(), annot=True, cmap='magma')
    sb.pairplot(dist)
#Looking at the features and the correlation coefficients of 0.8+ between features, we can tell that if we don't remove some attributes, there will be major colinearity issues.
#We therefore remove the three best_rating colums, as well as the bullet_last_rating and rapid_last_rating
#Further, the rd scores are not correlated with anything in any significant way, as most values are approximately 0 so we remove those columns

#Now that we have eliminated a few features, let's visualise how our feature relate to the targets with mt favourite graph: parallel co-ordinate plot
def paralle_co_o(dist):
    normalised_df=(dist-dist.mean())/dist.std()
    for i in range(len(dist.index)):
        #plot rows of data as if they were series data
        dataRow = normalised_df.iloc[i,0:-1]
        labelColor = 1.0/(1.0 + math.exp(-normalised_df.iloc[i, -1]))
        dataRow.plot(color=plot.cm.RdYlBu(labelColor), alpha=0.5)
    plot.xlabel("Attribute Index")
    plot.ylabel(("Attribute Values"))
#this graph applies a colour gradient to samples based on the label, similarly coloured lines have similar labels
#We are looking for groupings of similarly colored samples to indicate that a feature is a good predictor of the target
player_data = player_data.drop(columns=['blitz_best_rating', 'bullet_best_rating', 'rapid_best_rating', 'rapid_last_rating', 'bullet_last_rating', 'bullet_last_rd','blitz_last_rd', 'rapid_last_rd'])
plot.show()







