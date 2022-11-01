from dataclasses import dataclass
import pandas as pd
from dateutil import parser
import numpy as np
import matplotlib.pyplot as plt

#reading in the data

dfa = pd.read_csv('data\halloween2019a.csv', sep= ',')
dfb = pd.read_csv('data\halloween2019b.csv', sep=',')
dfc = pd.read_csv('data\halloween2019c.csv', sep=',')
df1 =pd.read_csv('data\halloween2022.csv', sep=',')

#getting column names for each file

columns_in_a = dfa.columns
columns_in_b = dfb.columns
columns_in_c = dfc.columns
columns_in_1 = df1.columns

#printing the column names
print(columns_in_a)
print(columns_in_b)
print(columns_in_c)
print(columns_in_1)

""" finding null values in each dataframe, aside from my collected data, before merging"""

nullsa = dfa.isna().sum()

nullsb = dfb.isna().sum()

nullsc = dfc.isna().sum()


"""getting rid of null values in each dataframe"""

dfa = dfa.dropna(subset=['FirstName'])
dfa= dfa.dropna(subset=['DOB'])
dfa = dfa.dropna(subset=['DOD'])

dfb = dfb.dropna(subset= [' DOD'])
dfb = dfb.dropna(subset= [' Sex'])

dfc = dfc.dropna(subset=['DOB'])
dfc = dfc.dropna(subset=['DOD'])

""" getting rid of the middle name column in dataframe a"""

dfa.drop('MiddleName', axis=1, inplace=True)


""" combining first & last name into one column called name"""

dfa['Name'] = dfa['FirstName'] + ' ' + dfa['LastName']
dfa.drop('FirstName', axis=1, inplace=True)
dfa.drop('LastName', axis=1, inplace=True)
dfa = dfa.reindex(columns=['Name', 'DOB', 'DOD'])

dfb['Name'] = dfb['FirstName'] + ' ' + dfb[' LastName']
dfb.drop('FirstName', axis=1, inplace=True)
dfb.drop(' LastName', axis=1, inplace=True)
dfb = dfb.reindex(columns= ['Name', ' DOB', ' DOD', ' Sex'])


""" changing sex to m or f """
dfb[' Sex'].mask(dfb[' Sex']=='Male', 'm', inplace=True)
dfb[' Sex'].mask(dfb[' Sex']== 'Female', 'f', inplace=True)
dfb[' Sex'].mask(dfb[' Sex']== 'female', 'f', inplace=True)
dfb[' Sex'].mask(dfb[' Sex']== 'male', 'm', inplace=True)
dfb[' Sex'].mask(dfb[' Sex']== 'F', 'f', inplace=True)
dfb[' Sex'].mask(dfb[' Sex']== 'M', 'm', inplace=True)

dfc['Sex'].mask(dfc['Sex']== 'Male', 'm', inplace=True)
dfc['Sex'].mask(dfc['Sex']== 'Female', 'f', inplace=True)

""" removing the spacing before the column names"""
dfb = dfb.rename(columns= {' DOB': 'DOB', ' DOD': 'DOD', ' Sex': 'Sex'})
print(dfb.columns)


"""combining dataframes, minus dfa since there was no gender column """

dfcombined = df1.append([dfb, dfc])
print(dfcombined.head())

""" changing format of DOB and DOD so that all are matching. I only need the years."""

print(dfcombined['DOB'].dtypes)

dfcombined['DOB'] = dfcombined['DOB'].astype(str)
dfcombined['DOB'] = dfcombined['DOB'].apply(parser.parse).dt.strftime('%Y')

dfcombined['DOD'] = dfcombined['DOD'].astype(str)
dfcombined['DOD'] = dfcombined['DOD'].apply(parser.parse).dt.strftime('%Y')

""" calculating lifespan & adding a new column"""

dfcombined['DOD'] = dfcombined['DOD'].astype(int)
dfcombined['DOB'] = dfcombined['DOB'].astype(int)
dfcombined['Lifespan'] = dfcombined['DOD'] - dfcombined['DOB']

""" Identify outliers by using an interquartile range """

q3, q1 = np.percentile(dfcombined['Lifespan'], [75,25])
iqr = q3 -q1
print(iqr)

""" removing entries where lifespan is negative and below 10"""

dfcombined.drop(dfcombined[dfcombined['Lifespan']< 0].index, inplace=True)
dfcombined.drop(dfcombined[dfcombined['Lifespan']< 10].index, inplace=True)

"""finding overall median lifespan"""
median_lifespan = dfcombined['Lifespan'].median()
average_lifespan = dfcombined['Lifespan'].mean()
print(median_lifespan)
print(average_lifespan)

"""finding mean lifespan by sex

first I have to clean the data some more because several m/f had a space in front of them."""
dfcombined['Sex'] = dfcombined['Sex'].astype(str)
dfcombined['Sex'].mask(dfcombined['Sex']== ' f', 'f', inplace=True)
dfcombined['Sex'].mask(dfcombined['Sex']== ' m', 'm', inplace=True)


mean_lifespan_by_sex = dfcombined.pivot_table(
    values = 'Lifespan',
    index = 'Sex',
    columns= 'DOB',
    aggfunc = 'mean'
)
print (mean_lifespan_by_sex)

"""doing some basic plots"""

mean_lifespan_by_sex.plot(kind='bar', title= 'lifespan by sex')
plt.savefig('lifespan_boxplot.png')
dfcombined.plot(kind='hist', column='Lifespan')
plt.show()
dfcombined.plot(kind='box', column='Lifespan')
plt.show()