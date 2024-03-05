import smtplib
import imghdr
from email.message import EmailMessage
 
Sender_Email = "testproject828@gmail.com"
Reciever_Email = "rithikb02@gmail.com"
Password = 'qwerty@12345'
 
newMessage = EmailMessage()                         
newMessage['Subject'] = "Alert!! Face without mask detected..." 
newMessage['From'] = Sender_Email                   
newMessage['To'] = Reciever_Email                   
newMessage.set_content('Image attached...') 
 
with open('photo.webp', 'rb') as f:
    image_data = f.read()
    image_type = imghdr.what(f.name)
    image_name = f.name
 
newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
 
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
 
    smtp.login(Sender_Email, Password)              
    smtp.send_message(newMessage)