import pymysql
from stream_getmongodata import getmongodata

def linktomysql():

    stream_mongo = getmongodata()

    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = pymysql.connect(
            host='localhost',  # 主機名稱
            port=3306,
            db='demo',  # 資料庫名稱
            user='root',  # 帳號
            password='tiba123')  # 密碼
        cursor = connection.cursor()

        username = stream_mongo['username']
        users_table = cursor.execute("INSERT INTO users (id, cookie) VALUES('','%s')" %(username))

        logoname = stream_mongo['logoname']
        category = stream_mongo["categoryname"]
        input_table = cursor.execute(
            "INSERT INTO input_value (logoname, category) VALUES('%s','%s')" % (logoname, category))

        wordname = stream_mongo['name']
        score = stream_mongo['score']
        for i in range(len(wordname)):
            cursor.execute("INSERT INTO output_word (wordname, score) VALUES('%s','%s')" % (wordname[i], score[i]))

        imgname = stream_mongo['imgname']
        imgurl = stream_mongo['imgurl']
        for i in range(len(imgname)):
            cursor.execute("INSERT INTO output_img (imgname, imgurl) VALUES('%s','%s')" % (imgname[i], imgurl[i]))

        acc_table = cursor.execute("INSERT INTO acc (wordacc, imgacc) VALUES('高','低')")

        connection.commit()







        # 顯示資料庫版本
        # db_Info = connection.get_server_info()
        # print("資料庫版本：", db_Info)

        # 顯示目前使用的資料庫
        # cursor = connection.cursor()
        # cursor.execute("SELECT DATABASE();")
        # record = cursor.fetchone()
        # print("目前使用的資料庫：", record)

        # 新增資料
        # sql = "INSERT INTO zoo (name, age) VALUES (%s, %s);"
        # new_data = (data, num)
        # cursor = connection.cursor()
        # cursor.execute(sql, new_data)
        #
        # # 確認資料有存入資料庫
        # connection.commit()

        # 查詢資料庫
        # cursor = connection.cursor()
        # cursor.execute("SELECT name, age FROM zoo;")

        # 列出查詢的資料
        # for (name, age) in cursor:
        #     print("Name: %s, Age: %s" % (name, age))
        # cursor.close()
        # connection.close()

    except Error as e:
        print("資料庫連接失敗：", e)

    finally:
        cursor.close()
        connection.close()
        print("資料庫連線已關閉")

        return print("datato mysql done")

if __name__ =="__main__":

    linktomysql()