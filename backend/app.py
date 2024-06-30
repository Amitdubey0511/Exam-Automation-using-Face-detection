from flask import Flask, render_template, redirect, request, session, url_for
import pyodbc
import cv2
import os
from datetime import datetime
import csv
import time
import base64

app = Flask(__name__)
app.secret_key = 'secret_key'

conn = pyodbc.connect("DRIVER={SQL Server};SERVER=ASUS;DATABASE=EXAM;")
cursor = conn.cursor()

def train_classifier(data_dir):
    path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    faces = []
    ids = []

    for image in path:
        img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        imageNp = np.array(img, 'uint8')
        id1 = int(os.path.split(image)[1].split(".")[1])

        faces.append(imageNp)
        ids.append(id1)

    ids = np.array(ids)

    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("classifier.xml")

def mark_attendance(user_id, name, attendance):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attendance[user_id] = {'Name': name, 'Latest_Attendance_Time': current_time}
    save_attendance_to_csv(attendance)

def save_attendance_to_csv(attendance):
    try:
        with open('attendance.csv', 'w', newline='') as csvfile:
            fieldnames = ['User_ID', 'Name', 'Latest_Attendance_Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user_id, data in attendance.items():
                writer.writerow({'User_ID': user_id, 'Name': data['Name'], 'Latest_Attendance_Time': data['Latest_Attendance_Time']})
    except Exception as e:
        print(f"Error saving attendance to CSV: {e}")

def get_user_name(user_id):
    # Add a mapping or database lookup for user IDs to names
    # Modify this function according to your requirements
    if user_id == 1:
        return "Amit Dubey"
    elif user_id == 2:
        return "Bhanu Priya Dixit"
    elif user_id == 3:
        return "Abhishek choudhary"
    elif user_id == 4:
        return "Chirag mangal"
    else:
        return "UNKNOWN"

@app.route('/', methods=['GET', 'POST'])
def teacher_login():
    if request.method == 'POST':
        session.pop('teacher_id', None)
        tid = request.form['tid']
        password = request.form['pswd']
        cursor.execute("SELECT name FROM teacher WHERE id=? AND passworrd=?", (tid, password))
        teacher = cursor.fetchone()
        if teacher:
            session['logged_in'] = True
            session['teacher_id'] = tid
            session['teacher_name']=teacher[0]
            cursor.execute("SELECT room_no,exam_date,department_name FROM teacher_duty WHERE id=?",(tid))
            teacherdetail=cursor.fetchone()
            session['room_no']=teacherdetail[0]
            session['exam_date']=teacherdetail[1]
            session['department_name']=teacherdetail[2]
            session['attend']=""
            cursor.execute("SELECT photo FROM teacher WHERE id=?", (tid))
            photo=cursor.fetchval()
            photo_data = base64.b64encode(photo).decode('utf-8')
            return redirect(url_for('teacher_details'))
        else:
            error_message = "Invalid login credentials. Please try again."
            return render_template('login.html', error_message=error_message)
    # If login fails or it's a GET request, render the login page
    return render_template('login.html')

@app.route('/studentlist')
def studentlist():
    if session.get('logged_in'):
        item=[]
        
        cursor.execute("SELECT s.name, s.rollno, s.branch, e.papercode, e.paper_name, a.attend FROM student s JOIN Examday e ON s.branch = e.branch LEFT JOIN attendance a ON a.rollno = s.rollno AND a.paper_code = e.papercode AND a.exam_date = e.examday WHERE e.examday = ? ORDER BY s.rollno;",(session['exam_date']))
        for row in cursor.fetchall():
            item_dict={}
            item_dict["name"]=row[0]
            item_dict["rollno"]=row[1]
            item_dict["branch"]=row[2]
            item_dict["Papercode"]=row[3]
            item_dict["Paper_name"]=row[4]
            item_dict["attendance"]=row[5]
            item.append(item_dict)
        indexed_list = [(index, item) for index, item in enumerate(item)]
        return render_template('studentlist.html',name=session['teacher_name'],list=indexed_list)
    else:
        return redirect(url_for('teacher_login'))
    
@app.route('/teacherDetails')
def teacher_details():
    if session.get('logged_in'):
        # cursor.execute("SELECT photo FROM teacher WHERE id=?", (session['teacher_id']))
        # photo=cursor.fetchval()
        # photo_data = base64.b64encode(photo).decode('utf-8')
        return render_template('teacherDetails.html',
                               name=session['teacher_name'],id=session['teacher_id'],dept= session['department_name'],
                               room=session['room_no'],date=session['exam_date'])
    else:
        return redirect(url_for('teacher_login'))
    
@app.route('/dropsession')
def dropsession():
    session.pop('logged_in',None)
    return redirect(url_for('teacher_login'))


@app.route('/student',methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        session.pop('student_id', None)
        sid = request.form['stid']
        password = request.form['stpassword']
        cursor.execute("SELECT name,branch FROM student WHERE rollno=? AND passsword=?", (sid, password))
        student = cursor.fetchone()
        if student:
            session['logged_in'] = True
            session['student_rollno'] = sid
            session['student_name']=student[0]
            session['student_branch']=student[1]
            return redirect(url_for('studentDetails'))
        else:
            error_message = "Invalid login credentials. Please try again."
            return render_template('login.html', error_message=error_message)
    # If login fails or it's a GET request, render the login page
    
    return render_template('login.html')
@app.route('/studentDetails')
def studentDetails():
    if session.get('logged_in'):
           
           return render_template('studentDetails.html',name=session['student_name'])
    else:
        return redirect(url_for('student_login'))


@app.route('/admitcard')
def admitcard():
    if session.get('logged_in'):
        cursor.execute("SELECT s.rollno, s.semester, sd.category,sd.enrollment, sd.Formno, sd.dept , sd.fname, sd.Mname, sd.Email,sd.mob, s.venue, s.room FROM  student s  JOIN   studentdetails sd ON s.rollno = sd.rollno  where s.rollno =?;",(session['student_rollno']))
        studentdet = cursor.fetchone()
        return render_template('admitcard.html', name=session['student_name'],student=studentdet)
    else:
        return redirect(url_for('student_login'))

@app.route('/timetable')
def timetable():
    if session.get('logged_in'):
        cursor.execute("SELECT e.papercode ,e.paper_name , e.examday ,a.attend FROM  Examday e JOIN attendance a ON a.paper_code = e.papercode WHERE  a.rollno = ? and e.branch=? ORDER BY  a.exam_date;",(session['student_rollno'],session['student_branch']))
        item=[]
        for row in cursor.fetchall():
            item_dict={}
            item_dict["papercode"]=row[0]
            item_dict["paper_name"]=row[1]
            item_dict["examday"]=row[2]
            item_dict["attend"]=row[3]
            item.append(item_dict)
        indexed_list = [(index, item) for index, item in enumerate(item)]
        return render_template('timetable.html', name=session['student_name'],table=indexed_list)
    else:
        return redirect(url_for('student_login'))




@app.route('/capture_attendance',methods=['GET', 'POST'])
def capture_attendance():
    if request.method == 'POST':
     faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
     clf = cv2.face.LBPHFaceRecognizer_create()
     clf.read("classifier.xml")

     video_capture = cv2.VideoCapture(0)
     attendance = {}

     start_time = time.time()
     detected_names = set()

     while time.time() - start_time < 10:
        ret, img = video_capture.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = faceCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in features:
            id, pred = clf.predict(gray[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))

            if confidence > 70:
                user_id = str(id)
                name = get_user_name(id)
                detected_names.add(name)
                if user_id not in attendance:
                    attendance[user_id] = {'Name': name, 'Latest_Attendance_Time': None}
                mark_attendance(user_id, name, attendance)

        cv2.imshow("Face Detection", img)

        if cv2.waitKey(1) == 13:
            break

     video_capture.release()
     cv2.destroyAllWindows()

     if detected_names:
        print("Detected faces:", detected_names)
     else:
        print("No face detected.")
     
     stname=request.form['stname']
     roll=request.form['stroll']
     papercode=request.form['papercode']
     if stname in detected_names:
         cursor.execute("UPDATE attendance SET attend = 'Present' WHERE rollno=? and paper_code=?",(roll,papercode))
         conn.commit()
     else  :
            cursor.execute("UPDATE attendance SET attend = 'Abesent' WHERE rollno=? and paper_code=?",(roll,papercode))
            conn.commit()
    return redirect(url_for('studentlist'))



if __name__ == '__main__':
    app.run(debug=True)