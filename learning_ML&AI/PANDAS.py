from pandas import read_csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv_file = "learning_ML&AI/data/Product Dataset.csv"
csv_file2 = "learning_ML&AI/data/Athletes Dataset.csv"
csv_file3 = "learning_ML&AI/data/noc_regions.csv"
data = pd.read_csv(csv_file)
athlete_data = pd.read_csv(csv_file2)
noc_regions_data = pd.read_csv(csv_file3)
# print(data.head())

# LOC AND ILOC(only index) - accesing rows and columns -----------------------------------------------------------
# print(data.loc[0:, "Name"])
# print(data.iloc[0, 1])

# FILTERING DATA -----------------------------------------------------------------------
# print(data[data['Name'].str.contains('Vitamin|Liquid', case=False)])
# print(data[data['Name'].isin(["Moisturizing", "Shampoo"]) & (data['Sold'] > 10)])
# print(data[data['Name'].str.contains('Vitamin|Liquid', case=False)])
# print(data.query('Name == "Shampoo"'))

# ADDING - UPDATING -----------------------------------------------------------------------------
# data['new_price'] = np.where(data['Name'] == 'Shampoo', 100, 899)
# data['Price'] = 89.00

# delete_col = data.drop(columns=['Sold'], inplace=True)  # 'inpalce=True - modify or reset the memory
# print(delete_col)

# data['Revenue'] = data['Price'] * data['Sold']
# rename = data.rename(columns={'new_price':'Price'}) #Rename column header
# print(data[['Price', 'Sold', 'Revenue']])
# print(rename)

# delete_column = athlete_data.drop(columns=['Year of birth'], inplace=True)
# # print(athlete_data['Year of birth'])
# athlete_data['First name'] = athlete_data['Name'].str.split(' ').str[0]
# athlete_data['born_dateyear'] = pd.to_datetime(athlete_data['Birth Date'], dayfirst=True)
# athlete_data['Year of Birth'] = athlete_data['born_dateyear'].dt.year
# athlete_data['Month of Birth'] = athlete_data['born_dateyear'].dt.month_name()

# athlete_data.to_csv('./uploads/new.csv', index=False) #Save csv

# athlete_data['Height Category'] = athlete_data['Height (cm)'].apply(lambda x: 'Short' if x < 185 else ('Average' if x < 190 else 'Tall'))

# print(athlete_data.head())
# print(athlete_data.info())

# MERGING AND CONCATENATING DATA -----------------------------------------------------------------------------
# athlete_data_new = pd.merge(athlete_data, noc_regions_data, left_on='NOC', right_on='NOC', how='left')
# print(athlete_data_new.head())

# print(athlete_data.head())
# print(noc_regions_data.head())

# HANDLING NULL VALUES
# athlete_data.dropna(subset=['Medal'], inplace=True) # Drop the rows with NaN specificall based on 'subset'
# print(athlete_data.isna().sum())
# print(athlete_data.notna().sum())
# print(athlete_data[athlete_data['Medal'].notna()][['Name', 'Age', 'Medal']])
# print(athlete_data[['Name', 'Age', 'Medal']])
# athlete_data['Medal'].fillna("Silver", inplace=True)
# print(athlete_data.head())

# AGGREGATING DATA -------------------------------------------------------------------------------
# group_by = data.groupby(['Name'])['Sold'].sum() # Grouped multiple things
# group_by = data.groupby(['Name']).agg({'Sold': 'sum', 'Price': 'mean'})
# print(group_by)
# data.groupby(['Name'])['Sold'].sum().plot(kind='pie', title='Based on Number of Solds')
# plt.show()

counts = athlete_data.groupby(['NOC'])['NOC'].value_counts().sample(10)
# print(x_value)
# athlete_data.groupby(['NOC'])['NOC'].value_counts().sample(20).sort_values().plot(kind="bar")
counts.plot(kind="bar", color="red")
plt.xlabel("NOC")
plt.ylabel("Total counts of each NOC participated")
plt.xticks(rotation=60)
plt.show()
# print(group_by)





# HORIZONAL BAR GRAPH--------------------------------------------------------------------------------------
# df = data.groupby('Name')['Sold'].max().sort_values(ascending=False).head(10).sort_values().plot(kind='barh', figsize=(5, 10), title='Based on Number of Solds')
# plt.show()


# data = {
#   "Name": ["Mark", "Piolo", "Yasmin", "Soba"],
#   "Age": [21, 22, 23, 24],
#   "Job": ["Developer", "Software Engineering", "Data Analysis", "Researcher"]
# }

# df = pd.DataFrame(data)
# print(df)