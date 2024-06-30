create database Exam;
use Exam
create table student(
name varchar(30),
rollno int primary key,
semester int,
branch varchar(40),
DOB  date ,
passsword varchar(50),
venue varchar(40),
room int
)
create table teacher(
name  varchar(50),
passworrd varchar(20),
id int primary key
)
create table Examday(
examday date,
branch varchar(20),
papercode varchar(10) primary key,
paper_name varchar(40),
)
create table  attendance(
paper_code  varchar(10),
rollno int,
exam_date date,
attend varchar(10),
foreign key(rollno) references student(rollno),
foreign key(paper_code) references Examday(papercode)
)
create table teacher_duty(
id int ,
room_no int,
exam_date date,
department_name varchar(20),
foreign key(id) references teacher(id)
)
create table studentdetails(
rollno int ,
category varchar(30),
fname varchar(30),
Mname varchar(30),
Formno int,
enrollment varchar(10),
dept varchar(50),
Email varchar(30),
mob bigint,
foreign key(rollno) references student(rollno)
)
insert into teacher values ('Nagendar ',1002,'army');
DELETE FROM student WHERE rollno=9002;
select*from teacher_duty;
insert into teacher_duty values(1001,25,'2024-04-15','ECE Dept');
insert into teacher_duty values(1002,23,'2024-04-16','civil Dept');
SELECT room_no, exam_date, department_name FROM teacher_duty WHERE id=1002
select *from Examday
insert into Examday values('2024-04-15','ECC','EC-404','OS');
insert into Examday values('2024-04-15','ECE','EC-403','ACT');
insert into Examday values('2024-04-16','ECC','EC-401','VLSI');
insert into Examday values('2024-04-16','ECE','EC-402','DCS');
insert into Examday values('2024-04-17','ECC','EC-405','CCDN');
insert into Examday values('2024-04-18','ECC','EC-412','ACS');
insert into Examday values('2024-04-19','ECC','EC-413','MULTIMEDIA');


insert into student values('Abhishek choudhary',8002,8,'ECC','2002-10-02','abhishek')
insert into student values('Amit Dubey',8006,8,'ECC','2001-11-05','dubey')
insert into student values('Abhishek choudhary',8002,8,'ECC','2002-10-02','abhishek')
insert into student values('sidhharth ',9002,8,'ECE','2002-02-24','shidharth')
insert into student values('Bhanu Priya Dixit',8055,8,'ECC','2002-10-13','bhanu')
insert into student values('vidhi jain',9003,8,'ECE','2002-10-02','vidhi')
insert into student values('Chirag mangal',8011,8,'ECC','2003-11-07','chirag')

insert into attendance values('EC-401',8002,'2024-04-16','Pending')
insert into attendance values('EC-404',8002,'2024-04-15','Pending')
insert into attendance values('EC-405',8002,'2024-04-17','Pending')
insert into attendance values('EC-412',8002,'2024-04-18','Pending')
insert into attendance values('EC-413',8002,'2024-04-19','Pending')
insert into attendance values('EC-405',8006,'2024-04-17','Pending')
insert into attendance values('EC-412',8006,'2024-04-18','Pending')
insert into attendance values('EC-413',8006,'2024-04-19','Pending')
insert into attendance values('EC-405',8055,'2024-04-17','Pending')
insert into attendance values('EC-412',8055,'2024-04-18','Pending')
insert into attendance values('EC-413',8055,'2024-04-19','Pending')
insert into attendance values('EC-405',8011,'2024-04-17','Pending')
insert into attendance values('EC-412',8011,'2024-04-18','Pending')
insert into attendance values('EC-413',8011,'2024-04-19','Pending')
insert into attendance values('EC-401',8006,'2024-04-16','Pending')
insert into attendance values('EC-404',8006,'2024-04-15','Pending')
insert into attendance values('EC-401',8011,'2024-04-16','Pending')
insert into attendance values('EC-404',8011,'2024-04-15','Pending')
insert into attendance values('EC-401',8055,'2024-04-16','Pending')
insert into attendance values('EC-404',8055,'2024-04-15','Pending')
insert into attendance values('EC-402',9002,'2024-04-16','Pending')
insert into attendance values('EC-403',9002,'2024-04-15','Pending')
insert into attendance values('EC-402',9003,'2024-04-16','Pending')
insert into attendance values('EC-403',9003,'2024-04-15','Pending')

insert into studentdetails values(8006,'Regular','Munesh Kumar Dubey','Heera Sharma',345678,'J20U676878','ELECTRONICS AND COMMUNICATION ENGINEERING','manishamitdubey@gamil.com',7378244919);
insert into studentdetails values(8055,'Regular','Kanhaiya Lal Sharma','Tanu Sharma',345679,'J20U676890','ELECTRONICS AND COMMUNICATION ENGINEERING','bhanu10@gmail.com',9145860318);
insert into studentdetails values(8011,'Regular','Sunil Kumar Mangal','Anju Devi Mangal',345680,'J20U676895','ELECTRONICS AND COMMUNICATION ENGINEERING','mangalchirag@gamil.com',6377688671);
insert into studentdetails values(8002,'Regular','Jagdish Choudhary','Priti  Singh',345681,'J20U676876','ELECTRONICS AND COMMUNICATION ENGINEERING','leborn@gamil.com',8079045615);

SELECT s.name, s.rollno, s.branch, e.papercode, e.paper_name, a.attend
FROM student s
JOIN Examday e ON s.branch = e.branch
LEFT JOIN attendance a ON a.rollno = s.rollno AND a.paper_code = e.papercode AND a.exam_date = e.examday
WHERE e.examday = '2024-04-15';
UPDATE attendance
SET attend = 'Pending'
WHERE rollno=8006 and exam_date='2024-04-15';
ALTER TABLE student
ADD room int;
SELECT s.rollno, s.semester, sd.category,sd.enrollment, sd.Formno, sd.dept , sd.fname, sd.Mname, sd.Email,sd.mob, s.venue, s.room FROM  student s  JOIN   studentdetails sd ON s.rollno = sd.rollno  where s.rollno = 8006;
SELECT e.papercode ,e.paper_name , e.examday ,a.attend FROM  Examday e JOIN attendance a ON a.paper_code = e.papercode WHERE  a.rollno = 8006 and e.branch='ECC' ORDER BY  a.exam_date;
SELECT name,branch FROM student WHERE rollno=8006 AND passsword='dubey'
alter table teacher Add photo varbinary(MAX)
select * from teacher
insert into teacher(photo) 
SELECT BulkColumn 
FROM Openrowset( Bulk 'A:\finalproject\backend\static\Kapil Parihar.jpeg', Single_Blob) as img 
UPDATE teacher
SET photo = 'A:\finalproject\backend\static\Kapil Parihar.jpeg'
WHERE id=1001
DECLARE @Photo VARBINARY(MAX)
DECLARE @FilePath NVARCHAR(1000) = 'A:\finalproject\backend\static\Kapil Parihar.jpeg'  -- Replace with the actual file path
DECLARE @TeacherID INT = 1002  -- Replace with the appropriate teacher ID

-- Read the image file as binary data using dynamic SQL
DECLARE @Sql NVARCHAR(MAX)
SET @Sql = 'SELECT @Photo = BulkColumn FROM OPENROWSET(BULK ' + QUOTENAME(@FilePath, '''') + ', SINGLE_BLOB) AS img;'
EXEC sp_executesql @Sql, N'@Photo VARBINARY(MAX) OUTPUT', @Photo OUTPUT;

-- Update the teacher record with the binary image data
UPDATE teacher 
SET photo = @Photo
WHERE id = @TeacherID;
select * from  studentdetails

