CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY, name VARCHAR(100), major VARCHAR(100), gpa DECIMAL(3,2)
);
INSERT INTO students VALUES 
(1, 'Nguyen Van A', 'Information Technology', 3.40),
(2, 'Tran Thi B', 'Data Science', 3.70),
(3, 'Le Van C', 'Computer Science', 3.20) ON CONFLICT (id) DO NOTHING;

DROP TABLE IF EXISTS students_export;
CREATE TABLE students_export (
    id INT PRIMARY KEY, name VARCHAR(100), major VARCHAR(100), gpa DECIMAL(3,2)
);

CREATE TABLE IF NOT EXISTS class(
    id INT PRIMARY KEY, class_name VARCHAR(50), room VARCHAR(20)
);
INSERT INTO class VALUES 
(1,'BigData01','A101'),(2,'BigData02','A102'),(3,'BigData03','B201') ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS teacher(
    id INT PRIMARY KEY, teacher_name VARCHAR(50), subject VARCHAR(50)
);
INSERT INTO teacher VALUES 
(1,'Nguyen Van A','Data Eng'),(2,'Tran Thi B','DB Sys'),(3,'Le Van C','Dist Sys') ON CONFLICT (id) DO NOTHING;