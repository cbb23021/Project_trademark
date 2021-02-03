from confluent_kafka import Consumer, KafkaException, KafkaError
import sys
import json

from conn_mongodb import status_open,status_doing,status_done

# word model
from model_word_famous import check_famous
from model_word_acc import find_same_word
from category_data import checkdata

# img model
from model_img_similar import find_imgUrl
from model_img_acc import get_image_ans


# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)


# 轉換msgKey或msgValue成為utf-8的字串
def try_decode_utf8(data):
    if data:
        return data.decode('utf-8')
    else:
        return None


# 當發生commit時被呼叫
def print_commit_result(err, partitions):
    if err:
        print('# Failed to commit offsets: %s: %s' % (err, partitions))
    else:
        for p in partitions:
            print('# Committed offsets for: %s-%s {offset=%s}' % (p.topic, p.partition, p.offset))

def getdata():
    """
    flow kafka value to model
    """
    # 步驟1.設定要連線到Kafka集群的相關設定
    # Consumer configuration
    # See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
    props = {
        'bootstrap.servers': '10.1.0.189:9092',  # Kafka集群在那裡? (置換成要連接的Kafka集群)
        'group.id': 'iii',  # ConsumerGroup的名稱 (置換成你/妳的學員ID)
        'auto.offset.reset': 'latest',  # 是否從這個ConsumerGroup尚未讀取的partition/offset開始讀
        'enable.auto.commit': False,  # 是否啟動自動commit
        'on_commit': print_commit_result,  # 設定接收commit訊息的callback函數
        'error_cb': error_cb  # 設定接收error訊息的callback函數
    }

    # 步驟2. 產生一個Kafka的Consumer的實例
    consumer = Consumer(props)
    # 步驟3. 指定想要訂閱訊息的topic名稱
    topicName = 'zoo'
    # 步驟4. 讓Consumer向Kafka集群訂閱指定的topic
    consumer.subscribe([topicName])

    # 步驟5. 持續的拉取Kafka有進來的訊息
    try:
        while True:
            records_pulled = False  # 用來檢查是否有有效的record被取出來
            # 請求Kafka把新的訊息吐出來
            records = consumer.consume(num_messages=1, timeout=1.0)  # 批次讀取
            if records is None:
                continue
            for record in records:
                # 檢查是否有錯誤
                if record is None:
                    continue
                if record.error():
                    # Error or event
                    if record.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (record.topic(), record.partition(), record.offset()))
                    else:
                        # Error
                        raise KafkaException(record.error())
                else:
                    records_pulled = True
                    # ** 在這裡進行商業邏輯與訊息處理 **
                    # 取出相關的metadata
                    topic = record.topic()
                    partition = record.partition()
                    offset = record.offset()
                    timestamp = record.timestamp()

                    # 取出msgKey與msgValue
                    msgKey = try_decode_utf8(record.key())
                    msgValue = eval(try_decode_utf8(record.value()))
                    print(type(msgValue))
                    print("start consuming data... key:{} value:{}".format(msgKey, msgValue))

                    # run mongodb
                    # mongodb-open
                    status_open(msgValue)

                    logoname = msgValue["logoname"]
                    category3 = msgValue["category3"]

                    # check 著名商標
                    logo_namecheck = check_famous(logoname)

                    # check 類別名稱
                    cate_name = checkdata(category3)

                    # mongodb-doing
                    status_doing(msgValue,logo_namecheck,cate_name)

                    # word model + acc
                    print("start model acc...", str(category3.rjust(3,"0")))
                    db_path = r"./g_code_tname_clean.csv"

                    res5 = find_same_word(str(logoname), str(category3.rjust(3,"0")), db_path)
                    print(res5)

                    if len(res5) == 6:
                        name1 = res5[0][0]
                        name2 = res5[1][0]
                        name3 = res5[2][0]
                        name4 = res5[3][0]
                        name5 = res5[4][0]
                        score1 = res5[0][1]
                        score2 = res5[1][1]
                        score3 = res5[2][1]
                        score4 = res5[3][1]
                        score5 = res5[4][1]
                        acc = res5[5][1]

                    elif len(res5) == 5:
                        name1 = res5[0][0]
                        name2 = res5[1][0]
                        name3 = res5[2][0]
                        name4 = res5[3][0]
                        name5 = "null"
                        score1 = res5[0][1]
                        score2 = res5[1][1]
                        score3 = res5[2][1]
                        score4 = res5[3][1]
                        score5 = "null"
                        acc = res5[4][1]

                    elif len(res5) == 4:
                        name1 = res5[0][0]
                        name2 = res5[1][0]
                        name3 = res5[2][0]
                        name4 = name5 = "null"
                        score1 = res5[0][1]
                        score2 = res5[1][1]
                        score3 = res5[2][1]
                        score4 = score5 = "null"
                        acc = res5[3][1]

                    elif len(res5) == 3:
                        name1 = res5[0][0]
                        name2 = res5[1][0]
                        name3 = name4 = name5 = "null"
                        score1 = res5[0][1]
                        score2 = res5[1][1]
                        score3 = score4 = score5 = "null"
                        acc = res5[2][1]
                    else:
                        name1 = res5[0][0]
                        name2 = name3 = name4 = name5 = "null"
                        score1 = res5[0][1]
                        score2 = score3 = score4 = score5 = "null"
                        acc = res5[1][1]

                    # img model
                    print("start img...")
                    filepath= msgValue["filepath"].replace("=",".")
                    imglist = find_imgUrl(filepath)
                    imgurl1 = imglist[0][1]
                    imgurl2 = imglist[1][1]
                    imgurl3 = imglist[2][1]
                    imgname1 = imglist[0][0]
                    imgname2 = imglist[1][0]
                    imgname3 = imglist[2][0]

                        # img acc
                    print("imgacc start...")
                    imgacc = get_image_ans(filepath, imgurl1)
                    print("imgacc done",imgacc)

                    print(name1, name2, name3, name4, name5, acc)
                    print(score1, score2, score3, score4, score5, acc)

                    #mongodb-done
                    status_done(msgValue, name1, name2, name3, name4, name5,
                                score1, score2, score3, score4, score5,
                                imgname1, imgname2, imgname3,
                                imgurl1, imgurl2, imgurl3,
                                acc, imgacc,
                                logo_namecheck,cate_name
                                )

                    # 秀出metadata與msgKey & msgValue訊息
                    # print('%s-%d-%d : (%s , %s)' % (topic, partition, offset, msgKey, msgValue))

                    print("Model Success")
                    # 步驟6.關掉Consumer實例的連線
                    consumer.commit(asynchronous=False)
                    consumer.close()
                    return print("total done!!!")

            # 異步地執行commit (Async commit)
            if records_pulled:
                consumer.commit()

    except KeyboardInterrupt as e:
        sys.stderr.write('Aborted by user\n')
    except Exception as e:
        sys.stderr.write(str(e))

if __name__ == '__main__':
    while True:
        result = getdata()
        print(result)