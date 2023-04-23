-- ONLY CREATES TABLES AND DATABASE IF THEY DON'T EXIST

-- Create the database if it doesn't exist
CREATE 
DATABASE IF NOT EXISTS 
lms;

USE lms;

-- Create Users table
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);



-- Create Departments table
CREATE TABLE IF NOT EXISTS departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(255) NOT NULL
);



-- Create Majors table
CREATE TABLE IF NOT EXISTS majors (
    major_id INT PRIMARY KEY,
    dept_id INT NOT NULL, 
    major_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);


-- Create Students table
CREATE TABLE IF NOT EXISTS students (
    user_id INT PRIMARY KEY,
    major_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (major_id) REFERENCES majors(major_id)
);



-- Create Professors table
CREATE TABLE IF NOT EXISTS professors (
    user_id INT PRIMARY KEY,
    dept_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);



-- Create Admins table
CREATE TABLE IF NOT EXISTS admins (
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);



--  Create Courses table
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



-- Create Assignments table
CREATE TABLE IF NOT EXISTS assignments (
    assignment_id INT PRIMARY KEY,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    assignment_title VARCHAR(255),
    assignment_description TEXT,
    due_date DATETIME
);



-- Create Enrollments table
CREATE TABLE IF NOT EXISTS enrollments (
    enroll_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    status ENUM('enrolled', 'dropped'),
    FOREIGN KEY (student_id) REFERENCES students(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);



-- Create Grades table
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