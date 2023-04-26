SELECT u.firstname AS `First Name`, u.lastname AS `Last Name`, u.email AS `Email Address`
FROM users u
WHERE u.user_id NOT IN (
    SELECT s.user_id FROM students s
);

SELECT courses.course_name AS `Courses`
FROM ((users 
INNER JOIN students ON users.user_id=students.user_id) 
INNER JOIN enrollments ON students.user_id=enrollments.student_id) 
INNER JOIN courses ON enrollments.course_id=courses.course_id 
WHERE users.firstname="Tammy" AND users.lastname="Alexander";

SELECT c.course_name
FROM users u 
JOIN professors p ON u.user_id = p.user_id
JOIN courses c ON p.user_id = c.professor_id
WHERE u.firstname = "Ruben" AND u.lastname = "Burton";

SELECT d.dept_name
FROM departments d 
JOIN professors p ON d.dept_id = p.dept_id
JOIN users u ON u.user_id = p.user_id
WHERE u.firstname = "Ruben" AND u.lastname = "Burton";

SELECT course_code AS `Course Code`, course_name AS `Course` 
FROM departments d 
JOIN courses c ON d.dept_id = c.dept_id
WHERE d.dept_name = "Management";

SELECT u.firstname, u.lastname, u.email
FROM professors p
JOIN users u ON u.user_id = p.user_id
WHERE p.user_id NOT IN (
    SELECT c.professor_id FROM courses c
);

SELECT u.firstname AS `First Name`, u.lastname AS `Last Name`, COUNT(*) as `Enrollments`
FROM users u
JOIN students s ON u.user_id = s.user_id
JOIN enrollments e ON s.user_id = e.student_id
GROUP BY u.user_id
HAVING COUNT(*) >= 5;

SELECT u.firstname AS `First Name`, u.lastname AS `Last Name`, u.email AS `Email`
FROM professors p
JOIN users u ON u.user_id = p.user_id
JOIN departments d ON d.dept_id = p.dept_id
WHERE d.dept_name = 'Computer Science';

SELECT c.course_name AS `Course Name`, COUNT(e.student_id) AS `Enrollments`
FROM courses c
JOIN enrollments e ON e.course_id = c.course_id
GROUP BY c.course_id;


SELECT m.major_name AS `Major`, COUNT(s.user_id) AS `Number of Students`
FROM majors m
JOIN students s ON s.major_id = m.major_id
GROUP BY m.major_id
ORDER BY COUNT(s.user_id) DESC;

SELECT course_code AS `Course Code`, course_name AS `Course Name`
FROM courses
WHERE course_id IN (
    SELECT course_id FROM enrollments
    GROUP BY course_id
    HAVING COUNT(student_id) >= 50
);

SELECT u.user_id AS `ID`, u.firstname AS `First Name`, u.lastname AS `Last Name`
FROM users u
JOIN students s ON u.user_id = s.user_id
JOIN enrollments e ON e.student_id = s.user_id
JOIN courses c ON e.course_id = c.course_id
WHERE c.course_name = "'Number Theory'";

SELECT major_name AS `Major`, COUNT(major_name) AS `Number of students`
FROM  students NATURAL JOIN majors 
GROUP BY major_name 
HAVING COUNT(major_name) = (
   SELECT MAX(stud_num) 
   FROM  (SELECT COUNT(major_name) AS stud_num 
   FROM students NATURAL JOIN majors 
   GROUP BY major_name)  
AS stud);

SELECT dept_name AS `Department`, COUNT(dept_name) As `Number of Professors`
FROM professors 
NATURAL JOIN departments 
GROUP BY dept_name 
HAVING COUNT(dept_name)= (
    SELECT MAX(profnum) FROM (
        SELECT COUNT(dept_name) AS profnum 
        FROM professors NATURAL JOIN departments 
        GROUP BY dept_name) AS subquery
);

SELECT c.course_name AS `Course`, COUNT(c.course_name) AS `Number of Students` 
FROM enrollments e 
JOIN courses c ON e.course_id = c.course_id
GROUP BY c.course_name 
HAVING COUNT(c.course_name) = (
    SELECT MAX(stud_num) 
    FROM (SELECT COUNT(c1.course_name) AS stud_num 
          FROM enrollments e1 
          JOIN courses c1 ON e1.course_id = c1.course_id
          GROUP BY c1.course_name) as max_stud_num
);