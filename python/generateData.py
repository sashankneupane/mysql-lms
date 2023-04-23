# use faker to create user data for the database
import csv
from faker import Faker
import random
import json

# Create a Faker object
fake = Faker()

class generateData:

    def __init__(self, mycursor, rootfile = './data/'):
        self.root = rootfile
        self.cursor = mycursor

    def generate(self, string):
        eval(f'self.generate{string}()')

    # generates both departments and majors data
    def generateDepartments(self):
        
        # get raw data
        raw_dept_data = None
        with open(self.root + "json/departments_and_majors.json", mode="r") as file:
            raw_dept_data = json.load(file)

        # open departments.csv and majors.csv
        departmentfile = open(self.root + "departments.csv", mode="w", newline="")
        majorfile = open(self.root + "majors.csv", mode="w", newline="")

        # create a writer for each file
        departmentwriter = csv.DictWriter(departmentfile, fieldnames=["dept_id", "dept_name"])
        majorwriter = csv.DictWriter(majorfile, fieldnames=["major_id", "dept_id", "major_name"])

        # write the headers
        departmentwriter.writeheader()
        majorwriter.writeheader()


        # write the data
        major_count = 0
        for i, dept in enumerate(raw_dept_data):

            departmentwriter.writerow({
                "dept_id": str(i),
                "dept_name": dept
            })

            for major in raw_dept_data[dept]:
                majorwriter.writerow({
                    "major_id" : str(major_count),
                    "dept_id": str(i),
                    "major_name": major
                })
                major_count += 1

        # close the files
        departmentfile.close()
        majorfile.close()



    # create a username based on the first and last name
    def createusername(self, firstname, lastname):
        
        # introduce some randomness to the username
        if random.randint(0, 1) == 0:
            return firstname.lower() + lastname.lower() + str(random.randint(0, 1000))
        else:
            return firstname.lower() + "." + lastname.lower()

    # generates users data
    def generateUsers(self, number_of_users = 5000):
        # ----------------------------------------------------------------------------------------
        # Create a list of roles
        ratio = [1, 3, 40] # admin:professor:student (ratio)
        roles = ["admin"] * ratio[0] + ["professor"] * ratio[1] + ["student"] * ratio[2]

        # get number of departments
        self.cursor.execute("SELECT COUNT(*) FROM departments")
        dept_count = self.cursor.fetchone()[0]

        # get number of majors
        self.cursor.execute("SELECT COUNT(*) FROM majors")
        major_count = self.cursor.fetchone()[0]

        # create user data
        with open(self.root + "users.csv", mode="w", newline="") as file:
            
            writer = csv.DictWriter(file, fieldnames=["user_id", "firstname", "lastname", "username", "password", "email"])
            writer.writeheader()

            # open students.csv, professors.csv, and admins.csv
            studentfile = open(self.root + "students.csv", mode="w", newline="")
            professorfile = open(self.root + "professors.csv", mode="w", newline="")
            adminfile = open(self.root + "admins.csv", mode="w", newline="")

            # create a writer for each file
            studentwriter = csv.DictWriter(studentfile, fieldnames=["user_id", "major_id"])
            professorwriter = csv.DictWriter(professorfile, fieldnames=["user_id", "dept_id"])
            adminwriter = csv.DictWriter(adminfile, fieldnames=["user_id"])

            # write the headers
            studentwriter.writeheader()
            professorwriter.writeheader()
            adminwriter.writeheader()

            for i in range(number_of_users):

                firstname = fake.first_name()
                lastname = fake.last_name()
                username = self.createusername(firstname, lastname)
                writer.writerow({
                    "user_id": str(i),
                    "firstname": firstname,
                    "lastname": lastname,
                    "username": username,
                    "password": fake.password(),
                    "email": username+"@gmail.com",
                })

                # choose a random role
                role = random.choice(roles)
                if role == "student":
                    studentwriter.writerow({
                        "user_id": str(i),
                        "major_id": str(random.randint(0, major_count - 1))
                    })
                elif role == "professor":
                    professorwriter.writerow({
                        "user_id": str(i),
                        "dept_id": str(random.randint(0, dept_count - 1))
                    })
                else:
                    adminwriter.writerow({
                        "user_id": str(i)
                    })

            # close the files
            studentfile.close()
            professorfile.close()
            adminfile.close()


    # generate courses data
    def generateCourses(self):
        # create course data, read from courses.json
        raw_course_data = None
        with open(self.root + "json/courses.json", mode="r") as file:
            raw_course_data = json.load(file)

        # open courses.csv
        coursefile = open(self.root + "courses.csv", mode="w", newline="")
        coursewriter = csv.DictWriter(coursefile, fieldnames=["course_id", "course_code", "course_name", "professor_id", "dept_id", "credit_hours", "course_description"])

        # write the headers
        coursewriter.writeheader()

        # write the data
        course_count = 0

        for i, courses in enumerate(raw_course_data):

            courses = raw_course_data[courses]

            # get professors from the same department
            query = f'SELECT p.user_id FROM professors AS p WHERE p.dept_id = {i}'

            # get the professors with pandas
            self.cursor.execute(query)

            # fetch professor ids
            professor_ids = [str(row[0]) for row in self.cursor.fetchall()]

            for course in courses:

                # get a random professor id
                professor_id = random.choice(professor_ids)


                coursewriter.writerow({
                    "course_id": str(course_count),
                    "course_code": course["course_code"],
                    "course_name": course["course_name"],
                    "professor_id": professor_id,
                    "dept_id": i,
                    "credit_hours": str(course["credits"]),
                    "course_description": course["description"]
                })

                course_count += 1

        # close the file
        coursefile.close()

        

    def generateEnrollments(self):
        # create enrollment data
        status = ['enrolled'] * 85 + ['dropped'] * 15

        # open enrollments.csv
        enrollmentfile = open(self.root + "enrollments.csv", mode="w", newline="")
        enrollmentwriter = csv.DictWriter(enrollmentfile, fieldnames=["student_id", "course_id", "status"])

        # write header
        enrollmentwriter.writeheader()

        # read students.csv
        studentfile = open("./data/students.csv", mode="r")
        studentreader = csv.DictReader(studentfile)


        # loop through students to get user_id and major_id
        for student in studentreader:
            
            user_id, major_id = student["user_id"], student["major_id"]

            # get courses from students major
            query = f'SELECT course_id FROM courses JOIN majors ON courses.dept_id = majors.dept_id WHERE majors.major_id = {major_id}'
            self.cursor.execute(query)
            result = [x[0] for x in self.cursor.fetchall()]

            num_courses = min(len(result), random.randint(3,6))
            courses = random.sample(result, num_courses)

            # loop through courses
            for course in courses:
                enrollmentwriter.writerow({
                    "student_id": user_id,
                    "course_id": course,
                    "status": random.choice(status)
                })

        # close files
        enrollmentfile.close()
        studentfile.close()