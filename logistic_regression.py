# -*- coding: utf-8 -*-
"""Logistic regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ildIs88cMM5U9JTiTSTeyAxuwylsHKg6
"""

import pandas as pd
import plotly.express as pe
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

df = pd.read_csv('/weatherAUS.csv')

df

df.info()

df.dropna(subset=['RainToday', 'RainTomorrow'], inplace=True)

df

pe.histogram(df, x='Location', title="Location vs Rainy Days", color="RainToday")

pe.histogram(df, x='Temp3pm', title="Temperature at 3 pm vs. Rain tomorrow", color="RainTomorrow")

pe.histogram(df, x="RainTomorrow", color="RainToday", title="Raintomorrow vs RainToday")

pe.scatter(df.sample(2000), title="Min Temp vs Max Temp", x='MinTemp', y='MaxTemp', color='RainToday')

tvdf, test_df = train_test_split(df, test_size=0.2, random_state=42)
train_df, val_df = train_test_split(tvdf, test_size=0.25, random_state=42)

print(test_df.shape, "test_df")
print(val_df.shape, "val_df")
print(train_df.shape, "train_df")

plt.title('NO. of Rows Per year')
sns.countplot(x=pd.to_datetime(df.Date).dt.year);

year = pd.to_datetime(df.Date).dt.year
train_df = df[year < 2015]
val_df = df[year == 2015]
test_df = df[year > 2015]

print(test_df.shape, "test_df")
print(val_df.shape, "val_df")
print(train_df.shape, "train_df")

input_columns = list(train_df.columns)[1:-1]
target_column = 'RainTomorrow'

train_input = train_df[input_columns].copy()
train_target = train_df[target_column].copy()

val_input = val_df[input_columns].copy()
val_target = val_df[target_column].copy()

test_input = test_df[input_columns].copy()
test_target = test_df[target_column].copy()

num_cols = train_input.select_dtypes(include=np.number).columns.tolist()
categorical_cols = train_input.select_dtypes('object').columns.tolist()

train_input[categorical_cols].nunique()

im = SimpleImputer(strategy = 'mean')

df[num_cols].isna().sum()

im.fit(df[num_cols])

train_input[num_cols] = im.transform(train_input[num_cols])
val_input[num_cols] = im.transform(val_input[num_cols])
test_input[num_cols] = im.transform(test_input[num_cols])

scaler = MinMaxScaler()
scaler.fit(df[num_cols])

train_input[num_cols] = scaler.transform(train_input[num_cols])
val_input[num_cols] = scaler.transform(val_input[num_cols])
test_input[num_cols] = scaler.transform(test_input[num_cols])

"""Encoding Categorical Data"""

enc = OneHotEncoder(sparse=False, handle_unknown='ignore')

"""Creatinf a new df which contain empty categorical values changed to unknown"""

ndf = df[categorical_cols].fillna('unknown')

enc.fit(ndf)

enc_cols = list(enc.get_feature_names(categorical_cols))

train_input[enc_cols] = enc.transform(train_input[categorical_cols].fillna('unknown'))
val_input[enc_cols] = enc.transform(val_input[categorical_cols].fillna('unknown'))
test_input[enc_cols] = enc.transform(test_input[categorical_cols].fillna('unknown'))

pd.set_option('display.max_columns', None)

model = LogisticRegression(solver='liblinear')

model.fit(train_input[num_cols + enc_cols], train_target)

x_train = train_input[num_cols + enc_cols]
x_val = val_input[num_cols + enc_cols]
test_val = test_input[num_cols + enc_cols]

train_prediction = model.predict(x_train)

accuracy_score(train_target, train_prediction)

confusion_matrix(train_target, train_prediction, normalize='true')

def pp(inputs, targets, name=''):
  preds = model.predict(inputs)
  accuracy = accuracy_score(targets, preds, normalize='true')
  
  cf = confusion_matrix(targets, preds, normalize='true')
  plt.figure()
  sns.heatmap(cf, annot=True)
  plt.xlabel('Prediction')
  plt.ylabel('Target')

train_preds = pp(x_train, train_target, 'Training')

val_prediction = pp(x_val, val_target, 'validation')

