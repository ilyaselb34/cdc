"""
Author: Ilyas El Boujadaini

Content: Analysis of simulated data (calculation of average charge per day)
"""

#import necessary libraries
import os   #for paths
import sys #for paths

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
path_repo = str(os.path.dirname(current_dir))

import csv  #for importing and exporting data
import pandas as pd #for dataframes
import datetime as dt   #for dates


entry_path = os.path.join('..', 'output', '00_simulation_20min_const.csv') #path to the simulated data file, adapted to the user's OS
simul=[]    #list that will hold the data

with open(entry_path, "r", newline='', encoding='utf-8') as csv_file:    #file opening
    csv_reader = csv.reader(csv_file, delimiter=";")
    for line in csv_reader:
            line[0]=dt.datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')   #converting the date to datetime format
            line[1]=int(line[1])  #converting the charge to integer for averaging
            simul.append(line)

def average_daily_charge(simul):
    df=pd.DataFrame(simul,columns=['date','charge'])   #creating a dataframe for easier calculations
    daily_average = df.groupby(df['date'].dt.date)['charge'].mean().reset_index()   #calculating the average charge per day
    return daily_average

res=average_daily_charge(simul)
print(res.head(5))

exit_path = os.path.join('..', 'output', '01_simulation_analysis.csv')
res.to_csv(exit_path, sep=';', index=False, header=False, encoding='utf-8')