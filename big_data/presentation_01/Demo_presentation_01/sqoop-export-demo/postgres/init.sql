CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    major VARCHAR(100),
    gpa DECIMAL(3,2)
);

INSERT INTO students VALUES
(1, 'Nguyen Van A', 'Information Technology', 3.40),
(2, 'Tran Thi B', 'Data Science', 3.70),
(3, 'Le Van C', 'Computer Science', 3.20)
ON CONFLICT (id) DO NOTHING;

DROP TABLE IF EXISTS students_export;

CREATE TABLE students_export (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    major VARCHAR(100),
    gpa DECIMAL(3,2)
);