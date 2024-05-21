import cv2
import os

dataPath = 'videos'
imagePaths = os.listdir(dataPath)

def detectFace(filename: str):
    global imagePaths
    reconocido = False
    
    face_recognizer = cv2.face.EigenFaceRecognizer_create()
    face_recognizer.read('modeloEigenFace.yaml')
    cap = cv2.VideoCapture(filename)
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
 
    while reconocido==False:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()

        faces = faceClassif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y+h, x:x+w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)
            print(result)
            cv2.putText(frame, '{}'.format(result), (x, y-5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
            
            # EigenFaces
            if result[1] < 4500:
                print("reconocido, es:", imagePaths[result[0]])
                reconocido = True
                break
        
        
        if reconocido:
            break
        
                
    if reconocido:
        return imagePaths[result[0]]
    else:
        return "desconocido"