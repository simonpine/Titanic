import streamlit as st
import pickle
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier

st.image('./titanic.jpg', caption='Titanic banner.')

st.write('''
# Titanic Prediction
         
This app predicts if a person could survive the Titanic with some information.
         
''')

st.write('## Form:')

forPrediction = [0,0,0,0,0,0,0,0,0,0]

a = 0
b = 512.3292
A = 0.42
B = 80.0
C = 0
D = 6
c = 0
d = 8
def MinMaxScalerAge(x):
    return (x - A) / (B - A)
def MinMaxScalerFare(x):
    return (x - a) / (b - a)
def MinMaxScalerParch(x):
    return (x - C) / (D - C)
def MinMaxScalerSibSp(x):
    return (x - c) / (d - c)

embarked = st.radio(
    "Select where did you embarked:",
    ["Cherbourg", "Queenstown", "Southampton"],
)

if embarked == 'Cherbourg':
    forPrediction[7] = True
    forPrediction[8] = False
    forPrediction[9] = False
elif embarked == 'Queenstown':
    forPrediction[7] = False
    forPrediction[8] = True
    forPrediction[9] = False 
else:
    forPrediction[7] = False
    forPrediction[8] = False
    forPrediction[9] = True 

sex = st.radio(
    "Select your sex:",
    ["Male", "Female"],
)

if sex == 'Female':
    forPrediction[5] = True
    forPrediction[6] = False
else:
    forPrediction[5] = False
    forPrediction[6] = True

forPrediction[4] = MinMaxScalerFare(st.slider('Select the fare you paid:', 0, 600))
forPrediction[1] = MinMaxScalerAge(st.slider('How old you were:', 0, 100))

forPrediction[3] = MinMaxScalerParch(st.slider('Number of family relations aboard (mother, father, daughter, son, stepdaughter, stepson):', 0, 10))
forPrediction[2] = MinMaxScalerSibSp(st.slider('Number of family relations aboard (husband, wife, brother, sister, stepbrother, stepsister):', 0, 10))

forPrediction[0] = st.radio(
    "Select the class you were in:",
    [1, 2, 3],
)

# model = pickle.load(open('./trained_model_AdaBoost.pkl', 'rb'))

df_train = pd.read_csv('./train.csv')
df_train.drop(['Ticket', 'PassengerId', 'Cabin', 'Name'], axis=1, inplace = True)
df_train['Age'].fillna(df_train['Age'].mean(), inplace = True)
con_train = pd.get_dummies(df_train[['Sex', 'Embarked']])
df_train.drop(['Sex', 'Embarked'], axis=1, inplace = True)
df_train = pd.concat([df_train, con_train], axis='columns')
df_train['Fare'] = df_train['Fare'].apply(MinMaxScalerFare)
df_train['Age'] = df_train['Age'].apply(MinMaxScalerAge)
df_train['SibSp'] = df_train['SibSp'].apply(MinMaxScalerSibSp)
df_train['Parch'] = df_train['Parch'].apply(MinMaxScalerParch)
X_train = df_train.drop(['Survived'], axis=1)
y_train = df_train['Survived']

model = AdaBoostClassifier(algorithm = 'SAMME.R', learning_rate = 1, n_estimators = 150, random_state = None)
model.fit(X_train, y_train)

if st.button('Predict'):
    if model.predict([forPrediction]):
        st.write('Survived 😍')
    else:
        st.write('Death 😭')