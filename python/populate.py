# this file is used to populate the database with data from csv files
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

# populate users table
with open("./data/users.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        query = f'INSERT INTO users (user_id, firstname, lastname, username, password, email)\nVALUES ("{row["user_id"]}", "{row["firstname"]}", "{row["lastname"]}", "{row["username"]}", "{row["password"]}", "{row["email"]}");'
        mycursor.execute(query)

# populate departments table
with open("./data/departments.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        query = f'INSERT INTO departments (dept_id, dept_name)\nVALUES ("{row["dept_id"]}", "{row["dept_name"]}");'
        mycursor.execute(query)


# populate majors table
with open("./data/majors.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        query = f'INSERT INTO majors (major_id, dept_id, major_name)\nVALUES ("{row["major_id"]}", "{row["dept_id"]}", "{row["major_name"]}");'
        mycursor.execute(query)


# populate students table
with open("./data/students.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        query = f'INSERT INTO students (user_id, major_id)\nVALUES ("{row["user_id"]}", "{row["major_id"]}");'
        mycursor.execute(query)


# populate professors table
with open("./data/professors.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        query = f'INSERT INTO professors (user_id, dept_id)\nVALUES ("{row["user_id"]}", "{row["dept_id"]}");'
        mycursor.execute(query)


# populate admins table
with open("./data/admins.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        query = f'INSERT INTO admins (user_id)\nVALUES ("{row["user_id"]}");'
        mycursor.execute(query)


# populate courses table
with open("./data/courses.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        query = f'INSERT INTO courses (course_id, course_code, course_name, professor_id, dept_id, credit_hours, course_description)\nVALUES ("{row["course_id"]}", "{row["course_code"]}", "{row["course_name"]}"  ,"{row["professor_id"]}", "{row["dept_id"]}", "{row["credit_hours"]}", "{row["course_description"]}");'
        mycursor.execute(query)

mydb.commit()