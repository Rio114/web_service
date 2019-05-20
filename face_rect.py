from PIL import Image
import numpy as np
import cv2
import sys
from werkzeug import secure_filename
import sqlite3
from contextlib import closing
from handle_db import db_save_image
import os

db_name = 'database.db'
OUTPUT_FOLDER = './outputs'

def face_rect_out(image_path, cascade_path, output_path):

    image = cv2.imread(image_path)
    image_shape = (image.shape[1],image.shape[0])
    image_center = (int(image.shape[1]/2),int(image.shape[0]/2))
    angle = 0

    mtx = cv2.getRotationMatrix2D(image_center, angle, 1)
    image_rot = cv2.warpAffine(image, mtx, image_shape)
    image_gray = cv2.cvtColor(image_rot, cv2.COLOR_BGR2GRAY)

    cascade = cv2.CascadeClassifier(cascade_path)
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=2, minSize=(50, 50))

    # 検出した場合
    if len(facerect) > 0:
        color = (255, 0, 255) 
        #検出した顔を囲む矩形の作成
        rect_data = []
        trimmed_images = []
        trimmed_image_url = []
        for i, rect in enumerate(facerect):
            xmin = rect[0]
            ymin = rect[1]
            xmax = rect[0]+rect[2]
            ymax = rect[1]+rect[3]
            trimmed = image[ymin:ymax, xmin:xmax, :] 
            trimmed_images.append(trimmed)
            url = os.path.join(OUTPUT_FOLDER, '{}.jpg'.format(i))
            trimmed_image_url.append(url)
            cv2.imwrite(url, trimmed)

        for rect in facerect:
            cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2) 
            rect_data.append((image_path.split('/')[-1], int(xmin), int(ymin), int(xmin-xmax), int(ymin-ymax)))

        #認識結果の保存
        db_save_image(rect_data)

    #認識結果の保存
    cv2.imwrite(output_path, image)
    return trimmed_image_url


if __name__ == "__main__":
    #image_path = "test0.jpg"
    cascade_path = "haarcascade_frontalface_default.xml"
    output_path = "output.jpg"
    face_rect_out(sys.argv[1], cascade_path, output_path)