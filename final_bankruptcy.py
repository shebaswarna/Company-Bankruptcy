# -*- coding: utf-8 -*-
"""Final_Bankruptcy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19_Mjin4TeXmiiZxwPKbNYgy-ckGJtFGd

# Importing the libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

"""# Importing the dataset"""

dataset = pd.read_csv('data.csv.zip')
X = dataset.iloc[:,1:]
y = dataset.iloc[:,0]

dataset.head()

dataset.describe()   #to see the min/max values of all the columns

plt.hist(dataset[' Operating Gross Margin'])

plt.hist(dataset[' Research and development expense rate'])

dataset.info()   #to see if there are any null values in the data set

{columns : len(dataset[columns].unique()) for columns in dataset} #to check if there ane any columns having a single values

dataset.drop(' Net Income Flag', axis = 1, inplace = True)       # The 'Net Income Flag' column is dropped because it consists of only one value i.e. 1.

dataset.head()

"""# Visualizing the Dataset"""

Bankrupt = dataset[dataset['Bankrupt?']==1]
Not_Bankrupt = dataset[dataset['Bankrupt?']==0]

print("Total =", len(dataset))

print("Number of companies that are Bankrupt =", len(Bankrupt))
print("Percentage of bankrput companies  =", 1.*len(Bankrupt)/len(dataset)*100.0, "%")
 
print("Number of companies that are NOT Bankrupt =", len(Not_Bankrupt))
print("Percentage of not bankrupt companies =", 1.*len(Not_Bankrupt)/len(dataset)*100.0, "%")

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Bankrupt', 'Not_Bankrupt'
sizes = [len(Bankrupt), len(Not_Bankrupt)]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.'''
plt.rcParams['figure.figsize'] = [5,5]
plt.show()

"""# Splitting the dataset"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

X_train

"""# Feature Scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = pd.DataFrame(sc.fit_transform(X_train), index=X_train.index, columns=X_train.columns)
X_test = pd.DataFrame(sc.transform(X_test), index=X_test.index, columns=X_test.columns)

X_train.head()

X_test.head()

"""## Training the Model

"""

original_models = {
    "       Logistic Regression" : LogisticRegression(random_state = 0),
    "    Support Vector Machine" : SVC(kernel = 'linear', random_state = 0),
    "             Decision Tree" : DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
}
for name, model in original_models.items():
  model.fit(X_train, y_train)
  print(name + ' trained')

original_results = []

for name,model in original_models.items():
  result = model.score(X_test, y_test)
  original_results.append(result)
  print(name + " : {:.2f}%".format(result*100))

"""# Dimensionality reduction"""

from sklearn.decomposition import PCA
n_components = 95
pca = PCA(n_components = n_components)
X_train_reduced = pd.DataFrame(pca.fit_transform(X_train), index=X_train.index, columns=['PC'+ str(i) for i in range(1, n_components+1)])
X_test_reduced = pd.DataFrame(pca.transform(X_test), index=X_test.index, columns=['PC'+ str(i) for i in range(1, n_components+1)])

X_test_reduced

X_test_reduced.describe()

pca.explained_variance_ratio_

import seaborn as sns
sns.barplot(x = ['PC'+ str(i) for i in range(1, n_components+1)], y = pca.explained_variance_ratio_)
sns.set(rc= {'figure.figsize':(20,10)})
plt.ylabel('Variance Ratio')
plt.xticks(rotation=90)
plt.show()

n_components_2 = 10
pca_2 = PCA(n_components = n_components_2)
X_train_reduced2 = pd.DataFrame(pca_2.fit_transform(X_train), index=X_train.index, columns=['PC'+ str(i) for i in range(1, n_components_2+1)])
X_test_reduced2 = pd.DataFrame(pca_2.transform(X_test), index=X_test.index, columns=['PC'+ str(i) for i in range(1, n_components_2+1)])

X_test_reduced

X_test_reduced2

pca_2.explained_variance_ratio_

import seaborn as sns
sns.barplot(x = ['PC'+ str(i) for i in range(1, n_components_2+1)], y = pca_2.explained_variance_ratio_)
sns.set(rc= {'figure.figsize':(20,10)})
plt.ylabel('Variance Ratio')
plt.xticks(rotation=90)
plt.show()

reduced_models = {
    "       Logistic Regression" : LogisticRegression(random_state = 0),
    "    Support Vector Machine" : SVC(kernel = 'linear', random_state = 0),
    "             Decision Tree" : DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
}
for name, model in reduced_models.items():
  model.fit(X_train_reduced, y_train)
  print(name + ' trained')

reduced_models_2 = {
    "       Logistic Regression" : LogisticRegression(random_state = 0),
    "    Support Vector Machine" : SVC(kernel = 'linear', random_state = 0),
    "             Decision Tree" : DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
}
for name, model in reduced_models_2.items():
  model.fit(X_train_reduced2, y_train)
  print(name + ' trained')

reduced_results = []

for name, model in reduced_models.items():
  result = model.score(X_test_reduced, y_test)
  original_results.append(result)
  print(name + " : {:.2f}%".format(result*100))

reduced_results2 = []

for name, model in reduced_models_2.items():
  result = model.score(X_test_reduced2, y_test)
  original_results.append(result)
  print(name + " : {:.2f}%".format(result*100))

