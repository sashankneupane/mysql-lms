import mysql.connector
import getpass

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
  password=password
)

# Create a cursor object
mycursor = mydb.cursor()

# Create brightspace database
mycursor.execute("CREATE DATABASE IF NOT EXISTS lms")

# Commit the changes
mydb.commit()

# Close the cursor and connection
mycursor.close()
mydb.close()

print("Database created successfully!")