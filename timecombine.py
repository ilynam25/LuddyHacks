import pandas as pd

fall_data = pd.read_excel('fall_times.xlsx')
spring_data = pd.read_excel('spring_times.xlsx')

combined_df = pd.concat([fall_data, spring_data], ignore_index=True)

combined_df.to_excel("combined_times.xlsx", index=False)