import cv2
import os

if not os.path.exists(os.path.join(os.path.curdir,"data")):
    os.mkdir(os.path.join(os.path.curdir,"data"))

def generate_dataset():
    face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    def face_cropped(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray, 1.3, 5)
        
        if not faces.all():
            return None

        for (x,y,w,h) in faces:
            cropped_face = img[y:y+h,x:x+w]
            return cropped_face
        
    cap = cv2.VideoCapture(0)
    img_id = 0
        
    while True:
        ret, frame = cap.read()
        if face_cropped(frame) is not None:
            img_id+=1
            face = cv2.resize(face_cropped(frame), (200,200))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            file_name_path =os.path.join(os.path.curdir,"data","person1."+str(img_id)+".jpg")
            cv2.imwrite(file_name_path, face)
            cv2.putText(face, str(img_id), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0),2)
                
            cv2.imshow("Cropped_Face", face)
            if cv2.waitKey(1)==13 or int(img_id)==1000:
                break
                    
    cap.release()
    cv2.destroyAllwindows()
    print("collecting samples is completed !!!")
generate_dataset()
                        