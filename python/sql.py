# this file writes sql files in ./sql/ directory that can be used to populate the database
import mysql.connector
import csv
import yaml

# read config file
with open("./config.yaml", mode="r") as file:
    config = yaml.safe_load(file)

# connect to database
mydb = mysql.connector.connect(**config["lms"])

# create a cursor
mycursor = mydb.cursor()

def writeQueries(file, query):
    with open(f"./sql/{file}.sql", mode="w") as populatesql:
        with open(f"./data/{file}.csv", mode="r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row_data in reader:
                formattted_query = query % row_data
                populatesql.write(formattted_query + "\n\n")


toWrite = {
    "departments": 'INSERT INTO departments (dept_id, dept_name)\nVALUES (%(dept_id)s, "%(dept_name)s");',
    "majors": 'INSERT INTO majors (major_id, dept_id, major_name)\nVALUES (%(major_id)s, %(dept_id)s, "%(major_name)s");',
    "users": 'INSERT INTO users (user_id, firstname, lastname, username, password, email)\nVALUES (%(user_id)s, "%(firstname)s", "%(lastname)s", "%(username)s", "%(password)s", "%(email)s");',
    "students": 'INSERT INTO students (user_id, major_id)\nVALUES (%(user_id)s, %(major_id)s);',
    "professors": 'INSERT INTO professors (user_id, dept_id)\nVALUES (%(user_id)s, %(dept_id)s);',
    "admins": 'INSERT INTO admins (user_id)\nVALUES (%(user_id)s);',
    "courses": 'INSERT INTO courses (course_id, course_code, course_name, professor_id, dept_id, credit_hours, course_description)\nVALUES (%(course_id)s, "%(course_code)s", "%(course_name)s", %(professor_id)s, %(dept_id)s, %(credit_hours)s, "%(course_description)s");',
    "enrollments": 'INSERT INTO enrollments (student_id, course_id)\nVALUES (%(student_id)s, %(course_id)s);'
}

for file, query in toWrite.items():
    writeQueries(file, query)

mydb.commit()