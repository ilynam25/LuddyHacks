import pandas as pd
import random as rand
import re
import classes_by_interest as by_interest
import math

# Load datasets
df = pd.read_csv('combined_output.csv')

# Predefined time slots
predefined_times = [
    '08:00A-09:15A', 
    '09:35A-10:50A', 
    '02:20P-03:35P', 
    '03:55P-05:10P', 
    '05:30P-06:45P', 
    '11:10A-12:25P', 
    '12:45P-02:00P'
]

def get_times_by_semester(course_ids, semester_value):
    filtered_df = df[df['Semester'] == semester_value]
    for course_id in course_ids:
        course_times = get_times(course_id)
        unique_times = sorted(list(set([time for sublist in course_times for time in sublist])), key=lambda x: (x[-1], x[:5]))
        if unique_times:
            print(f"Times for {course_id}: {unique_times}")
        else:
            print(f"No times found for {course_id}.")

def get_times(course_id):
    time_column = df.columns[3]
    df['Extracted Times'] = df[time_column].apply(extract_times)
    course_id_clean = course_id.strip().replace('–', '-')
    times = df.loc[df[df.columns[0]].str.strip().str.replace('–', '-') == course_id_clean, 'Extracted Times']
    return times.tolist()

def extract_times(text):
    text = str(text).strip()
    time_ranges = re.findall(r'\b\d{2}:\d{2}[APap]?-?\d{2}:\d{2}[APap]?\b', text)
    return time_ranges

def output(term):
    df = pd.read_csv('coursemaphackathon.csv')
    dax = df.iloc[term, 3] 
    dax = dax.split('],\n')
    daxclean = []
    for i in range(len(dax)):
        if ']' in dax[i]:
            p = dax[i].replace(']', '').replace('\n', '').replace('[', '')
            daxclean.append(p)
        else:
            daxclean.append(dax[i][1:])
    return daxclean

def times_overlap(time1, time2):
    def parse_time(t):
        try:
            t = t.upper().replace('A', 'AM').replace('P', 'PM')
            return pd.to_datetime(t, format='%I:%M%p').time()
        except (ValueError, TypeError):
            return None
    
    start1, end1 = time1.split('-')
    start2, end2 = time2.split('-')
    start1 = parse_time(start1)
    end1 = parse_time(end1)
    start2 = parse_time(start2)
    end2 = parse_time(end2)

    if None in [start1, end1, start2, end2]:
        return False

    return (start1 < end2) and (start2 < end1)

def assign_predefined_times(course_ids, schedule):
    available_times = predefined_times[:]
    for course_id in course_ids:
        if schedule[course_id]['time'] == '-':
            selected_time = rand.choice(available_times)
            schedule[course_id]['time'] = selected_time
            available_times.remove(selected_time)
    return schedule

def get_average_gpa(course_id):
    course_id_clean = course_id.strip().replace('–', '-')
    # Try to find the GPA column (case insensitive)
    gpa_columns = [col for col in df.columns if 'gpa' in col.lower()]
    if not gpa_columns:
        return round(rand.uniform(2.8, 4.0), 2)  # Return random GPA if no GPA column exists
    
    gpa_column = gpa_columns[0]  # Use the first GPA column found
    try:
        gpa = df.loc[df[df.columns[0]].str.strip().str.replace('–', '-') == course_id_clean, gpa_column]
        if not gpa.empty:
            return math.round(float(gpa.values[0]),2)
    except:
        pass
    
    # Return random GPA between 2.0 and 4.0 if no GPA found or if there's an error
    return round(rand.uniform(2.8, 4.0), 2)

def build_schedule(course_ids, term):
    schedule = {}
    used_times = []
    for course_id in course_ids:
        course_times = get_times(course_id)
        if not course_times:
            course_times = ['-']
        flattened_times = [time for sublist in course_times for time in sublist]
        unique_times = sorted(list(set(flattened_times)), key=lambda x: (x[-1], x[:5]))
        
        # Initialize course entry in schedule
        schedule[course_id] = {'time': '-', 'Avg Gpa': get_average_gpa(course_id)}
        
        for time in unique_times:
            if time != '-' and not any(times_overlap(time, used_time) for used_time in used_times):
                used_times.append(time)
                schedule[course_id]['time'] = time
                break
        else:
            schedule[course_id]['time'] = '-'
            used_times.append('-')
    return schedule

def schedule_build(interests, term):
    clst = output(term)
    regularclasses = []
    geneds = []
    p = 'AHSHWCNSWLECNMMMIGEN'

    for i in clst:
        if i == 'WLWC':
            clst[clst.index(i)] = 'WL'

    for i in clst:
        if i in p:
            geneds.append(i)
        else:
            if ',' in i:
                req_choice=i
                req_choice=req_choice.split(',')
                regularclasses.append(rand.choice(req_choice))
            else:
                regularclasses.append(i)

    genids = []
    dic={}
    for i in geneds:
        d = by_interest.recommended_class(interests, i)
        dax = d[1]
        reasons=d[2]
        dic[dax]=reasons
        course_title = ' '.join(dax.split()[:2])
        genids.append(course_title)

    final_course = regularclasses + genids
    schedule = build_schedule(final_course, term)
    final_schedule = assign_predefined_times([course_id for course_id, details in schedule.items() if details['time'] == '-'], schedule)
    return final_schedule

# Example usage:
print(schedule_build(('Art','Music'), 2))