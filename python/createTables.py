import mysql.connector

# Get username and password from the user
# username = input("Enter your MySQL username: ")
# password = getpass.getpass("Enter your MySQL password: ")

# my username and password
username = 'root'
password = 'password'

# Create a connection to the MySQL server
mydb = mysql.connector.connect(
  host="localhost",
  user=username,
  password=password,
  database="lms"
)

# Create a cursor object
mycursor = mydb.cursor()



# Create the tables in the database
create_users_table = '''
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role ENUM('admin', 'professor', 'student') NOT NULL
);
'''
mycursor.execute(create_users_table)



create_majors_table = '''
CREATE TABLE IF NOT EXISTS majors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);
'''
mycursor.execute(create_majors_table)



create_departments_table = '''
CREATE TABLE IF NOT EXISTS departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);
'''
mycursor.execute(create_departments_table)



create_students_table = '''
CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    student_number VARCHAR(255) NOT NULL,
    major_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (major_id) REFERENCES majors(id)
);
'''
mycursor.execute(create_students_table)



create_professors_table = '''
CREATE TABLE IF NOT EXISTS professors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    professor_number VARCHAR(255) NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
'''
mycursor.execute(create_professors_table)



create_admins_table = '''
CREATE TABLE IF NOT EXISTS admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
'''
mycursor.execute(create_admins_table)



create_courses_table = '''
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    credit_hours INT NOT NULL,
    professor_id INT NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (professor_id) REFERENCES professors(id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
'''
mycursor.execute(create_courses_table)



create_assignments_table = '''
CREATE TABLE IF NOT EXISTS assignments (
    id INT PRIMARY KEY,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    title VARCHAR(255),
    description TEXT,
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
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
'''
mycursor.execute(create_enrollments_table)



create_grades_table = '''
CREATE TABLE IF NOT EXISTS grades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    assignment_id INT NOT NULL,
    grade FLOAT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (assignment_id) REFERENCES assignments(id)
);
'''
mycursor.execute(create_grades_table)



create_announcements_table = '''
CREATE TABLE IF NOT EXISTS announcements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);
'''
mycursor.execute(create_announcements_table)


# Commit the changes
mydb.commit()

# Close the cursor and connection
mycursor.close()
mydb.close()

print("Tables created successfully!")