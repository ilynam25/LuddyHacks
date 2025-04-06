import pandas as pd
import re
from datatesting import output
import fred_labeling_classes as fred
import random as rand

# Load the CSV file
df = pd.read_csv('combined_output.csv')

# Assume the times are in the third column (index 3)
time_column = df.columns[3]

# Function to extract the full time range (start-end) using regex
def extract_times(text):
    text = str(text).strip()  # Remove leading/trailing spaces
    # Match the full time range like 09:35A-10:50A
    time_ranges = re.findall(r'\b\d{2}:\d{2}[APap]?-?\d{2}:\d{2}[APap]?\b', text)
    return time_ranges

# Apply the function to the time column
df['Extracted Times'] = df[time_column].apply(extract_times)

# Function to get times for a specific course ID
def get_times(course_id):
    # Clean course_id and dataset values (remove spaces and normalize dashes)
    course_id_clean = course_id.strip().replace('–', '-')
    
    # Filter the rows where the course_id matches and return the extracted times
    times = df.loc[df[df.columns[0]].str.strip().str.replace('–', '-') == course_id_clean, 'Extracted Times']
    
    return times.tolist()

# Get the course list
terms = [0,1,2,3,4,5,6,7]
clst = output(rand.choice(terms))

# Interests and sample generation
interests = ['Nutrition', 'South America', 'Pop Culture', 'Legal Issues', 'Teaching', 'Journalism', 'Nutrition', 'Sustainability',
                'Finance', 'Nature', 'Conflict Resolution', 'Video Games', 'Math', 'Human Behavior', 'Literature', 'Crafts',
                'Technology', 'Movies', 'Nature', 'Journalism\n', 'Fitness', 'Forensics', 'Central America', 'Language', 
                'Science', 'Marketing', 'Asia', 'Fashion', 'Business', 'Music', 'Philosophy', 'History', 'Internet', 
                'Children', 'Travel', 'Media', 'Photography', 'Design', 'Environment', 'Food', 'Music', 'Security', 
                'Video Games', 'Religion', 'Sports', 'Healthcare', 'Data Analysis', 'Helping People', 'Performance', 
                'Finance', 'Legal Issues', 'North America', 'Animals', 'Sustainability', 'Management', 'Programming', 
                'Art', 'Design', 'Writing', 'South America', 'Leadership', 'Culture',
                'Fashion', 'Photography', 'Counseling', 'Media',
                'Rehabilitation', 'Performance', 'News', 'Human Rights', 'Philosophy', 
                'Management', 'Pop Culture', 'Math', 'Communication', 'Language', 'Public Relations', 
                'News', 'Teaching', 'Science', 'Art', 'Religion', 'Programming', 'Marketing', 'Europe', 
                'International', 'History', 'Rehabilitation', 'Movies', 'Technology', 'Government', 
                'Leadership', 'Africa', 'Human Behavior', 'Gender and LGBTQ+', 'Human Rights', 'International', 
                'Helping People', 'Europe', 'Security', 'Literature', 'North America', 'Africa']

sample_interests = [rand.choice(interests) for _ in range(4)]

regularclasses=[]
geneds=[]
p = 'AHSHWCNSWLECNMMMIGEN'

for i in clst:
    if i == 'WLWC':
        clst[clst.index(i)]='WL'

for i in clst:
    if i in p:
        geneds.append(i)
    else:
        regularclasses.append(i)

genids=[]
for i in geneds:
    # print(i)
    d = fred.recommended_class(sample_interests, i)
    dax = d[1]
    print(dax)
    course_title = ' '.join(dax.split()[:2])
    genids.append(course_title)

final_course = regularclasses + genids
print(final_course)
# Function to get times for courses by semester (Fall: 1, Spring: 0)
def get_times_by_semester(course_ids, semester_value):
    filtered_df = df[df['Semester'] == semester_value]
    
    # Iterate through the course_ids list and print the corresponding times for the filtered dataframe
    for course_id in course_ids:
        course_times = get_times(course_id)
        
        # Remove duplicate times using set(), sort them, and ensure they're in correct order
        unique_times = sorted(list(set([time for sublist in course_times for time in sublist])), key=lambda x: (x[-1], x[:5]))
        
        if unique_times:
            print(f"Times for {course_id}: {unique_times}")
        else:
            print(f"No times found for {course_id}.")

# Example usage for Fall (semester = 1) and Spring (semester = 0)
semester_map = {}
for course_id in final_course:
    course_times = get_times(course_id)
    
    # Clean the times by removing duplicates, sorting them and storing
    unique_times = sorted(list(set([time for sublist in course_times for time in sublist])), key=lambda x: (x[-1], x[:5]))
    semester_map[course_id] = unique_times

print("\n=== Fall Semester Courses ===")
get_times_by_semester(final_course, 1)  # Semester 1 is for Fall

