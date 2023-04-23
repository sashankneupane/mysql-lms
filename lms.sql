-- Create the database if it doesn't exist
CREATE 
DATABASE IF NOT EXISTS 
lms;

USE lms;

-- Create the tables in the database
CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);



CREATE TABLE IF NOT EXISTS departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(255) NOT NULL
);



CREATE TABLE IF NOT EXISTS majors (
    major_id INT PRIMARY KEY,
    dept_id INT NOT NULL, 
    major_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);



CREATE TABLE IF NOT EXISTS students (
    user_id INT PRIMARY KEY,
    major_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (major_id) REFERENCES majors(major_id)
);


CREATE TABLE IF NOT EXISTS professors (
    user_id INT PRIMARY KEY,
    dept_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
);



CREATE TABLE IF NOT EXISTS admins (
    user_id INT PRIMARY KEY,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);



CREATE TABLE IF NOT EXISTS courses (
    course_id INT PRIMARY KEY,
    code VARCHAR(255) NOT NULL,
    course_name VARCHAR(255) NOT NULL,
    course_description TEXT,
    credit_hours INT NOT NULL,
    professor_id INT NOT NULL,
    dept_id INT NOT NULL,
    FOREIGN KEY (professor_id) REFERENCES professors(user_id),
    FOREIGN KEY (dept_id) REFERENCES departments(id)
);


CREATE TABLE IF NOT EXISTS assignments (
    assignment_id INT PRIMARY KEY,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    assignment_title VARCHAR(255),
    assignment_description TEXT,
    due_date DATETIME
);


CREATE TABLE IF NOT EXISTS enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    status ENUM('enrolled', 'dropped'),
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);


CREATE TABLE IF NOT EXISTS grades (
    id INT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    assignment_id INT NOT NULL,
    grade FLOAT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (assignment_id) REFERENCES assignments(id)
);