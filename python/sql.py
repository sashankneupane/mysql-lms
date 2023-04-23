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


# write users to users.sql
with open("./sql/users.sql", mode="w") as populatesql:
    # write users to populate sql file
    with open("./data/users.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            query = f'INSERT INTO users (user_id, firstname, lastname, username, password, email)\nVALUES ("{row["user_id"]}", "{row["firstname"]}", "{row["lastname"]}", "{row["username"]}", "{row["password"]}", "{row["email"]}");'
            populatesql.write(query + "\n\n")


# write departments to departments.sql
with open("./sql/departments.sql", mode="w") as populatesql:
    # write departments to populate sql file
    with open("./data/departments.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            query = f'INSERT INTO departments (dept_id, dept_name)\nVALUES ("{row["dept_id"]}", "{row["dept_name"]}");'
            populatesql.write(query + "\n\n")

# write majors to majors.sql
with open("./sql/majors.sql", mode="w") as populatesql:
    # write majors to populate sql file
    with open("./data/majors.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            query = f'INSERT INTO majors (major_id, dept_id, major_name)\nVALUES ("{row["major_id"]}", "{row["dept_id"]}", "{row["major_name"]}");'
            populatesql.write(query + "\n\n")

# write students to students.sql
with open("./sql/students.sql", mode="w") as populatesql:
    # write students to populate sql file
    with open("./data/students.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            query = f'INSERT INTO students (user_id, major_id)\nVALUES ("{row["user_id"]}", "{row["major_id"]}");'
            populatesql.write(query + "\n\n")


# write professors to professors.sql
with open("./sql/professors.sql", mode="w") as populatesql:
    # write professors to populate sql file
    with open("./data/professors.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            query = f'INSERT INTO professors (user_id, dept_id)\nVALUES ("{row["user_id"]}", "{row["dept_id"]}");'
            populatesql.write(query + "\n\n")


# write admins to admins.sql
with open("./sql/admins.sql", mode="w") as populatesql:
    # write admins to populate sql file
    with open("./data/admins.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            query = f'INSERT INTO admins (user_id)\nVALUES ("{row["user_id"]}");'
            populatesql.write(query + "\n\n")

# write courses to courses.sql
with open("./sql/courses.sql", mode="w") as populatesql:
    # write courses to populate sql file
    with open("./data/courses.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            query = f'INSERT INTO courses (course_id, course_code, course_name, professor_id, dept_id, credit_hours, course_description)\nVALUES ("{row["course_id"]}", "{row["course_code"]}", "{row["course_name"]}"  ,"{row["professor_id"]}", "{row["dept_id"]}", "{row["credit_hours"]}", "{row["course_description"]}");'
            populatesql.write(query + "\n\n")


# write course_enrollments to course_enrollments.sql
with open("./sql/enrollments.sql", mode="w") as populatesql:
    # write course_enrollments to populate sql file
    with open("./data/enrollments.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            query = f'INSERT INTO enrollments (student_id, course_id, status)\nVALUES ("{row["student_id"]}", "{row["course_id"]}", "{row["status"]}");'
            populatesql.write(query + "\n\n")

mydb.commit()