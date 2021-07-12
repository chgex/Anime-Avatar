"""
crop face from image

"""

import cv2
import sys
import os.path
from glob import glob


def newBbox(imgShape,bbox):
    # 48*48 to 96*96
    height,width=imgShape
    x,y,w,h=bbox
    xmin = int(max(x - round(w/2) ,0))
    xmax = int(min(x + w + round(w/2),width))
    ymin = int(max(y - round(h/2) ,0))
    ymax = int(min(y + h + round(h/2),height))
    return xmin, ymin, xmax, ymax


def detect(filename, cnt,savePath,cascade_file = "./lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    
    faces = cascade.detectMultiScale(gray,
                                     # detector options
                                     scaleFactor = 1.1,
                                     minNeighbors = 5,
                                     minSize = (24, 24))
    # for box in faces:
    #     xmin, ymin, xmax, ymax = newBbox(image.shape[:2],box)
    #     print(xmax-xmin)
    #     print(ymax-ymin)
    #     cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
    # cv2.imshow("AnimeFaceDetect", image)
    # cv2.waitKey(0)
    # # cv2.imwrite("out.png", image)

    for i, box in enumerate(faces):
        xmin, ymin, xmax, ymax = newBbox(image.shape[:2],box)
        face = image[ymin:ymax,xmin:xmax,:]        
        save_filename = savePath + "/" + str(cnt).zfill(5) + "-" + str(i) + ".jpg"
        cv2.imwrite(save_filename, face)

def main(filePath,savePath):
    assert os.path.exists(filePath), "file path {} not find".format(filePath)
    if os.path.exists(savePath) is False:
        os.makedirs(savePath)
    file_list = glob(filePath + "/" + "*.jpg")
    cnt=0
    total=len(file_list)
    for image in file_list:
        cnt+=1
        detect(image,cnt,savePath)
        if cnt%100 == 0:print("current:%d, total:%d "%(cnt,total) + image.split("/")[-1])


if __name__ == '__main__':
    
    filePath="IMAGES"
    savePath="FaceData/FaceData"

    main(filePath,savePath)