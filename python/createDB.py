import yaml
import mysql.connector

# Read the config file
with open("config.yaml", "r") as file:
  config = yaml.safe_load(file)

# Connect to the database
mydb = mysql.connector.connect(**config["mysql"])

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