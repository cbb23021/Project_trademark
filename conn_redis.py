import redis
from redis import ConnectionPool

# pool = redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
# r = redis.Redis(connection_pool=pool)

r=redis.StrictRedis(host='localhost',port=6379, db=0, decode_responses=True)

def insertredis(email):
    # pool = redis.connectionPool(
    #     host = "localhost",
    #     port = 6379,
    #     decode_responses = True
    # )

    r.set("key", email)

    return 1

def getredis():
    # pool = redis.connectionPool(
    #     host = "localhost",
    #     port = 6379,
    #     decode_responses = True
    # )

    value = r.get("key")
    print(value)
    return value

if __name__ =="__main__":
    email = "test@gmail.com"
    insertredis(email)
    getredis()