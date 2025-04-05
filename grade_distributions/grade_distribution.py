import numpy as np
import pandas as pd
import csv


print("yamato")

num = 55 

#Num = 0 mod 3 is summer
#1 mod 3 is fall
#2 mod 3 is Spring

#1) Iterate to see which classes are available both in Spring and Fall. First, only regular academic session, <str = Course Description, avg gpa, # of students with gpa, academic class standing>

#Most recent 5 times they gave the class

df = pd.read_csv(f'grade_distributions/reportID_gradedist ({num}).csv')

print(df.columns)

'''Columns: Term Description, Term, Session, Session Description, Department, Subject, Course, Class/Section NBR, Course Description, Instructor name, GPA Grades'''


#print(df['COURSE'][0])

with open("grade_distributions\working_csv.csv", mode = 'w', newline = "") as file:
    writer = csv.writer
    pass

df = pd.read_csv(f'grade_distributions/reportID_gradedist ({num}).csv')

print(df.iloc[0])
        


