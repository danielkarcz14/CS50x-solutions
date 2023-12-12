DROP TABLE students;
DROP TABLE houses;
DROP TABLE assigments;

CREATE TABLE students (
    id INTEGER,
    student_name TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE houses (
    id INTEGER AUTO,
    house TEXT NOT NULL,
    head TEXT,
    PRIMARY KEY(id)
);

CREATE TABLE assigments (
    student_id INT NOT NULL,
    house_id INT NOT NULL,
    name TEXT NOT NULL,
    subject TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (house_id) REFERENCES houses(id)
)
