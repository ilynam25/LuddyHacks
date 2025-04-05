#test
print("Hello World")

#chat prompt, get the interests, previous classes, which semester, which majors

#chat answer

#use roadmap to know what we need to fulfill

import sqlite3
from datetime import datetime


# conn = sqlite3.connect("university.db")
# cursor = conn.cursor()

# cursor.executescript("""
# CREATE TABLE courses (
#     course_id TEXT PRIMARY KEY,
#     title TEXT,
#     description TEXT,
#     credits INTEGER,
#     term TEXT,
#     days TEXT,
#     start_time TEXT,
#     end_time TEXT
# );

# CREATE TABLE prerequisites (
#     course_id TEXT,
#     prerequisite_id TEXT
# );
# """)

# conn.commit()
# conn.close()
# print("✅ Schema created!")


# Connect to SQLite (creates file if it doesn't exist)
conn = sqlite3.connect("university.db")
cursor = conn.cursor()

# --------------------------
# Student Input
# --------------------------
student_input = {
    "career_goal": "Data Scientist",
    "preferred_subjects": ["Math", "Computer Science"],
    "completed_courses": ["CS101", "MATH101"],
    "available_schedule": {
        "Mon": [(8, 12), (14, 17)],
        "Wed": [(8, 12), (14, 17)]
    },
    "credit_range": (12, 18),
    "term": "Fall 2025"
}

# Static mapping: career goals → recommended courses
career_course_map = {
    "Data Scientist": ["CS102", "STAT201", "ML301", "DS401"]
}

# --------------------------
# Helper Functions
# --------------------------

def get_courses(term):
    cursor.execute("""
        SELECT course_id, title, description, credits, days, start_time, end_time 
        FROM courses 
        WHERE term = ?
    """, (term,))
    return cursor.fetchall()

def get_prerequisites(course_id):
    cursor.execute("""
        SELECT prerequisite_id FROM prerequisites WHERE course_id = ?
    """, (course_id,))
    return [row[0] for row in cursor.fetchall()]

def has_prerequisites(course_id, completed):
    prereqs = get_prerequisites(course_id)
    return all(pr in completed for pr in prereqs)

def fits_schedule(days_str, start_str, end_str, availability):
    days = days_str.split(",")  # from string like "Mon,Wed"
    start_hour = int(start_str.split(":")[0])
    end_hour = int(end_str.split(":")[0])
    for day in days:
        blocks = availability.get(day, [])
        if not any(start_hour >= block[0] and end_hour <= block[1] for block in blocks):
            return False
    return True

# --------------------------
# Main Filtering Logic
# --------------------------

eligible_courses = []
target_courses = career_course_map.get(student_input["career_goal"], [])
available_courses = get_courses(student_input["term"])

for course in available_courses:
    course_id, title, desc, credits, days, start, end = course
    if course_id not in target_courses:
        continue
    if not has_prerequisites(course_id, student_input["completed_courses"]):
        continue
    if not fits_schedule(days, start, end, student_input["available_schedule"]):
        continue
    eligible_courses.append({
        "course_id": course_id,
        "title": title,
        "credits": credits,
        "days": days,
        "start": start,
        "end": end
    })

# --------------------------
# Greedy Selection Based on Credits
# --------------------------

selected = []
total_credits = 0
min_cred, max_cred = student_input["credit_range"]

for course in eligible_courses:
    if total_credits + course["credits"] <= max_cred:
        selected.append(course)
        total_credits += course["credits"]

if total_credits < min_cred:
    print("⚠️ Could not meet minimum credit load.")
else:
    print(f"✅ Selected Courses (Total Credits: {total_credits}):")
    for course in selected:
        print(f"- {course['course_id']}: {course['title']} ({course['credits']} credits)")
