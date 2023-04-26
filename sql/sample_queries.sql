SELECT u.firstname, u.lastname, u.email
FROM users u
WHERE u.user_id NOT IN (
    SELECT s.user_id FROM students s
);

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

SELECT c.course_code AS `Course Code`, c.course_name AS `Course Name`
FROM courses c
WHERE c.professor_id IN (
    SELECT u.user_id
    FROM professors p
    JOIN users u 
    ON u.user_id = p.user_id
    WHERE u.lastname = 'Smith'
);

SELECT c.course_name AS `Course Name`, COUNT(e.student_id) AS `Enrollments`
FROM courses c
JOIN enrollments e ON e.course_id = c.course_id
GROUP BY c.course_id;

SELECT u.firstname, u.lastname, u.email
FROM students s
JOIN users u ON u.user_id = s.user_id
JOIN enrollments e ON e.student_id = s.user_id
JOIN courses c ON c.course_id = e.course_id
WHERE c.course_name = 'Database Systems';

SELECT u.firstname, u.lastname, AVG(g.grade) AS avg_grade
FROM students s
JOIN users u ON u.user_id = s.user_id
JOIN grades g ON g.student_id = s.user_id
GROUP BY s.user_id;

SELECT DISTINCT u.firstname, u.lastname, u.email
FROM students s
JOIN users u ON u.user_id = s.user_id
JOIN grades g ON g.student_id = s.user_id
WHERE g.grade < 70;

SELECT m.major_name, COUNT(s.user_id) AS num_students
FROM majors m
JOIN students s ON s.major_id = m.major_id
GROUP BY m.major_id;

SELECT course_code, course_name
FROM courses
WHERE course_id IN (
    SELECT course_id FROM enrollments
    GROUP BY course_id
    HAVING COUNT(student_id) >= 3
);

SELECT firstname, lastname, email
FROM users
WHERE user_id IN (
    SELECT user_id FROM admins
    UNION
    SELECT user_id FROM professors
);