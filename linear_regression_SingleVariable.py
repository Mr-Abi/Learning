# -*- coding: utf-8 -*-
"""Linear Regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CCk_BLdoiSBRbZ_deR8M3oTgv-nWwG3c
"""

medical_charges_url = 'https://raw.githubusercontent.com/JovianML/opendatasets/master/data/medical-charges.csv'

from urllib.request import urlretrieve
urlretrieve(medical_charges_url, 'medical.csv')

import pandas as pd
medical_df = pd.read_csv('medical.csv')
medical_df

medical_df.info()

medical_df.describe()

# Commented out IPython magic to ensure Python compatibility.
import plotly.express as px
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

sns.set_style('darkgrid')
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['figure.figsize'] = (10, 6)
matplotlib.rcParams['figure.facecolor'] = '#00000000'

medical_df.age.describe()

fig = px.histogram(medical_df, x = 'age', marginal = 'box', 
                   nbins=47, title='Distribution of age')
fig.update_layout(bargap=0.1)
fig.show()

fig = px.histogram(medical_df, x = 'bmi', marginal = 'box', 
                   color_discrete_sequence=['red'], title='Distribution of BMI')
fig.update_layout(bargap=0.1)
fig.show()

fig = px.histogram(medical_df, x='charges', marginal='box', color='smoker', 
                   color_discrete_sequence=['red', 'green'], title='Annual Medical Charges')
fig.update_layout(bargap=0.1)
fig.show()

fig = px.histogram(medical_df, x='charges', marginal='box', color='sex', color_discrete_sequence=['pink', 'blue'])
fig.update_layout(bargap=0.1)
fig.show()

fig = px.histogram(medical_df, x="charges", color='region', 
                   color_discrete_sequence=['pink', 'red', 'blue', 'grey'])
fig.update_layout(bargap=0.1)
fig.show()

fig = px.histogram(medical_df, x='sex', color='region', 
                   color_discrete_sequence=['red', 'green', 'pink', 'blue'])
fig.update_layout(bargap=0.1)
fig.show()



fig = px.histogram(medical_df, x='age', color='sex', 
                   color_discrete_sequence=['pink', 'blue'])
fig.update_layout(bargap=0.1)
fig.show()

fig = px.histogram(medical_df, x='bmi', color='sex', 
                   color_discrete_sequence=['pink', 'blue'])
fig.update_layout(bargap=0.1)
fig.show()

medical_df.smoker.value_counts()

f = px.histogram(medical_df, x='smoker', color='sex', 
                 color_discrete_sequence=['pink', 'blue'], title='Smoker')
f.update_layout(bargap=0.1)
f.show()

fig = px.scatter(medical_df, x='age', y='charges', color='smoker', 
      opacity=0.7, hover_data=['sex', 'region'], title='Age vs Charges')
fig.update_traces(marker_size=5)
fig.show()

f = px.scatter(medical_df, x='bmi', y='charges', opacity=.7, color='smoker',
               hover_data=['sex', 'region'], title='BMI vs Charges')
f.update_traces(marker_size=5)
f.show()

medical_df.charges.corr(medical_df.age)

medical_df.charges.corr(medical_df.bmi)

medical_df.charges.corr(medical_df.children)

smoker_values = {'no':0, 'yes':1}
smoker_numeric = medical_df.smoker.map(smoker_values)
medical_df.charges.corr(smoker_numeric)

medical_df.corr()

sns.heatmap(medical_df.corr(), cmap='Reds', annot=True)
plt.title('Correlation Coefficient');

non_smokers_df = medical_df[medical_df.smoker == 'no']

fig = px.scatter(non_smokers_df, x='age', y='charges', 
                 opacity=.7, title='Age vs Charges (Non Smokers)', hover_data=['sex'])
fig.update_traces(marker_size=5)
fig.show()

def estimate_charges(age, w, b):
  return w * age + b

w = 50
b = 100

ages = non_smokers_df.age
estimated_charges = estimate_charges(ages, w, b)

# plot the estimated charges using line graph
plt.plot(ages, estimated_charges, 'r-o');
plt.xlabel('age');
plt.ylabel('Estimated Charges');

target = non_smokers_df.charges

plt.plot(ages, estimated_charges, 'r', alpha=0.9);
plt.scatter(ages, target, s=8, alpha=0.8);
plt.xlabel('age');
plt.ylabel('charges');
plt.legend(['Estimate', 'Actual']);

def try_parameters(w, b):
  ages = non_smokers_df.age
  target = non_smokers_df.charges

  estimated_charges = estimate_charges(ages, w, b)
  plt.plot(ages, estimated_charges, 'r', alpha=0.9);
  plt.scatter(ages, target, s=8, alpha=0.8);
  plt.xlabel('age');
  plt.ylabel('charges');
  plt.legend(['Estimate', 'Actual']);

try_parameters(60, 200)

try_parameters(400, 5000)

try_parameters(400, 2000)

try_parameters(30, 5000)

import numpy as np

def rmse(targets, predictions):
  return np.sqrt(np.mean(np.square(targets-predictions)))

w = 50
b = 100

try_parameters(w, b)

targets = non_smokers_df['charges']
predicted = estimate_charges(non_smokers_df.age, w, b)

rmse(targets, predicted)

def try_parameters(w, b):
  ages = non_smokers_df.age
  target = non_smokers_df.charges
  predictions = estimate_charges(ages, w, b)

  estimated_charges = estimate_charges(ages, w, b)
  plt.plot(ages, estimated_charges, 'r', alpha=0.9);
  plt.scatter(ages, target, s=8, alpha=0.8);
  plt.xlabel('age');
  plt.ylabel('charges');
  plt.legend(['Estimate', 'Actual']);

  loss = rmse(target, predictions)
  print("RMSE Loss: ", loss)

try_parameters(50, 100)

from sklearn.linear_model import LinearRegression

model = LinearRegression()
help(model.fit)

inputs = non_smokers_df[['age']]
targets = non_smokers_df[['charges']]

print('inputs.shape:', inputs.shape)
print('targets.shape:', targets.shape)

model.fit(inputs, targets)

model.predict(np.array([[23], [37], [61]]))

predictions = model.predict(inputs)
predictions

rmse(targets, predictions)

model.coef_
model.intercept_
try_parameters(model.coef_[0][0], model.intercept_[0])