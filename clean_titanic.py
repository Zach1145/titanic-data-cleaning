# Copyright (c) 2025 [Zachary Bower]
# Licensed under the MIT License. See LICENSE file in the repository root.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sqlite3 import Error

# Read in the csv file
df = pd.read_csv('train.csv')

# Drop any duplicate rows
df.drop_duplicates(inplace=True)

# Drop unneeded columns
df.drop(['Name', 'Ticket', 'Cabin', 'Fare'], axis=1, inplace=True)

# Fill in missing ages with the mean of all ages
df.fillna({'Age': round(df['Age'].mean())}, inplace=True)

# Fill in missing embarked locations with the most common one, Standardize input capitalization
df.fillna({'Embarked': df['Embarked'].mode()[0]}, inplace=True)
df['Embarked'] = df['Embarked'].str.lower()

# Save cleaned data to csv
df.to_csv('titanic_cleaned.csv', index=False)

# Connect to the database (or create if it doesn't exist)
connection = sqlite3.connect('titanic.db')
cursor = connection.cursor()

# Convert Cleaned Data to SQL Table and Save to Database
df.to_sql('titanic', connection, if_exists='replace', index=False)

# Create Visualizations
# Bar chart: Survival rate by gender
sns.barplot(x='Sex', y='Survived', data=df)
plt.title('Survival Rate by Gender')
plt.savefig('survival_by_gender.png')
plt.close()

# Histogram: Age distribution
plt.hist(df['Age'], bins=20)
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('Count')
plt.savefig('age_distribution.png')
plt.close()