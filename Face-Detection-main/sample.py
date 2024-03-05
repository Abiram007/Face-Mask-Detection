import cv2
import h5py
import threading
import datetime
import os
import smtplib
import imghdr
from email.message import EmailMessage
import numpy as np
from tensorflow.keras.layers import GlobalMaxPooling2D, MaxPooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
j = 0
Sender_Email = "testproject828@gmail.com"
Reciever_Email = "abiram5646@gmail.com"
Password = 'qwerty@12345'
def send():
    newMessage = EmailMessage()                         
    newMessage['Subject'] = "Alert!! Face without mask detected..." 
    newMessage['From'] = Sender_Email                   
    newMessage['To'] = Reciever_Email                   
    newMessage.set_content('Image attached might not be accurate...')
    with open("/Users/admin/Documents/Project/Img_hold/test.png", 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name
 
    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    
        smtp.login(Sender_Email, Password)              
        smtp.send_message(newMessage)




model = load_model("/Users/admin/Documents/Project/NEW_MODEL-010.model")
model.save("/Users/admin/Documents/Project/modelNEW.h5")
del model
model=load_model("/Users/admin/Documents/Project/modelNEW.h5")

labels_dict={0:'without mask',1:'mask'}
color_dict={0:(0,0,255),1:(0,255,0)}

size = 4
webcam = cv2.VideoCapture(0)# + cv2.CAP_DSHOW)

classifier = cv2.CascadeClassifier('/Users/admin/Documents/Project/face.xml')
cooldown_begin = datetime.datetime.now()
date  = datetime.date(1,1,1)
cool_down = 0
while webcam.isOpened():
    (rval, im) = webcam.read()
    #print(im)
    mini = cv2.resize(im, (im.shape[1] // size, im.shape[0] // size))
     
    faces = classifier.detectMultiScale(mini)
    
    for f in faces:
        (x, y, w, h) = [v * size for v in f] 
        face_img = im[y:y+h, x:x+w]
        resized=cv2.resize(face_img,(150,150))
        reshaped=np.reshape(resized,(1,150,150,3))
        reshaped = np.vstack([reshaped])
        result=model.predict(reshaped)
        
        
        label=np.argmax(result,axis=1)[0] 
        
        if label==0 and  cool_down>20:
            #t = threading.Thread(target=send)
            j+=1
            cool_down = 0
            print("running")
            cv2.imwrite("/Users/admin/Documents/Project/Img_hold/test.png",im)
            #t.start()
            send()
            os.remove("/Users/admin/Documents/Project/Img_hold/test.png")
        cv2.rectangle(im,(x,y),(x+w,y+h),color_dict[label],2)
        cv2.rectangle(im,(x,y-40),(x+w,y),color_dict[label],-1)
        cv2.putText(im, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        cool_down+=1
        
    cv2.imshow('Run',   im)
    key = cv2.waitKey(10)
     
    if key == 27: 
        break

webcam.release()


cv2.destroyAllWindows()