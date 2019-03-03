from PIL import Image
import numpy as np
import cv2
import sys
from werkzeug import secure_filename
import sqlite3
from contextlib import closing
db_name = 'database.db'

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
        color = (255, 0, 255) #白
        #検出した顔を囲む矩形の作成
        rect_data = []
        for rect in facerect:
            cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), color, thickness=2)
            rect_data.append((image_path.split('/')[-1], int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3])))

        #認識結果の保存
        with closing(sqlite3.connect(db_name)) as conn:
            c = conn.cursor()
            create_table = '''CREATE TABLE IF NOT EXISTS images (id integer primary key, file_name varchar(64), x_pos int, y_pos int, width int, hight int)'''
            c.execute(create_table)
            insert_sql = 'INSERT INTO images (file_name, x_pos, y_pos, width, hight) values (?, ?, ?, ?, ?)'
            c.executemany(insert_sql, rect_data)
            conn.commit()

            select_sql = 'SELECT * FROM images'
            for row in c.execute(select_sql):
                print(row)
    #認識結果の保存
    cv2.imwrite(output_path, image)

if __name__ == "__main__":
    #image_path = "test0.jpg"
    cascade_path = "haarcascade_frontalface_default.xml"
    output_path = "output.jpg"
    face_rect_out(sys.argv[1], cascade_path, output_path)