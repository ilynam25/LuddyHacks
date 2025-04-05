import pandas as pd
 

data = pd.read_excel('soc4258.xls.xlsx')
data = data.drop(data.columns[0], axis=1)
data = data.iloc[8:]
data.columns = ["Class_Title","Specific_Thing","Class_Num","thing","Time","Day","code","Prof"]
#drop rows that do not have a value in time and class title or specific thing
mask = data["Class_Title"].isna() & data["thing"].isna()
data = data.drop(columns=["Specific_Thing"])
data = data.drop(columns=["code"])


# Drop the rows that match the condition
data = data[~mask].reset_index(drop=True)

# print(data.head(15))
# filtered_data = data[data["Class_Title"] == "HHC-H 101  EDUCATION AND ITS AIMS (1.5 CR)"]

# print(filtered_data.head())
import pandas as pd
import re

# Make sure these are your column names
data.columns = ["Class_Title", "Class_Num", "thing", "Time", "Day", "Prof"]

clean_rows = []
current_course = None

def is_course_title(cell):
    # Checks for pattern like: "XXX-XXX COURSE NAME (3 CR)"
    return isinstance(cell, str) and re.search(r"[A-Z]{3}-[A-Z]\s+\d+\s+.+\(\d+(\.\d+)? CR\)", cell)

i = 0
while i < len(data):
    row = data.iloc[i]
    title_cell = row["Class_Title"]

    if is_course_title(title_cell):
        # Extract course name and credits
        match = re.match(r"([A-Z]{3}-[A-Z]\s+\d+\s+.+?)\s+\(([\d\.]+)\s+CR\)", title_cell)
        if match:
            course_name = match.group(1).strip()
            credits = float(match.group(2))
            current_course = {
                "Class_Title": course_name,
                "Credits": credits,
                "Notes": [],
                "Times": []
            }
            clean_rows.append(current_course)

    elif current_course:
        # If there's a 'thing' (notes), store it
        if isinstance(row["thing"], str) and not pd.isna(row["thing"]):
            current_course["Notes"].append(row["thing"].strip())

        # If there's timing info, store it
        if pd.notna(row["Class_Num"]) and pd.notna(row["Time"]):
            time_info = f'{row["Class_Num"]} {row["Time"]} {row["Day"]} {row["Prof"]}'
            current_course["Times"].append(time_info.strip())

    i += 1

# Build final DataFrame
final_data = pd.DataFrame([
    {
        "Class_Title": row["Class_Title"],
        "Credits": row["Credits"],
        # "Notes": " ".join(row["Notes"]),
        "Times": ",".join(row["Times"]),
        "Semester": 1 #1 for Fall, 0 for Spring
    }
    for row in clean_rows
])


# Assuming your cleaned DataFrame is called final_data
# print(final_data.head())

# Export the DataFrame to an Excel file
final_data.to_excel("fall_times.xlsx", index=False)

