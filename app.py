from flask import Flask,jsonify,request
import json
from dbCon import DBController
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)

connect = pymysql.connect(host='localhost',  # 本地数据库
                              user='root',
                              password='yourpassword',
                              db='old_care',
                              charset='utf8')  # 服务器名,账户,密码，数据库名称
cursor = connect.cursor()

@app.route('/login', methods=['POST'])
def uni_login():
    status = 0
    # c = connect.connect
    data = request.get_data()
    j_data = json.loads(data)
    # json_data = []
    userid = j_data['userid']
    password = j_data['pass']
    s = "SELECT * FROM sys_user WHERE UserName='{}' AND Password = '{}'".format(userid,password)
    cursor.execute(s)
    result = cursor.fetchall()
    if result:  #账号密码正确
        # print(right)
        status = 1
        # json_data.append(status)

    return jsonify(status)

#修改密码
@app.route('/change_pwd', methods=['POST'])
def change_password():
    status = 0
    data = request.get_data()
    j_data = json.loads(data)
    print(j_data)
    userid = j_data['userid']
    password = j_data['pass']
    update="UPDATE sys_user SET Password= '{}' WHERE UserName = '{}' ".format(password, userid)
    cursor.execute(update)
    # count = cursor.rowcount
    s = "SELECT * FROM sys_user WHERE UserName='{}' ".format(userid)
    cursor.execute(s)
    result = cursor.fetchall()
    print(result)
    pwd = result[0][4]
    print(pwd)
    if pwd == password:
        status = 1
    # s = "SELECT * FROM sys_user WHERE UserName='{}' ".format(userid)
    # cursor.execute(s)
    # result = cursor.fetchall()
    # print(result)
    return jsonify(status)

@app.route("/register", methods=['POST'])
def register():
    # json_data = request.json
    # print(json_data)
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    db=DBController()
    realname=json_data['realname']
    sex=json_data['sex']
    email=json_data['email']
    phone=json_data['phone']
    description=json_data['description']
    userid=json_data['userid']
    pasw=json_data['pass']
    s=db.register(userid,pasw,realname,sex,email,phone,description)
    return s

@app.route("/confirm", methods=['POST'])
def pass_confirm():
    json_data = request.json
    db = DBController()
    userid = json_data['userid']
    pasw = json_data['pass']
    s = db.pass_confirm(userid, pasw)
    return s

if __name__ == '__main__':
    app.run()
