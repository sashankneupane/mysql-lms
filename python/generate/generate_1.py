# use faker to create user data for the database
import csv
from faker import Faker
import random
import json


# Create a Faker object
fake = Faker()


# ----------------------------------------------------------------------------------------
# get departments and major data from json file

# get raw data
raw_dept_data = None
with open("./data/departments_and_majors.json", mode="r") as file:
    raw_dept_data = json.load(file)

# open departments.csv and majors.csv
departmentfile = open("./data/departments.csv", mode="w", newline="")
majorfile = open("./data/majors.csv", mode="w", newline="")

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



# ----------------------------------------------------------------------------------------
# Create a list of roles
ratio = [1, 3, 40] # admin:professor:student (ratio)
roles = ["admin"] * ratio[0] + ["professor"] * ratio[1] + ["student"] * ratio[2]

# create a username based on the first and last name
def createusername(firstname, lastname):
    # introduce some randomness to the username
    if random.randint(0, 1) == 0:
        return firstname.lower() + lastname.lower() + str(random.randint(0, 1000))
    else:
        return firstname.lower() + "." + lastname.lower()


# create user data
with open("./data/users.csv", mode="w", newline="") as file:
    
    writer = csv.DictWriter(file, fieldnames=["user_id", "firstname", "lastname", "username", "password", "email"])
    writer.writeheader()

    # open students.csv, professors.csv, and admins.csv
    studentfile = open("./data/students.csv", mode="w", newline="")
    professorfile = open("./data/professors.csv", mode="w", newline="")
    adminfile = open("./data/admins.csv", mode="w", newline="")

    # create a writer for each file
    studentwriter = csv.DictWriter(studentfile, fieldnames=["user_id", "major_id"])
    professorwriter = csv.DictWriter(professorfile, fieldnames=["user_id", "dept_id"])
    adminwriter = csv.DictWriter(adminfile, fieldnames=["user_id"])

    # write the headers
    studentwriter.writeheader()
    professorwriter.writeheader()
    adminwriter.writeheader()

    for i in range(5000):

        firstname = fake.first_name()
        lastname = fake.last_name()
        username = createusername(firstname, lastname)
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
                "dept_id": str(random.randint(0, len(raw_dept_data) - 1))
            })
        else:
            adminwriter.writerow({
                "user_id": str(i)
            })

    # close the files
    studentfile.close()
    professorfile.close()
    adminfile.close()