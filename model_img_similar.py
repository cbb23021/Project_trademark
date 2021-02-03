from keras.applications.densenet import DenseNet121
from keras.applications.densenet import preprocess_input
import time
import tensorflow as tf
from tensorflow import keras
import numpy as np
from numpy import linalg as LA
import h5py
from skimage import io
import pymongo

# run model找出feature
def extract_feat(img_path):
    input_shape = (224,224,3)
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(input_shape[0], input_shape[1]))
    img = keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    model_densenet = DenseNet121(weights ='imagenet',
                            input_shape = (224,224,3),
                            pooling = 'max', include_top = False)
    feat = model_densenet.predict(img)
    norm_feat = feat[0]/LA.norm(feat[0])
    return norm_feat

# Output imageUrl
def find_imgUrl(img_input):
    model_h5 = r"./feat_017.h5"   # feat.h5 檔案路徑
    h5f = h5py.File(model_h5, 'r')
    feats = h5f['dataset_1'][:]
    imgNames = h5f['dataset_2'][:]

    feat = extract_feat(img_input)
    scores = np.dot(feat, feats.T)
    rank_ID = np.argsort(scores)[::-1]

    imlist = []
    maxres = 3  # output 相似img數量
    for i, score in enumerate(rank_ID[0:maxres]):
        imgid = str(imgNames[score], 'utf-8').split("_")[1].split(".")[0]# 照片名稱 EX:"001_000000015" 取後段 imgId
        # print(imgid)  #輸入相似 imgId
        imlist.append(imgid)

    myclient = pymongo.MongoClient('localhost', 27017)   # MongoDB (ip,27017)
    mydb = myclient.demo  # dbName
    mycol = mydb.zoo  # collectionName
    results = mycol.find({})
    Urllist = []

    for result in results:
        if result["_id"] in imlist: # key
            imgurl = result["image"]
            imgname = result["tmark-name"]
            Urllist.append([imgname,imgurl])
    print(Urllist)
    return Urllist
    
# Output image
# def find_img(classNo, img_input):
#     model_h5 = 'models/feature_%s.h5' % classNo
#     h5f = h5py.File(model_h5, 'r')
#     feats = h5f['dataset_1'][:]
#     imgNames = h5f['dataset_2'][:]
#
#     feat = extract_feat(img_input)
#     scores = np.dot(feat, feats.T)
#     rank_ID = np.argsort(scores)[::-1]
#
#     imlist = []
#     maxres = 3  # output 數量
#     for i, score in enumerate(rank_ID[0:maxres]):
#         imgid = str(imgNames[score], 'utf-8').split("_")[1]
#         print(imgid)
#         imlist.append(imgid)
#     myclient = pymongo.MongoClient('localhost', 27017)
#     mydb = myclient.test
#     mycol = mydb.tmark_json
#     results = mycol.find({})
#     for result in results:
#         if result["_id"] in imlist:
#             image = io.imread(result["image"])
#             io.imshow(image)
#             io.show()

#     print(find_imgUrl('012','./database/089037461.jpg'))


if __name__ =="__main__":
    img_path = "./logomark3030.png"
    res = find_imgUrl(img_path)
    # print(res)
