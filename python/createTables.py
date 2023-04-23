import yaml
import mysql.connector

# Read the config file
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Connect to the database
mydb = mysql.connector.connect(**config["lms"])

# Create a cursor object
mycursor = mydb.cursor()

# Create the tables in the database
create_users_table = '''
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);
'''
mycursor.execute(create_users_table)



create_departments_table = '''
CREATE TABLE IF NOT EXISTS departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(255) NOT NULL
);
'''
mycursor.execute(create_departments_table)



create_majors_table = '''
CREATE TABLE IF NOT EXISTS majors (
    major_id INT PRIMARY KEY,
    dept_id INT NOT NULL, 
    major_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
'''
mycursor.execute(create_majors_table)




create_students_table = '''
CREATE TABLE IF NOT EXISTS students (
    user_id INT PRIMARY KEY,
    major_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (major_id) REFERENCES majors(major_id)
);
'''
mycursor.execute(create_students_table)



create_professors_table = '''
CREATE TABLE IF NOT EXISTS professors (
    user_id INT PRIMARY KEY,
    dept_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);
'''
mycursor.execute(create_professors_table)



create_admins_table = '''
CREATE TABLE IF NOT EXISTS admins (
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
'''
mycursor.execute(create_admins_table)



create_courses_table = '''
CREATE TABLE IF NOT EXISTS courses (
    course_id INT PRIMARY KEY,
    course_code VARCHAR(255) NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    professor_id INT NOT NULL,
    dept_id INT NOT NULL,
    credit_hours INT NOT NULL,
    course_description TEXT,
    FOREIGN KEY (professor_id) REFERENCES professors(user_id),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);

'''
mycursor.execute(create_courses_table)



create_assignments_table = '''
CREATE TABLE IF NOT EXISTS assignments (
    assignment_id INT PRIMARY KEY,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    assignment_title VARCHAR(255),
    assignment_description TEXT,
    due_date DATETIME
);
'''
mycursor.execute(create_assignments_table)



create_enrollments_table = '''
CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    status ENUM('enrolled', 'dropped'),
    FOREIGN KEY (student_id) REFERENCES students(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
'''
mycursor.execute(create_enrollments_table)



create_grades_table = '''
CREATE TABLE IF NOT EXISTS grades (
    grade_id INT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    assignment_id INT NOT NULL,
    grade FLOAT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    FOREIGN KEY (assignment_id) REFERENCES assignments(assignment_id)
);
'''
mycursor.execute(create_grades_table)


# too complicated to include for now
# create_announcements_table = '''
# CREATE TABLE IF NOT EXISTS announcements (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     course_id INT NOT NULL,
#     title VARCHAR(255) NOT NULL,
#     description TEXT NOT NULL,
#     date DATETIME NOT NULL,
#     FOREIGN KEY (course_id) REFERENCES courses(id)
# );
# '''
# mycursor.execute(create_announcements_table)


# Commit the changes
mydb.commit()

# Close the cursor and connection
mycursor.close()
mydb.close()

print("Tables created successfully!")