
from flask import Flask,jsonify,request
import json
from dbCon import DBController
from flask_cors import CORS
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
CORS(app, supports_credentials=True)

#登录
@app.route('/login', methods=['POST'])
def uni_login():
    db = DBController()
    status = "0"
    # c = connect.connect
    data = request.get_data()
    j_data = json.loads(data)
    # json_data = []
    userid = j_data['userid']
    password = j_data['pass']
    status = db.login(userid, password)
    return jsonify(status)

#注册
@app.route("/register", methods=['POST'])
def register():
    # json_data = request.json
    # print(json_data)
    data = request.get_data()
    json_data = json.loads(data)
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

#确认密码
@app.route("/confirm", methods=['POST'])
def pass_confirm():
    json_data = json.loads(request.get_data())
    print(json_data)
    db = DBController()
    userid = json_data['userid']
    pasw = json_data['pass']
    s = db.pass_confirm(userid, pasw)
    return s

#修改密码
@app.route('/change_pwd', methods=['POST'])
def change_password():
    db = DBController()
    status = "0"
    data = request.get_data()
    j_data = json.loads(data)
    print(j_data)
    userid = j_data['userid']
    password = j_data['pass']
    status = db.change_password(userid, password)
    return jsonify(status)

#查看管理员个人信息
@app.route("/queryManager",methods=['POST'])
def queryManager():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    id = json_data['userName']
    db = DBController()
    return db.queryManager(id)

#修改管理员个人信息
@app.route('/change',methods=['POST'])
def change():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    db = DBController()
    realname = json_data['realName']
    sex = json_data['sex']
    email = json_data['mail']
    phone = json_data['phone']
    description = json_data['des']
    userid = json_data['userName']
    s = db.change(userid, realname, sex, email, phone, description)
    return s

#录入工作人员信息
@app.route("/addWorker", methods = ['POST'])
def add_worker():
    data = request.get_data()
    print(data)
    json_data = json.loads(data)
    print(json_data)
    db = DBController()
    wName = json_data['workerName']
    sex = json_data['sex']
    phone = json_data['phone']
    ID = json_data['ID']
    birth = json_data['birthday']
    hire_date = json_data['hire_date']
    des = json_data['des']
    createTime = json_data['createTime']
    status = db.add_worker(wName, sex, phone, ID, birth, hire_date, des, createTime)
    return jsonify(status)

#修改工作人员信息
@app.route("/changeWorker", methods = ['POST'])
def change_worker():
    data = request.get_data()
    json_data = json.loads(data)
    db = DBController()
    id = json_data['id']
    wName = json_data['workerName']
    sex = json_data['sex']
    phone = json_data['phone']
    ID = json_data['ID']
    birth = json_data['birthday']
    print(birth)
    hire_date = json_data['hire_date']
    resign_date = json_data['resign_date']
    des = json_data['des']
    createTime = json_data['createTime']
    createName = json_data['createName']
    print(123)
    status = db.change_worker(id, wName, sex, phone, ID, birth, hire_date, resign_date, des, createTime, createName)
    print(234)
    return jsonify(status)

#查询工作人员
@app.route("/queryWorkers", methods = ['POST'])
def query_workers():
    db = DBController()
    status = db.query_workers()#更改名称
    result = []
    for item in status:
        id = item[0]
        workerName = item[1]
        sex = item[2]
        phone = item[3]
        hire_date = item[4].__str__()
        result.append({'id':id, 'workerName':workerName, 'sex':sex, 'phone':phone, 'hire_date':hire_date})
    print(status)
    return jsonify(result)

#查询具体工作人员
@app.route("/queryWorker", methods = ['POST'])
def query_worker():
    data = request.get_data()
    json_data = json.loads(data)
    db = DBController()
    id = json_data['id']
    print(62)
    status = db.query_worker(id)
    print(status)
    result = []
    for item in status:
        id1 = item[0]
        workerName = item[1]
        sex = item[2]
        phone = item[3]
        ID = item[4]
        birthday = item[5].__str__()
        hire_date = item[6].__str__()
        resign_date = item[7].__str__()
        des = item[8]
        createTime = item[9].__str__()
        createName = item[10]
        result.append({'id': id1, 'workerName': workerName, 'sex': sex, 'phone': phone, 'ID':ID, 'birthday':birthday, 'hire_date': hire_date, 'resign_date': resign_date, 'des':des, 'createTime':createTime, 'createName':createName})
    return jsonify(result[0])


#删除工作人员
@app.route("/deleteWorker", methods = ['POST'])
def delete_worker():
    data = request.get_data()
    json_data = json.loads(data)
    db = DBController()
    id = json_data['id']
    print(id)
    status = db.delete_worker(id)
    return status

#录入义工信息
@app.route("/addVolunteer", methods = ['POST'])
def add_volunteer():
    data = request.get_data()
    json_data = json.loads(data)
    db = DBController()
    vName = json_data['volunteerName']
    sex = json_data['sex']
    phone = json_data['phone']
    ID = json_data['ID']
    birth = json_data['birthday']
    workTime = json_data['workTime']
    status = db.add_volunteer(vName, sex, phone, ID, birth, workTime)
    return jsonify(status)

#修改义工信息
@app.route("/changeVolunteer", methods = ['POST'])
def change_volunteer():
    data = request.get_data()
    json_data = json.loads(data)
    db = DBController()
    id = json_data['id']
    vName = json_data['volunteerName']
    sex = json_data['sex']
    phone = json_data['phone']
    ID = json_data['ID']
    birth = json_data['birthday']
    workTime = json_data['workTime']
    status = db.change_volunteer(id, vName, sex, phone, ID, birth, workTime)
    return jsonify(status)

#查询义工
@app.route("/queryVolunteers", methods = ['POST'])
def query_volunteers():
    db = DBController()
    status = db.query_volunteers()#改变name为volunteerName，gender为sex
    result = []
    for item in status:
        id = item[0]
        vName = item[1]
        sex = item[2]
        phone = item[3]
        ID = item[4]
        workTime = item[5]
        result.append({'id':id, 'volunteerName':vName, 'sex':sex, 'phone':phone, 'ID':ID, 'workTime':workTime})
    print(result)
    return jsonify(result)

#查询具体义工信息
@app.route("/queryVolunteer",methods=['POST'])
def queryVolunteer():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    id = json_data['id']
    db = DBController()
    return db.queryVolunteer(id)

#删除义工信息
@app.route("/deleteVolunteer",methods=['POST'])
def deleteVolunteer():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    id = json_data['id']
    print(id)
    db = DBController()
    return db.deleteVolunteer(id)

#读取突发情况记录
@app.route("/readRecord", methods = ['POST'])
def read_record():
    db = DBController()
    status = db.read_record()
    print(status)
    result = []
    for item in status:
        id = item[0]
        type = item[1]
        time = item[2]
        dest = item[3]
        des = item[4]
        old_id = item[5]
        result.append({'id':id, 'type':type, 'time':time, 'destination':dest, 'des':des, 'old_id':old_id})
        return jsonify(result)

#录入老人信息
@app.route("/addOld", methods=['POST'])
def addOld():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    oldName = json_data['oldName']
    sex = json_data['sex']
    phone = json_data['phone']
    ID = json_data['ID']
    birthday = json_data['birthday']
    date_in = json_data['date_in']
    date_out = json_data['date_out']
    roomNumber = json_data['roomNumber']
    guardian1_name = json_data['guardian1_name']
    guardian1_phone = json_data['guardian1_phone']
    guardian1_wechat = json_data['guardian1_wechat']
    guardian2_name = json_data['guardian2_name']
    guardian2_phone = json_data['guardian2_phone']
    guardian2_wechat = json_data['guardian2_wechat']
    situation = json_data['situation']
    des = json_data['des']
    createTime = json_data['createTime']
    createName = json_data['createName']
    updateTime = json_data['updateTime']
    updateName = json_data['updateName']
    db = DBController()
    s = db.addOld(oldName,sex,phone,ID,birthday,date_in,date_out,roomNumber,guardian1_name,guardian1_phone,guardian1_wechat,guardian2_name,guardian2_phone,guardian2_wechat,situation,des,createTime,createName,updateTime,updateName)
    return s

#修改老人信息
@app.route("/changeOld", methods=['POST'])
def chanegOld():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    id=json_data['id']
    oldName = json_data['oldName']
    sex = json_data['sex']
    phone = json_data['phone']
    ID = json_data['ID']
    birthday = json_data['birthday']
    date_in = json_data['date_in']
    date_out = json_data['date_out']
    roomNumber = json_data['roomNumber']
    guardian1_name = json_data['guardian1_name']
    guardian1_phone = json_data['guardian1_phone']
    guardian1_wechat = json_data['guardian1_wechat']
    guardian2_name = json_data['guardian2_name']
    guardian2_phone = json_data['guardian2_phone']
    guardian2_wechat = json_data['guardian2_wechat']
    situation = json_data['situation']
    des = json_data['des']
    createTime = json_data['createTime']
    createName = json_data['createName']
    updateTime = json_data['updateTime']
    updateName = json_data['updateName']
    db = DBController()
    s = db.changeOld(id,oldName,sex,phone,ID,birthday,date_in,date_out,roomNumber,guardian1_name,guardian1_phone,guardian1_wechat,guardian2_name,guardian2_phone,guardian2_wechat,situation,des,createTime,createName,updateTime,updateName)
    return s

#查询老人信息
@app.route("/queryOlds",methods=['POST'])
def quertOlds():
    db=DBController()
    s=db.queryOlds()
    return s

#查询老人具体信息
@app.route("/queryOld",methods=['POST'])
def queryOld():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    id = json_data['id']
    db=DBController()
    return db.queryOld(id)

#删除老人信息
@app.route("/deleteOld",methods=['POST'])
def deleteOld():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    id = json_data['id']
    db = DBController()
    return db.deleteOld(id)

#老年人年龄图
@app.route("/getPicture",methods=['GET'])
def get_Picture():
    return get_picture()

#保存图片
@app.route('/savePicture', methods=['POST'])
def save_picture():
    # import os
    # 图片对象
    file_obj = request.files.get('file')
    print(file_obj)
    # 图片名字
    file_name = request.form.get('fileName')
    # 图片保存的路径
    save_path = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\img' + '\\' + str(file_name)
    # 保存
    file_obj.save(save_path)
    return '图片保存成功'


#上传图片
def get_picture():
    picture_data = {
        "file_name": "2.jpg",
        "url": "http://127.0.0.1:5000/static/img/2.jpg"

    }
    return jsonify(picture_data)


if __name__ == '__main__':
    app.run()
