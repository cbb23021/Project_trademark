import cv2
import numpy as np
import urllib.request
import pickle
from img_download import downloadimg

def get_image_ans(img1_path,img2_path):
    input_img_1 = cv2.imread(img1_path, cv2.IMREAD_COLOR)
    input_img_2 = downloadimg(img2_path)

    img_1_2 = input_img_1.sum(axis=2)
    (row, col) = img_1_2.shape
    row_top = 0
    raw_down = 0
    col_top = 0
    col_down = 0
    for r in range(0, row):
        if img_1_2.sum(axis=1)[r] < 700 * col:
            row_top = r
            break

    for r in range(row - 1, 0, -1):
        if img_1_2.sum(axis=1)[r] < 700 * col:
            raw_down = r
            break
    for c in range(0, col):
        if img_1_2.sum(axis=0)[c] < 700 * row:
            col_top = c
            break

    for c in range(col - 1, 0, -1):
        if img_1_2.sum(axis=0)[c] < 700 * row:
            col_down = c
            break

    new_img_1 = input_img_1[row_top:raw_down + 1, col_top:col_down + 1, 0:3]

    img_2_1 = input_img_2.sum(axis=2)
    (row, col) = img_2_1.shape
    row_top = 0
    raw_down = 0
    col_top = 0
    col_down = 0
    for r in range(0, row):
        if img_2_1.sum(axis=1)[r] < 700 * col:
            row_top = r
            break

    for r in range(row - 1, 0, -1):
        if img_2_1.sum(axis=1)[r] < 700 * col:
            raw_down = r
            break
    for c in range(0, col):
        if img_2_1.sum(axis=0)[c] < 700 * row:
            col_top = c
            break

    for c in range(col - 1, 0, -1):
        if img_2_1.sum(axis=0)[c] < 700 * row:
            col_down = c
            break

    new_img_2 = input_img_2[row_top:raw_down + 1, col_top:col_down + 1, 0:3]
    new_img_1 = cv2.resize(new_img_1, (30, 30), interpolation=cv2.INTER_CUBIC)
    new_img_2 = cv2.resize(new_img_2, (30, 30), interpolation=cv2.INTER_CUBIC)
    new_img_1 = cv2.cvtColor(new_img_1, cv2.COLOR_BGR2GRAY)
    new_img_2 = cv2.cvtColor(new_img_2, cv2.COLOR_BGR2GRAY)
    (thresh, new_img_1) = cv2.threshold(new_img_1, 127, 255, cv2.THRESH_BINARY)
    (thresh, new_img_2) = cv2.threshold(new_img_2, 127, 255, cv2.THRESH_BINARY)

    #定义边长
    Sidelength=10
    #缩放图像
    img1=cv2.resize(new_img_1,(Sidelength,Sidelength),interpolation=cv2.INTER_CUBIC)
    img2=cv2.resize(new_img_2,(Sidelength,Sidelength),interpolation=cv2.INTER_CUBIC)
    #灰度处理
#         gray1=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
#         gray2=cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    #avglist列表保存每行像素平均值
    avglist1=[]
    avglist2=[]
    #计算每行均值，保存到avglist列表
    for i in range(Sidelength):
        avg1=sum(img1[i])/len(img1[i])
        avg2=sum(img2[i])/len(img2[i])
        avglist1.append(avg1)
        avglist2.append(avg2)
    #返回avglist平均值
    
    diff = [avglist1[j] - avglist2[j] for j in range(len(avglist1))]
    diff = np.array(diff).reshape(1, -1)
    with open("image_simalarity_model_02", 'rb') as file:
        Model = pickle.load(file)
        ans = Model.predict(diff)

    if ans[0] == 1:
        ans = "高"
    else:
        ans = "低"

    return ans

if __name__ =="__main__":
    img1_path = "./static/images/logomark3030.png"
    img2_path = "https://twtmsearch.tipo.gov.tw/imageLoad.jsp?path=/20160227/102/033/610/pic_102033610_20130627_1.jpg&formatName=jpeg&pathCodeId=282_pic"

    ans = get_image_ans(img1_path,img2_path)
    print(ans)