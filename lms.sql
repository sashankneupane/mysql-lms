-- Create the database if it doesn't exist
CREATE 
DATABASE IF NOT EXISTS 
lms;

USE lms;

-- Create the tables in the database
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    role ENUM('admin', 'professor', 'student') NOT NULL
);



CREATE TABLE IF NOT EXISTS majors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    student_number VARCHAR(255) NOT NULL,
    major_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (major_id) REFERENCES majors(id)
);


CREATE TABLE IF NOT EXISTS professors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    professor_number VARCHAR(255) NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);


CREATE TABLE IF NOT EXISTS admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


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


CREATE TABLE IF NOT EXISTS assignments (
    id INT PRIMARY KEY,
    course_id INT,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    title VARCHAR(255),
    description TEXT,
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
    id INT PRIMARY KEY AUTO_INCREMENT,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    assignment_id INT NOT NULL,
    grade FLOAT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (assignment_id) REFERENCES assignments(id)
);


CREATE TABLE IF NOT EXISTS announcements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    date DATETIME NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);