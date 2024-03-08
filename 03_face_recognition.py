import cv2
import numpy as np
import os 

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Ezz','John','Maram','Marah','Yasmin','Rahaf']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:

    ret, img =cam.read()
    # img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
print(id)
ma=input("enter amount")

import mysql.connector
# Creating connection object
conn = mysql.connector.connect(
    host = "sql8.freesqldatabase.com",
    user = "sql8678335",
    password = "pEPYlSQacx",
    database= "sql8678335"
)
 

#mycursor = conn.cursor()
#sql="insert into Persons (PersonID,LastName,FirstName,PASS,amount) values (%s,%s,%s,%s,%s)"
#val=(2,"Ezz","Obada","123",100)
#mycursor.execute(sql,val)
#conn.commit()

mycursor = conn.cursor(buffered=True)
#mycursor.execute("Select  @myNum := amount from Persons where LastName="+str(id))
sql="Select amount from Persons where LastName = \""+str(id)+"\""

mycursor.execute(sql)
result=mycursor.fetchall()
amount=result[0][0]
amount=amount-int(ma)
#mycursor.execute("UPDATE Persons SET amount= %s WHERE PersonID=2")
sql="UPDATE Persons SET amount="+str(amount)+" WHERE LastName = \""+str(id)+"\""
mycursor.execute(sql)
conn.commit()

