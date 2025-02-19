# -*- coding: utf-8 -*-
"""Linear_Regression ML_IIP.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1z0cF-e_Vgaz9gkl1KrawQi6fJ_QuOt7C
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

import pandas as pd
import numpy as np

data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]

df_boston = pd.DataFrame(data, columns=[
    "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD",
    "TAX", "PTRATIO", "B", "LSTAT"
])
df_boston["price"] = target

print(df_boston.head())

df_boston.keys()

df_boston.info()

"""**Explaratory Data Analysis (EDA)
**
"""

df_boston.corr()

import seaborn as sns
sns.pairplot(df_boston)

plt.scatter(df_boston['CRIM'], df_boston['price'])
plt.xlabel('Crime rate')
plt.ylabel('price')

plt.scatter(df_boston['RM'], df_boston['price'])
plt.xlabel('Avg Rooms')
plt.ylabel('price')

plt.scatter(df_boston['LSTAT'], df_boston['price'])
plt.xlabel('LSTAT')
plt.ylabel('price')

plt.scatter(df_boston['CHAS'], df_boston['price'])
plt.xlabel('CHAS')
plt.ylabel('price')

## Independent and Dependent Features
x=df_boston.iloc[:,:-1]
y=df_boston.iloc[:,-1]
print(x.head())
print(y.head())

## Train Test Split
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=0)

x_train

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

x_train=scaler.fit_transform(x_train)
x_test=scaler.transform(x_test)

x_train

x_test

"""**Model training**

"""

from sklearn.linear_model import LinearRegression
regression=LinearRegression()
regression.fit(x_train,y_train)

print(regression.coef_)

print(regression.intercept_)

regression.get_params

reg_pred=regression.predict(x_test)
reg_pred

##Scatter plot for prediction
plt.scatter(y_test,reg_pred)

residual=y_test-reg_pred
residual

sns.displot(residual,kind="kde")

## Scatter plot wrt prediction and residuals
plt.scatter(reg_pred,residual)

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

print(mean_absolute_error(y_test,reg_pred))
print(mean_squared_error(y_test,reg_pred))
print(np.sqrt(mean_squared_error(y_test,reg_pred)))

## Performance Metrics
# R-Square
from sklearn.metrics import r2_score
score=r2_score(y_test,reg_pred)
print(score)

#Adjusted R-Square
1-(1-score)*(len(y_test)-1)/(len(y_test)-x_test.shape[1]-1)

"""** New Data Preiction**
# New Section
"""

df_boston.values[0].reshape(1,-1)

regression.predict(df_boston.data[0].reshape(1,-1))

regression.predict(df_boston.iloc[0].values.reshape(1, -1))

# Drop the target column (assuming 'target' is the name of the target column)
X_features = df_boston.drop(columns=['price'])

# Make the prediction using the first row of features
regression.predict(X_features.iloc[0].values.reshape(1, -1))

from sklearn.preprocessing import StandardScaler

# Assuming X_features is the feature set
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_features)

# Now fit your regression model to X_scaled
regression.fit(X_scaled, target)

# Scale the single row input (the first row you want to predict)
scaled_input = scaler.transform(df_boston.iloc[0, :-1].values.reshape(1, -1))

# Now predict using the scaled input
regression.predict(scaled_input)

# Assuming the target column is 'target' or the last column
y_target = df_boston['price']
# Check if regression model was trained properly with the correct features
regression.fit(X_scaled, y_target)  # Ensure X_scaled and y_target are correctly assigned
# Double-check the row you are passing for prediction
scaled_input = scaler.transform(df_boston.iloc[0, :-1].values.reshape(1, -1))  # 1 sample, n features

# Predict
predicted_value = regression.predict(scaled_input)
print(predicted_value)

import pickle
pickle.dump(regression,open('regmodel.pkl','wb'))
pickled_model=pickle.load(open('regmodel.pkl','rb'))

pickled_model.predict(scaled_input)