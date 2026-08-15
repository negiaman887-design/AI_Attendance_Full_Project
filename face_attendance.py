import cv2, sqlite3, os
from datetime import datetime
import face_recognition

known_encodings=[]
known_names=[]

faces_dir="static/faces"

for file in os.listdir(faces_dir):
    path=os.path.join(faces_dir,file)
    img=face_recognition.load_image_file(path)
    enc=face_recognition.face_encodings(img)
    if enc:
        known_encodings.append(enc[0])
        known_names.append(os.path.splitext(file)[0])

cam=cv2.VideoCapture(0)

while True:
    ret,frame=cam.read()
    rgb=frame[:,:,::-1]

    locs=face_recognition.face_locations(rgb)
    encs=face_recognition.face_encodings(rgb,locs)

    for enc in encs:
        matches=face_recognition.compare_faces(known_encodings,enc)

        if True in matches:
            name=known_names[matches.index(True)]

            conn=sqlite3.connect("attendance.db")
            conn.execute(
                "INSERT INTO attendance(student_id,date,time) VALUES(?,?,?)",
                (name,str(datetime.now().date()),str(datetime.now().time())[:8])
            )
            conn.commit()
            conn.close()

    cv2.imshow("Attendance Camera",frame)

    if cv2.waitKey(1)==27:
        break

cam.release()
cv2.destroyAllWindows()
