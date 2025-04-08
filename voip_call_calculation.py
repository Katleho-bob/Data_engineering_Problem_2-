import pandas as pd

# Load the Excel file
df = pd.read_excel('Data_Engineer_ipdr.xlsx')

# Check the first few rows to understand the structure
print(df.head())
