import pandas as pd

df = pd.DataFrame(columns=["Day-Part", "Start Time", "End Time"])
parts = int(input("Enter the number of day parts:"))

for _ in range(parts):
    dp = input("Enter Part of the Day ")
    st = input("Enter start time for {}".format(dp))
    et = input("Enter end time for {}".format(dp))
    df1 = pd.DataFrame(data=[[dp,st,et]],columns=["Day-Part", "Start Time", "End Time"])
    df = pd.concat([df,df1], axis=0)

df.index = range(len(df.index))
print(df)