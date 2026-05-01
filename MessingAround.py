import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

try:
    df = pd.read_csv("Teen_Mental_Health_Dataset.csv")
    #print(df.describe())
    #gender_ave_st = df.groupby("gender")["daily_social_media_hours"].mean()
    #print(gender_ave_st)
    gender = df.groupby("gender")["daily_social_media_hours"].describe()
    print(gender)
    #gender_based.plot(title="Gender-Screentime Graph", kind="bar")
    #plt.xticks(rotation=45)
    #plt.show()
    

except Exception as e:
    print(f"Error fetching data: {e}")

