import urllib.request
import numpy as np
import cv2

def downloadimg(pic_url):
    with urllib.request.urlopen(pic_url) as resp:
        im_2 = np.asarray(bytearray(resp.read()), dtype="uint8")
        im_2 = cv2.imdecode(im_2, cv2.IMREAD_COLOR)
        return im_2

if __name__ =="__main__":
    pic_url = "https://twtmsearch.tipo.gov.tw/imageLoad.jsp?path=/20160227/102/033/610/pic_102033610_20130627_1.jpg&formatName=jpeg&pathCodeId=282_pic"
    image = downloadimg(pic_url)
    cv2.imshow("Image", image)
    cv2.waitKey(0)