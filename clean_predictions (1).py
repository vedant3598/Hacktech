# Clean Predictions
import pandas as pd

df = pd.read_csv("recovered_365_days.csv")

update = df['44'].tolist()
last_update = pd.DataFrame()

# Adding predicted confirmed cases to dataframe
confirmed = pd.DataFrame()
for i in range(1, len(df.columns), 3):
    col = df.iloc[:, i].tolist()
    confirmed = confirmed.append(col)
    last_update = last_update.append(update)
    
# Adding latitudes to dataframe
lat = pd.DataFrame()
for i in range(2, len(df.columns), 3):
    col = df.iloc[:, i].tolist()
    lat = lat.append(col)

# Adding longitudes to dataframe
lng = pd.DataFrame()
for i in range(3, len(df.columns), 3):
    col = df.iloc[:, i].tolist()
    lng = lng.append(col) 
    
# Create complete dataset
dataset = pd.DataFrame()
dataset['Recovered'] = confirmed.iloc[:, 0]
dataset['lat'] = lat.iloc[:, 0]
dataset['lng'] = lng.iloc[:, 0]
dataset['Last Update'] = last_update.iloc[:, 0]
dataset = dataset[['Last Update', 'Recovered', 'lat', 'lng']]
dataset.to_csv("recovered_365_days_cleaned.csv", encoding='utf-8', index=False)