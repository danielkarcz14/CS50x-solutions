from cs50 import SQL
import csv

db = SQL("sqlite:///roster.db")

with open("students.csv") as file:
    reader = csv.DictReader(file)
    i = 0
    for row in reader:
        db.execute("INSERT INTO students (id, student_name) VALUES (?, ?)", row['id'], row['student_name'])
        if not db.execute("SELECT house FROM houses WHERE house = ?", row['house']):
                i += 1
                db.execute("INSERT INTO houses (id, house, head) VALUES(?, ?, ?)", i, row['house'], row['head'])


