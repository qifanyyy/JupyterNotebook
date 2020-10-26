# Create connection to database
import sqlite3
conn = sqlite3.connect("courses.db")
c = conn.cursor()

# Drop old coursedata table
c.execute("drop table if exists coursedata")

# Create new coursedata table
statement = "create table if not exists coursedata ({}, {}, {}, {}, {})"
statement = statement.format(
	"course_id text primary key",
	"course_title text", 
	"course_level integer", 
	"course_category integer", # How STEMmy the course is
	"course_enrollment integer", 
)
c.execute(statement)

# Close connection to database after saving changes
conn.commit()
conn.close()
