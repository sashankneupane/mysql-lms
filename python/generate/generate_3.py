import csv
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

# create enrollment data
status = ['enrolled'] * 85 + ['dropped'] * 15

# open enrollments.csv
enrollmentfile = open("./data/enrollments.csv", mode="w", newline="")
enrollmentwriter = csv.DictWriter(enrollmentfile, fieldnames=["student_id", "course_id", "status"])

# write header
enrollmentwriter.writeheader()

# read students.csv
studentfile = open("./data/students.csv", mode="r")
studentreader = csv.DictReader(studentfile)


# loop through students to get user_id and major_id
for student in studentreader:
    
    user_id, major_id = student["user_id"], student["major_id"]

    # get courses from students major
    query = f'SELECT course_id FROM courses JOIN majors ON courses.dept_id = majors.dept_id WHERE majors.major_id = {major_id}'
    mycursor.execute(query)
    result = [x[0] for x in mycursor.fetchall()]

    num_courses = min(len(result), random.randint(3,6))
    courses = random.sample(result, num_courses)

    # loop through courses
    for course in courses:
        enrollmentwriter.writerow({
            "student_id": user_id,
            "course_id": course,
            "status": random.choice(status)
        })

# close files
enrollmentfile.close()
studentfile.close()

    
