import io
import os
import requests
import random
from datetime import datetime
from time import sleep
import cv2
import display
from google.cloud import vision_v1p3beta1 as vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_key.json'
SOURCE_PATH = "/home/pi/"
FOOD_TYPE = 'Fruit'

def weight():
    return random.randint(100, 1000)

def load_food_name(food_type):
    names = [line.rstrip('\n').lower() for line in open( food_type + '.dict')]
    return names

def recognize_food(list_foods, cap, userID):
    firstRecognize = True
    cap.release()
    cap = cv2.VideoCapture(0)
    img = cap.read()[1]
    height, width = img.shape[:2]
    img = cv2.resize(img, (800, int((height * 800) / width)))
    cv2.imwrite(SOURCE_PATH + "output.jpg", img)
    img_path = SOURCE_PATH + "output.jpg"
    client = vision.ImageAnnotatorClient()
    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    for label in labels:
        desc = label.description.lower()
        score = round(label.score, 2)
        if (desc in list_foods and score >= 0.75):
            print("MATCH FOUND !!!!!! ", desc, " WITH SCORE ", score)
            if score > 0.8:
                if display.otherProduct():
                    foncPOST(desc, weight(), userID)
                else:
                    foncPOST(desc, weight(), userID)
                    return False
            elif display.callUser(desc):
                if display.otherProduct():
                    foncPOST(desc, weight(), userID)
                else:
                    foncPOST(desc, weight(), userID)
                    return False
            firstRecognize = False
    if not firstRecognize:
       display.loading()
    return True

def qrCode(cap):
  userFound = False
  userID = -1
  while not userFound:
     img = cap.read()[1]
     det = cv2.QRCodeDetector()
     retval, points, straight_qrcode = det.detectAndDecode(img)
     if retval:
        userID = requests.get(retval)
        userID = userID.text
        userName = requests.get('https://cueillit.sarq.dev/getName/%s'%userID)
        display.helloUser(userName.text)
        userFound = True
        return userID


def startRecognize():
  while True:
     notFound = True
     display.qrCode()
     cap = cv2.VideoCapture(0)
     userID = qrCode(cap)
     display.newFruit()
     while notFound:
         notFound = recognize_food(load_food_name(FOOD_TYPE), cap, userID)
     print("sortie")

def foncPOST(product, qte, idUser):
  print("Panier : %s de %sg par user %s"%(product, qte, idUser))
  r = requests.post('https://cueillit.sarq.dev/api/products/%s/%s/%s'%(product, qte, idUser))
