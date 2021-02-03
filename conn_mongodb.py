from pymongo import MongoClient
import time
from conn_mysql import linktomysql

# link mongodb
client = MongoClient('localhost', 27017)
db = client['demo']
col = db['kafkadata']
cold = db['kafkadatademo']

def status_open(output_kafka_value):
    col.insert_one(output_kafka_value)
    return print("datatomongo open...")


def status_doing(output_kafka_value,logo_namecheck,cate_name):
    find_list = list()
    for i in col.find({
    "username": output_kafka_value["username"],
    "logoname" : output_kafka_value["logoname"],
    "category3" : output_kafka_value["category3"],
    }):
        find_list.append(i)
        input_content = col.find_one(find_list[-1])

    status_doing = col.update_one(input_content,{"$set":{
          "username": output_kafka_value["username"],
          "logoname" : output_kafka_value["logoname"],
          "category3" : output_kafka_value["category3"],
          "filepath" : output_kafka_value["filepath"],
          "status":"doing",
          "updatetime": time.time(),
          "famousname": logo_namecheck,
          "categoryname": cate_name,

          "name": [
              "-資料處理中-", "-資料處理中-", "-資料處理中-", "-資料處理中-", "-資料處理中-",
          ],
          "score": [
              "-資料處理中-", "-資料處理中-", "-資料處理中-", "-資料處理中-", "-資料處理中-"
          ],
          "imgname": [
              "-資料處理中-", "-資料處理中-", "-資料處理中-",
          ],
          "imgurl": [
              "-資料處理中-", "-資料處理中-", "-資料處理中-",
          ],
          "wordacc": "-資料處理中-",
          "imgacc": "-資料處理中-"
        }})

    print("datatomongo doing...")
    return status_doing

def status_done(output_kafka_value,name1, name2, name3, name4, name5,
                score1, score2, score3, score4, score5,
                imgname1, imgname2, imgname3,
                imgurl1, imgurl2, imgurl3,
                acc,imgacc,
                logo_namecheck,cate_name):

    # find mongo data
    find_list = []
    for i in col.find({
    "username": output_kafka_value["username"],
    "logoname": output_kafka_value["logoname"],
    "category3": output_kafka_value["category3"],
    }):
        find_list.append(i)
        print(find_list)
        doing_content = col.find_one(find_list[-1])


    done_update = col.update_one(doing_content,{"$set":{
        "username": output_kafka_value["username"],
        "logoname": output_kafka_value["logoname"],
        "category3": output_kafka_value["category3"],
        "filepath" : output_kafka_value["filepath"],
        "status":"done",
        "updatetime": time.time(),
        "famousname": logo_namecheck ,
        "categoryname": cate_name,

        "name" : [
            name1, name2, name3, name4, name5,
        ],
        "score" : [
            score1, score2, score3, score4, score5
        ],
        "imgname":[
            imgname1, imgname2, imgname3,
        ],
        "imgurl":[
            imgurl1, imgurl2, imgurl3,
        ],
        "wordacc": acc,
        "imgacc":imgacc
    }})
    print("datatomongo done!!")
    linktomysql()
    return done_update

def status_done_word(output_kafka_value,name1, name2, name3, name4, name5,
                score1, score2, score3, score4, score5,
                acc,
                ):

    # find mongo data
    find_list = []
    for i in cold.find({
    "username": output_kafka_value["username"],
    "logoname": output_kafka_value["logoname"],
    "category3": output_kafka_value["category3"],
    }):
        find_list.append(i)
        print(find_list)
        doing_content = cold.find_one(find_list[-1])


    done_update = cold.update_one(doing_content,{"$set":{
        "username": output_kafka_value["username"],
        "logoname": output_kafka_value["logoname"],
        "category3": output_kafka_value["category3"],
        "filepath" : output_kafka_value["filepath"],
        "status":"done",
        "updatetime": time.time(),
        "name" : [
            name1, name2, name3, name4, name5,
        ],
        "score" : [
            score1, score2, score3, score4, score5
        ],
        "wordacc": acc
    }})
    print("datatomongo done!!")
    linktomysql()
    return done_update

def status_done_img(output_kafka_value,
                imgname1, imgname2, imgname3,
                imgurl1, imgurl2, imgurl3,
                imgacc,
                ):

    # find mongo data
    find_list = []
    for i in cold.find({
    "username": output_kafka_value["username"],
    "logoname": output_kafka_value["logoname"],
    "category3": output_kafka_value["category3"],
    }):
        find_list.append(i)
        print(find_list)
        doing_content = cold.find_one(find_list[-1])


    done_update = cold.update_one(doing_content,{"$set":{
        "username": output_kafka_value["username"],
        "logoname": output_kafka_value["logoname"],
        "category3": output_kafka_value["category3"],
        "filepath" : output_kafka_value["filepath"],
        "status":"done",
        "updatetime": time.time(),
        "imgname":[
            imgname1, imgname2, imgname3,
        ],
        "imgurl":[
            imgurl1, imgurl2, imgurl3,
        ],
        "imgacc":imgacc
    }})
    print("datatomongo done!!")
    linktomysql()
    return done_update


if __name__ =="__main__":
    value = {'username': 'test1@yahoo_com_tw', 'logoname': '香奈', 'category3': '017', 'filepath': './static/images/md3.jpg', 'status': 'open'}
    name1 = "xx"
    name2 = "xx"
    name3 = "xx"
    name4 = "xx"
    name5 = "xx"
    score1 = "1"
    score2 = "1"
    score3 = "1"
    score4 = "1"
    score5 = "1"
    imgurl1 = "xx"
    imgurl2 = "xx"
    imgurl3 = "xx"
    imgname1 = "xx"
    imgname2 = "xx"
    imgname3 = "xx"
    acc = "xx"
    imgacc="xx"
    logo_namecheck= "xx"
    cate_name ="xx"
    # status_open(value)
    # status_doing(value,logo_namecheck,cate_name)
    # status_done(value,name1, name2, name3, name4, name5,score1, score2, score3, score4, score5,imgname1, imgname2, imgname3,imgurl1, imgurl2, imgurl3,acc,imgacc,logo_namecheck,cate_name)
    # status_done_word(value, name1, name2, name3, name4, name5, score1, score2, score3, score4, score5, acc)
    # status_done_img(value,imgname1, imgname2,imgname3, imgurl1, imgurl2, imgurl3, imgacc)

