from flask import Flask, request, render_template,make_response,Response,session,redirect,url_for
from werkzeug.utils import secure_filename
from flask_bootstrap import Bootstrap
import os
import time
import redis

from datetime import timedelta
from producer import producertest
from conn_redis import insertredis, getredis
from stream_getmongodata import getmongodata

UPLOAD_FOLDER = './static/images/'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_url_path='/static', static_folder='./static')
bootstrap = Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['SECRET_KEY'] = "123" #os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)



# 用來接收從Consumer instance發出的error訊息
def error_cb(err):
    print('Error: %s' % err)

#檢查上傳檔案是否合法的函數
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# login page, create user id
@app.route('/login', methods=['GET'])
def login():
    if request.method =='GET':
        return render_template("genericlogin.html",request_method="get")

# search page
@app.route('/index', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        email = request.form.get("email")
        insertredis(email)

        return render_template("index.html", email=email, request_method="post")

    if request.method == 'GET':
        email = getredis()
        return render_template("index.html", email=email, request_method="get")

@app.route('/genericpre', methods = ['GET','POST'])
def genericpre():
    if request.method == 'POST':

        # get user input data
        email= getredis().replace(".","_")
        logoname = request.form.get("logoname")
        category3 = request.form.get("category3")
        filepath= ""

        # get upload file
        file = request.files['file']
        # check upload file is accepted
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

        # create key:value format
        inputkafkakey=email
        inputlaflavalue={
          "username": email.replace(".","_"),
          "logoname" : logoname,
          "category3" : category3,
          "filepath" : filepath,
          "status":"open"
        }

        # Kafka Producer
        producertest(inputkafkakey, inputlaflavalue)
        return render_template("genericpre.html",request_method="post")

    if request.method == 'GET':
        stream_mongo = getmongodata()
        if stream_mongo == None:
            return render_template("genericpre.html", request_method="get")

        else:
            return redirect(url_for("generic"))

@app.route('/generic', methods = ['GET','POST'])
def generic():
    if request.method == 'GET':
        stream_mongo = getmongodata()
        logoname = stream_mongo["logoname"]
        cate_name = stream_mongo["categoryname"]
        logo_namecheck = stream_mongo["famousname"]
        filepath = stream_mongo["filepath"]
        acc = stream_mongo["wordacc"]
        imgacc = stream_mongo["imgacc"]
        name1 = stream_mongo["name"][0]
        name2 = stream_mongo["name"][1]
        name3 = stream_mongo["name"][2]
        name4 = stream_mongo["name"][3]
        name5 = stream_mongo["name"][4]
        score1 = stream_mongo["score"][0]
        score2 = stream_mongo["score"][1]
        score3 = stream_mongo["score"][2]
        score4 = stream_mongo["score"][3]
        score5 = stream_mongo["score"][4]
        imgname1 = stream_mongo["imgname"][0]
        imgname2 = stream_mongo["imgname"][1]
        imgname3 = stream_mongo["imgname"][2]
        imgurl1 = stream_mongo["imgurl"][0]
        imgurl2 = stream_mongo["imgurl"][1]
        imgurl3 = stream_mongo["imgurl"][2]

        return render_template("generic.html", logoname=logoname, cate_name=cate_name,
                               logo_namecheck=logo_namecheck, filepath=filepath,
                               name1=name1, name2=name2, name3=name3, name4=name4, name5=name5,
                               score1=score1, score2=score2, score3=score3, score4=score4, score5=score5,
                               imgurl1=imgurl1, imgurl2=imgurl2, imgurl3=imgurl3,
                               imgname1=imgname1, imgname2=imgname2, imgname3=imgname3,
                               imgacc=imgacc, acc=acc,
                               request_method="get")

@app.route('/elements', methods = ['GET','POST'])
def elements():
    if request.method =='GET':
        return render_template("elements.html")

@app.route('/home', methods = ['GET','POST'])
def home():
    if request.method =='GET':
        return render_template("old.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
