import pandas as pd

getfile = pd.read_csv('F1_Data\lap_times.csv')

dataframe = pd.DataFrame(getfile)

for index, row in dataframe.iterrows():
 
  if (row['raceId'] < 860):
    print(str(row['raceId']) + " We need to delete this data")
    dataframe.drop(index)


print("Done!!!!")
dataframe.to_csv("F1_Data\lap_times.csv", index=False)