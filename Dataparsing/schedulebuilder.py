import pandas as pd
from timetest import get_times, output  # Assuming timetest is in the same directory
import random as rand
import fred_labeling_classes as fred

# Load your CSV file in the same way
df = pd.read_csv('combined_output.csv')

# List of predefined time slots
predefined_times = [
    '08:00A-09:15A', 
    '09:35A-10:50A', 
    '02:20P-03:35P', 
    '03:55P-05:10P', 
    '05:30P-06:45P', 
    '11:10A-12:25P', 
    '12:45P-02:00P'
]

# Function to check if two time slots overlap
def times_overlap(time1, time2):
    # Fix AM/PM format and parse the start and end times
    def parse_time(t):
        # If the time is invalid or NaT, return None or a default value
        try:
            t = t.upper().replace('A', 'AM').replace('P', 'PM')  # Fix AM/PM notation
            return pd.to_datetime(t, format='%I:%M%p').time()
        except (ValueError, TypeError):
            return None  # Return None for invalid times
    
    start1, end1 = time1.split('-')
    start2, end2 = time2.split('-')

    start1 = parse_time(start1)
    end1 = parse_time(end1)
    start2 = parse_time(start2)
    end2 = parse_time(end2)

    # If any of the times are invalid (None), return False to avoid comparison errors
    if None in [start1, end1, start2, end2]:
        return False
    
    # Check for overlap: If start or end time of one course falls within the other
    return (start1 < end2) and (start2 < end1)

# Function to assign predefined times to courses without times
def assign_predefined_times(course_ids, schedule):
    available_times = predefined_times[:]
    
    for course_id in course_ids:
        if schedule[course_id] == '-':
            # Assign a random time slot from the predefined times
            selected_time = rand.choice(available_times)
            schedule[course_id] = selected_time
            available_times.remove(selected_time)  # Remove the selected time to avoid duplicates
    
    return schedule

# Function to build the schedule
def build_schedule(course_ids):
    schedule = {}
    used_times = []  # List to track used times and prevent overlap
    
    for course_id in course_ids:
        course_times = get_times(course_id)
        
        # If there are no times, assign a fake time
        if not course_times:
            course_times = ['-']
        
        # Flatten the list of times and remove duplicates
        flattened_times = [time for sublist in course_times for time in sublist]
        unique_times = sorted(list(set(flattened_times)), key=lambda x: (x[-1], x[:5]))
        
        # Check for overlapping and find a non-overlapping time
        for time in unique_times:
            if time != '-' and not any(times_overlap(time, used_time) for used_time in used_times):
                used_times.append(time)
                schedule[course_id] = time
                break
        else:
            # If no valid time found, assign a fake time
            schedule[course_id] = '-'
            used_times.append('-')
    
    return schedule

# Generate the course list (you may need to adjust how you get the final_course)
terms = [0, 1, 2, 3, 4, 5, 6, 7]
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
clst = output(rand.choice(terms))
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

# You can add more filtering logic here to generate the final list of courses
# For simplicity, using the original clst as the course list
final_course = regularclasses + genids

# Build the initial schedule
schedule = build_schedule(final_course)

# Assign predefined times to the courses that still have no assigned times ('-')
final_schedule = assign_predefined_times([course_id for course_id, time in schedule.items() if time == '-'], schedule)

# Print the final schedule
print('----------------------------------------')
print('----------------------------------------')
print('----------------------------------------')
print(final_schedule)
print('----------------------------------------')
print('----------------------------------------')
print('----------------------------------------')