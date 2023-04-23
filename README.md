# Learning Management System Database
By Sashank Neupane and Ayazhan Gabitskyzy

---
This is a MySQL database for learning management systems. It includes tables for `users`, `students`, `professors`, `admins`, `majors`, `departments`, `courses`, `enrollments`, `grades`, and `assignments`.

## About the Data

The files `generate_1.py`, `generate_2.py`, and `generate_3.py` are used to generate the data for this database. All the data is stored in the `./data` folder as csv files. 

- `users.csv` is generated using the `faker` library.
- `courses.json` and `departments_and_majors.json` is generated using ChatGPT.


If you want to generate data for yourself, you can run the `generate` python scripts in the `./python/generate` folder.
- `generate_1.py` file generates data for the `users`, `students`, `professors`, `admins`, `majors`, and `departments` tables. 
- `generate_2.py` file generates data for the `courses`, `enrollments`, `grades`, and `assignments` tables. 
- `generate_3.py` file generates data for the `enrollments`, `grades`, and `assignments` tables.

However, `generate_2.py` only works when the tables generated from `generate_1.py` are populated. Similarly, the `generate_3.py` file only works when the tables generated from `generate_1.py` and `generate_2.py` are populated. Therefore, you should run the `generate` python scripts in order while populating the tables.

## Requirements

To use this database, you'll only need `MySQL` installed on your computer. You can download it from [here](https://dev.mysql.com/downloads/mysql/).


## Installation

To install this database, follow these steps:
1. Clone/download this repository: `git clone https://github.com/sashankneupane7/mysql-lms.git`.
2. Navigate to the repository directory: `cd mysql-lms`.
3. Login to MySQL: `mysql -u <username> -p`.
4. Run the SQL file: `SOURCE ./sql/createFullDB.sql`. This will populate the database with the data from the csv files.
5. If you only want to create database and tables, run: `SOURCE ./sql/createDB.sql`.

## You can also run the python scripts to create the database and tables.

To install this database using python scripts, follow these steps:

1. Clone/download this repository: `git clone https://github.com/sashankneupane7/mysql-lms.git`.
2. Navigate to the repository directory: `cd mysql-lms`.
3. Update `username` and `password` in the `config.yaml` file.
3. Install the required packages: `pip3 install -r python/requirements.txt`
3. Run following commands:
```
python3 createDB.py
python3 createTables.py
python3 populateTables.py
```


## Usage

You can now use this database in your application by connecting to the `lms` database and querying the appropriate tables.


## Web app

We have also create Flask web app for this database. You can run a flask server by running the following command:
```
pip3 install -r python/requirements.txt
flask run
```
The web app is available at `http://127.0.0.1:5000`.

