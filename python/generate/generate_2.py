import csv
import json
import random
import mysql.connector

# connect to database
mydb = mysql.connector.connect(
    host="localhost",
    username = "root",
    password = "password",
    database = "lms"
)

# create a cursor
mycursor = mydb.cursor()

# ----------------------------------------------------------------------------------------

# create course data, read from courses.json
raw_course_data = None
with open("./data/courses.json", mode="r") as file:
    raw_course_data = json.load(file)

# open courses.csv
coursefile = open("./data/courses.csv", mode="w", newline="")
coursewriter = csv.DictWriter(coursefile, fieldnames=["course_id", "course_code", "course_name", "professor_id", "dept_id", "credit_hours", "course_description"])

# write the headers
coursewriter.writeheader()

# write the data
course_count = 0

for i, courses in enumerate(raw_course_data):

    courses = raw_course_data[courses]

    # get professors from the same department
    query = f'SELECT p.user_id FROM professors AS p WHERE p.dept_id = {i}'

    # get the professors with pandas
    mycursor.execute(query)

    # fetch professor ids
    professor_ids = [str(row[0]) for row in mycursor.fetchall()]


    for course in courses:

        # get a random professor id
        professor_id = random.choice(professor_ids)


        coursewriter.writerow({
            "course_id": str(course_count),
            "course_code": course["course_code"],
            "course_name": course["course_name"],
            "professor_id": professor_id,
            "dept_id": i,
            "credit_hours": str(course["credits"]),
            "course_description": course["description"]
        })

        course_count += 1

# close the file
coursefile.close()