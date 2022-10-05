"""
Recognize food: fruit, vegetable
"""

import io
import os
from datetime import datetime
from time import sleep

import cv2
from google.cloud import vision_v1p3beta1 as vision

# Setup google authen client key
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'client_key.json'

# Source path content all images
SOURCE_PATH = "D:\workspace-b3\py.cueillit.org/"

FOOD_TYPE = 'Fruit'  # 'Vegetable'


def load_food_name(food_type):
    """
    Load all known food type name.
    :param food_type: Fruit or Vegetable
    :return:
    """
    names = [line.rstrip('\n').lower() for line in open( food_type + '.dict')]
    return names


def recognize_food(list_foods):
    print('Trying to find food in image...')
    cap = cv2.VideoCapture(0)
    img = cap.read()[1]
    height, width = img.shape[:2]
    img = cv2.resize(img, (800, int((height * 800) / width)))
    # Save the image to temp file
    cv2.imwrite(SOURCE_PATH + "output.jpg", img)
    # Create new img path for google vision
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
        print("label: ", desc, "  score: ", score)
        if (desc in list_foods):
            cv2.putText(img, desc.upper() + " ???", (300, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 200), 2)
            cv2.imshow('Recognize & Draw', img)
            cv2.waitKey(0)
            break
    return True

list_foods = load_food_name(FOOD_TYPE)

notFound = True
while notFound:
  recognize_food(list_foods)