import sqlite3
import json

# Connect to database
conn = sqlite3.connect("courses.db")
c = conn.cursor()

# Open data file
f = open("courses.json")
data = json.load(f)

# Prepare useful constants
STEM = ["MAT", "PHY", "MOL", "EEB", "CBE", "ELE", "COS", "CHM", "MAE", "AST", "CEE", "ORF", "SML"] 
HUM = ["POR", "LAT", "CLA", "HUM", "ENG", "HIS", "PHI", "MUS", "SLA", "COM", "AAS", "SPA", "PER"]

# Process JSON to add a course to coursedata table
def insert_course(course):
    if course["courseid"] in ids:
        return # don't duplicate courses, violating primary key constraint
    statement = "insert into coursedata values ('{}', '{}', {}, {}, {})"
    statement = statement.format(
        course["courseid"],
        get_course_title(course), 
        get_course_level(course), 
        get_course_category(course), # course STEM-ness, currently sketchy
        get_course_enrollment(course) 
    )
    c.execute(statement)
    ids.append(course["courseid"]) # add to list of "visited" courseids

# Extract the course title (currently hacky)
def get_course_title(course):
    return ["title"].replace("'", ""),

# Extract the course level
def get_course_level(course):
    if course.get("listings"):
        return int(course.get("listings")[0]["number"])
    else:
        return -1 # missing data

# Extract the course STEM-ness
def get_course_category(course):
    if course.get("listings"):
        if course.get("listings")[0]["dept"] in STEM:
            return 30 # very STEM
        elif course.get("listings")[0]["dept"] in HUM:
            return 10 # very non-STEM
        else:
            return 20 # in between: social sciences and other
    else:
        return -1 # missing data

# Extract the enrollment
def get_course_enrollment(course):
    if course.get("classes"):
        return int(course["classes"][0]["enroll"])
    else:
        return -1 # missing data

# Initialize list of "visited" courseids
c.execute("select course_id from coursedata")
ids = [row[0] for row in c.fetchall()]

# Process courses.json and use it to fill courses.db
for course in data:
    insert_course(course)

# Close database connection
conn.commit()
conn.close()
