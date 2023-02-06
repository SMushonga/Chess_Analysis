import pandas as pd
from sklearn.impute import SimpleImputer
import numpy as np
from sklearn.model_selection import train_test_split, KFold
from sklearn.feature_selection import RFE

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plot
import scipy.stats as stats
import pylab, math
import seaborn as sb

from data_analysis import player_data, player_data_2, winrate_dist

def prepare_data(data):

    X, y = data.iloc[:, :-1].values, data.iloc[:, -1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

    #Very often it is necessary to turn samples into standardised data sets
    stdsc = StandardScaler()
    X_train_std = stdsc.fit_transform(X_train)
    X_test_std = stdsc.transform(X_test)

    return {'x_train' : X_train_std, 'x_test' : X_test_std, 'y_train' : y_train, 'y_test': y_test}

#We initially just applied simple linear regression to see the base line outcome
def train_linear(data_dict):
    regression = LinearRegression()
    regression.fit(data_dict['x_train'], data_dict['y_train'])

    print(regression.score(data_dict['x_test'], data_dict['y_test']))
    y_pred = regression.predict(data_dict['x_test'])
    residuals = data_dict['y_test'] - y_pred
    sb.displot(residuals, kde=False)
#test_1 = prepare_data(player_data)
#test = prepare_data(player_data_2)
#train_linear(test)
#train_linear(test_1)

#player_data scores 0.36, and player_data_2 scores 0.4

#This indicates that a linear fit is inadequate, let explore this more before giving up the linear model

#Now the real work begins and we work to improve the score
#First point of contention is our feature selection, we have applied filtering via looking at the pearson coefficients -> let us apply more feature selection methods

#We are performing feature selection on the original data to see if the it disagrees with our accessments
test = prepare_data(player_data)
rfe_selector = RFE(estimator=LinearRegression(),n_features_to_select = 4, step = 1)
rfe_selector.fit(test['x_train'], test['y_train'])
test['x_train'].columns[rfe_selector.get_support()]

player_data_inliers = player_data_2.query("win_rate < 0.57 and win_rate > 0.4 ")

train_linear(test)
plot.show()