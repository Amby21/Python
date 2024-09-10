#%%
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#%%
#Import Data
data_info = pd.read_csv('lending_club_info.csv',index_col='LoanStatNew')
data_info.head(10)

# %%
def feat_info(col_name):
    print(data_info.loc[col_name]['Description'])

feat_info('pub_rec_bankruptcies')

# %%
data_info.info()

# %%
df = pd.read_csv('lending_club_loan_two.csv')
df.info()

# %%
null_counts = df.isnull().sum()
print(null_counts)

# %%
#Countplot on loan_status
sns.countplot(x='loan_status',data=df,hue='loan_status')

# %%
sns.histplot(data=df,x='loan_amnt')

#%%
df['term']=df['term'].apply(lambda term: int(term[:3]))

# %%
df.corr()

#%%
sns.heatmap(df.corr(),annot=True)

#%%
# Exploratory Data Analysis
sns.boxplot(x='loan_status',y='loan_amnt',data=df,hue='loan_status')
df.groupby('loan_status')['loan_amnt'].describe()

#%%
sns.countplot(x='grade',data=df,hue='loan_status')

#%%
# Creating a new column called loan_repaid which will contain a 1 if the loan status was "Fully Paid" and a 0 if was "Charged Off"
df['loan_repaid'] = df['loan_status'].map({'Fully Paid':1,'Charged Off':0})

#%%
df.corr()['loan_repaid'].sort_values().drop('loan_repaid').plot(kind='bar')

#%%
# Working with Missing Data
#removing job title 
df = df.drop('emp_title',axis=1)

# %%
print(sorted(df['emp_length'].dropna().unique()))
emp_length_order = ['< 1 year','1 year', '2 years', '3 years', '4 years', '5 years', '6 years', '7 years', '8 years', '9 years','10+ years']

#%%
plt.figure(figsize=(12,4))
sns.countplot(x='emp_length',data=df,order = emp_length_order,hue='loan_status')

# %%
emp_co = df[df['loan_status'] == 'Charged Off'].groupby('emp_length').count()['loan_status']

# %%
emp_fp = df[df['loan_status'] == 'Fully Paid'].groupby('emp_length').count()['loan_status']

# %%
emp_len = emp_co/(emp_co+emp_fp)

#%%
emp_len.plot(kind='bar')

# %%
df = df.drop('emp_length',axis=1)

#%%
# check if purpose and title column hold the same info.
feat_info('title')

# %%
df = df.drop('title',axis=1)

# %%
#Find mort_acc represents
feat_info('mort_acc')

# %%
df['mort_acc'].value_counts()

#%%
# Collecting all numeric columns
df_numeric = df.select_dtypes(include=[float, int])

# %%
df_numeric.corr()['mort_acc'].sort_values()

# %%
feat_info('grade')

# %%
# to fill empty values in mort_acc because total_acc is most corelated with mort_acc

total_acc_avg = df.groupby('total_acc')['mort_acc'].mean()

#%%
# Function to see if there is an empty mort_acc value it will fill it up with the avergae from the look-up table 
def fill_mort_acc(total_acc,mort_acc):
    if np.isnan(mort_acc):
        return total_acc_avg[total_acc]
    else:
        return mort_acc

#%%
df['mort_acc']=df.apply(lambda x: fill_mort_acc(x['total_acc'],x['mort_acc']),axis=1)

#%%
df = df.dropna()

# %%
print(df.dtypes)

# Categorical Data

# %%
# find non-numeric columns
categorical_cols = df.select_dtypes(['object']).columns

# %% TERM
df['term'].value_counts()
sns.countplot(x='term',data=df)

# %%
df['term'].value_counts()

# %%
df = df.drop('grade',axis=1)

# %%
dummies = pd.get_dummies(df['sub_grade'],drop_first=True)

df = pd.concat([df.drop('sub_grade',axis=1),dummies],axis=1)

#%%
dummies = pd.get_dummies(df[['verification_status','application_type','initial_list_status','purpose']],drop_first=True)

df = pd.concat([df.drop(['verification_status','application_type','initial_list_status','purpose'],axis=1),dummies],axis=1)

#%% Home ownership

df['home_ownership'].value_counts()

# %%
# replace none and any category with other.Because the collective sum of none and any is just 32

df['home_ownership'] = df['home_ownership'].replace(['NONE','ANY'],'OTHER')

#%%
dummies = pd.get_dummies(df['home_ownership'],drop_first=True)
df = pd.concat([df.drop('home_ownership',axis=1),dummies],axis=1)

# %%
df['zip_code'] = df['address'].apply(lambda address:address[-5:])

# %%
df['zip_code'].value_counts()

# %%
dummies = pd.get_dummies(df['zip_code'],drop_first=True)

df = pd.concat([df.drop('zip_code',axis=1),dummies],axis=1)

# %%
df = df.drop('address',axis=1)

# %%
#dropping issue date as the analysis is before the issue of a loan
df = df.drop('issue_d',axis=1)

# %%
df['earliest_cr_line'] = df['earliest_cr_line'].apply(lambda date:int(date[-4:]))

# %%
df['earliest_cr_line']

# %%
from sklearn.model_selection import train_test_split

#%%
df = df.drop('loan_status',axis=1)

#%%
X = df.drop('loan_repaid',axis=1).values
y = df['loan_repaid'].values

#%%
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=101)

#%% 
# Step 1: Separate categorical and numeric columns
# Check for columns with object or string data types (usually categorical)
categorical_cols = X_train.select_dtypes(include=['object']).columns

#%%
# Step 2: Apply encoding to the categorical columns
# You can use one-hot encoding or label encoding
# Example using pandas get_dummies (for one-hot encoding)
X_train_encoded = pd.get_dummies(X_train, columns=categorical_cols, drop_first=True)

#%%
# Step 3: Apply scaling to only the numeric columns
from sklearn.preprocessing import StandardScaler

#%%
# Select only numeric columns (after encoding, all columns should be numeric)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)

#%%
X_test = scaler.transform(X_test)

# %%
# Creating the Model
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

model = Sequential()

#%%
X_train.shape()
# %% Creating the model
model.add(Dense(78,activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(39,activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(19,activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(units=1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam')
print('created')

#%%
model.fit(x=X_train,y=y_train,epochs=25,batch_size=256,validation_data=(X_test,y_test))
# %%

# %%
print(X_train.dtype)
print(X_test.dtype)
print(y_train.dtype)
print(y_test.dtype)
# %%
print(np.isnan(X_train).any())  # Should be False
print(np.isnan(y_train).any())  # Should be False

# %%
# To SAVE THE MODEL
model.save('lending_club_model.h5')

#%%
losses = pd.DataFrame(model.history.history)

# %%
losses.plot()

# %%
from sklearn.metrics import classification_report,confusion_matrix
#%%
predictions = model.predict(X_test)
predicted_classes = (predictions > 0.5).astype("int32")
#%%
print(classification_report(y_test,predicted_classes))

# %%
# New Customer Evaluation
import random
random.seed(101)
random_ind = random.randint(0,len(df))

#%%
new_customer = df.drop('loan_repaid',axis=1).iloc[random_ind]
new_customer

# %%
new_customer = scaler.transform(new_customer.values.reshape(1,78))

# %%
predict  = model.predict(new_customer)
predicted_class = (predict > 0.5).astype("int32")
#%%
predicted_classes = (predictions > 0.5).astype("int32")

#%%
df.iloc[random_ind]['loan_repaid']
# %%
