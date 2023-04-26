SHOW TABLES;

SHOW COLUMNS FROM students;

SELECT * FROM admins;

SELECT u.firstname as `Professor`, d.dept_name as `Department`
FROM professors p 
JOIN users u
ON p.user_id = u.user_id
JOIN departments d
ON p.dept_id = d.dept_id
WHERE d.dept_name = 'Computer Science';