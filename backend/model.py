import os
import cv2
from PIL import Image
import numpy as np
from datetime import datetime
import csv
import time

def generate_dataset():
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return None
        
        # Only consider the last detected face for cropping
        x, y, w, h = faces[-1]
        cropped_face = img[y:y+h, x:x+w]
        
        return cropped_face

    cap = cv2.VideoCapture(0)
    id = 3
    img_id = 0
    
    while True:
        ret, frame = cap.read()
        
        cropped_face = face_cropped(frame)
        if cropped_face is not None:
            img_id += 1
            face = cv2.resize(cropped_face, (200, 200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_name_path = f"A:/finalproject/backend/data/user.{id}.{img_id}.jpg"
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Cropped face", face)
        
        if cv2.waitKey(1) == 13 or img_id == 50:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Collecting samples is completed....")

generate_dataset()

def train_classifier(data_dir):
    path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
    faces = []
    ids = []

    for image in path:
        img = Image.open(image).convert('L')
        imageNp = np.array(img, 'uint8')
        id1 = int(os.path.split(image)[1].split(".")[1])
        faces.append(imageNp)
        ids.append(id1)

    ids = np.array(ids)

    # Train and save classifier
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("classifier.xml")
train_classifier("A:/finalproject/backend/data")   

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf, attendance):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    detected_names = set()

    for (x, y, w, h) in features:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        id, pred = clf.predict(gray_img[y:y + h, x:x + w])
        confidence = int(100 * (1 - pred / 300))

        if confidence > 70:
            user_id = str(id)
            name = get_user_name(id)
            detected_names.add(name)
            if user_id not in attendance:
                attendance[user_id] = {'Name': name, 'Latest_Attendance_Time': None}

            mark_attendance(user_id, name, attendance)
            cv2.putText(img, name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        else:
            cv2.putText(img, "UNKNOWN", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

    return img, detected_names

def mark_attendance(user_id, name, attendance):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    attendance[user_id]['Latest_Attendance_Time'] = current_time
    save_attendance_to_csv(attendance)

def save_attendance_to_csv(attendance):
    try:
        with open('attendance.csv', 'w', newline='') as csvfile:
            fieldnames = ['User_ID', 'Name', 'Latest_Attendance_Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user_id, data in attendance.items():
                latest_attendance_time = data.get('Latest_Attendance_Time', '')  # Use get to handle missing key
                writer.writerow({'User_ID': user_id, 'Name': data['Name'], 'Latest_Attendance_Time': latest_attendance_time})
    except Exception as e:
        print(f"Error saving attendance to CSV: {e}")

def get_user_name(user_id):
    # Add a mapping or database lookup for user IDs to names
    # Modify this function according to your requirements
    if user_id == 4:
        return "chirag"
    elif user_id == 2:
        return "Bhanu Priya Dixit"
    elif user_id == 1:
        return "Amit"
    elif user_id == 3:
        return "Abhishek"
    else:
        return "UNKNOWN"

# loading classifier
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

clf = cv2.face.LBPHFaceRecognizer_create()
clf.read("classifier.xml")

video_capture = cv2.VideoCapture(0)

# Dictionary to store attendance information
attendance = {}

# Load existing attendance data from CSV (if available)
try:
    with open('attendance.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row['User_ID']
            name = row['Name']
            latest_attendance_time = row.get('Latest_Attendance_Time', '')  # Use get to handle missing key
            attendance[user_id] = {'Name': name, 'Latest_Attendance_Time': latest_attendance_time}
except FileNotFoundError:
    pass  # The file doesn't exist initially

start_time = time.time()
detected_names = set()  # Set to store unique detected names

while time.time() - start_time < 2:
    ret, img = video_capture.read()
    img, names = draw_boundary(img, faceCascade, 1.3, 6, (255, 255, 255), "Face", clf, attendance)
    detected_names.update(names)  # Update the set with detected names
    cv2.imshow("Face Detection", img)

    if cv2.waitKey(1) == 13:  # Press Enter key to exit
        break

# Check if any face was detected
if detected_names:
    print("Detected faces:", detected_names)
else:
    print("No face detected.")

video_capture.release()
cv2.destroyAllWindows()