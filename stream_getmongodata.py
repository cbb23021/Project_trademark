from pymongo import MongoClient

# link mongodb
client = MongoClient('localhost', 27017)
db = client['demo']
col = db['kafkadata']



def getmongodata():

    while True:

        # find mongo data
        find_list = list()
        for i in col.find({},{"updatetime":1}).sort("updatetime",1):
            find_list.append(i)

        done_content = col.find_one(find_list[-1])

        if done_content["status"] == "done":
            print("mongo stream")
            print(done_content)
            return done_content
        else:
            return None

if __name__ =="__main__":
    getmongodata()
