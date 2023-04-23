# this file is used to populate the database with data from csv files
import mysql.connector
import csv
import yaml

from generateData import generateData


# generate data
if '__main__' == __name__:

    # read config file
    with open("./config.yaml", mode="r") as file:
        config = yaml.safe_load(file)

    # connect to database
    mydb = mysql.connector.connect(**config["lms"])

    # create a cursor
    mycursor = mydb.cursor()

    # general function to populate a table
    def populateTable(query, file):
        filename = f'./data/{file}.csv'
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row_data in reader:
                mycursor.execute(query, row_data)
    
    generator = generateData(mycursor)

    # generates and populates departments and majors
    generator.generate("Departments")
    insertqueries = {
        "departments": 'INSERT INTO departments (dept_id, dept_name)\nVALUES (%(dept_id)s, %(dept_name)s);',
        "majors": 'INSERT INTO majors (major_id, dept_id, major_name)\nVALUES (%(major_id)s, %(dept_id)s, %(major_name)s);'
    }
    for file, query in insertqueries.items():
        populateTable(query, file)

    # generates and populates users, students, professors, and admins
    generator.generate("Users")
    insertqueries = {
        "users": 'INSERT INTO users (user_id, firstname, lastname, username, password, email)\nVALUES (%(user_id)s, %(firstname)s, %(lastname)s, %(username)s, %(password)s, %(email)s);',
        "students": 'INSERT INTO students (user_id, major_id)\nVALUES (%(user_id)s, %(major_id)s);',
        "professors": 'INSERT INTO professors (user_id, dept_id)\nVALUES (%(user_id)s, %(dept_id)s);',
        "admins": 'INSERT INTO admins (user_id)\nVALUES (%(user_id)s);'
    }
    for file, query in insertqueries.items():
        populateTable(query, file)
    
    # generates and populates courses
    generator.generate("Courses")
    insertquery = 'INSERT INTO courses (course_id, course_code, course_name, professor_id, dept_id, credit_hours, course_description)\nVALUES (%(course_id)s, %(course_code)s, %(course_name)s, %(professor_id)s, %(dept_id)s, %(credit_hours)s, %(course_description)s);'
    populateTable(insertquery, "courses")

    # generates and populates enrollments
    generator.generate("Enrollments")
    insertquery = 'INSERT INTO enrollments (student_id, course_id)\nVALUES (%(student_id)s, %(course_id)s);'
    populateTable(insertquery, "enrollments")

    mydb.commit()