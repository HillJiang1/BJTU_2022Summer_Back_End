
from flask import Flask,jsonify,request
import json
from dbCon import DBController
from flask_cors import CORS
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
CORS(app, resources=r'/*')

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

#注册 获取头像
@app.route("/register", methods=['POST'])
def register():
    # json_data = request.json
    # print(json_data)
    data = request.form
    db=DBController()
    realname=data.get('realname')
    sex=data.get('sex')
    email=data.get('email')
    phone=data.get('phone')
    description=data.get('description')
    userid=data.get('userid')
    pasw=data.get('pass')
    code = data.get('code')
    file_obj = request.files.get('file')
    file_name = request.form.get('fileName')
    save_path = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\img' + '\\' + str(file_name)
    # 保存
    file_obj.save(save_path)
    path = "http://127.0.0.1:5000/static/img/" + file_name
    s=db.register(userid,pasw,realname,sex,email,phone,description,code,file_name, path)
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
    data = request.form
    print(data)
    db = DBController()
    wName = data.get('workerName')
    sex = data.get('sex')
    phone = data.get('phone')
    ID = data.get('ID')
    birth = data.get('birthday')
    hire_date = data.get('hire_date')
    des = data.get('des')
    createTime = data.get('createTime')
    file_obj = request.files.get('file')
    file_name = request.form.get('fileName')
    save_path = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\img' + '\\' + str(file_name)
    file_obj.save(save_path)
    path = "http://127.0.0.1:5000/static/img/" + file_name
    status = db.add_worker(wName, sex, phone, ID, birth, hire_date, des, createTime, file_name, path)
    return jsonify(status)

#修改工作人员信息
@app.route("/changeWorker", methods = ['POST'])
def change_worker():
    data = request.get_json()
    print(data)
    db = DBController()
    id = data['id']
    wName = data['workerName']
    sex = data['sex']
    phone = data['phone']
    ID = data['ID']
    birth = data['birthday']
    hire_date = data['hire_date']
    resign_date = data['resign_date']
    des = data['des']
    createTime = data['createTime']
    createName = data['createName']
    file_obj = request.files.get('file')
    file_name = request.form.get('fileName')
    save_path = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\img' + '\\' + str(file_name)
    print(123)
    file_obj.save(save_path)
    path = "http://127.0.0.1:5000/static/img/" + file_name
    status = db.change_worker(id, wName, sex, phone, ID, birth, hire_date, resign_date, des, createTime, createName, file_name, path)
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
    print(data)
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
        img=item[11]
        result.append({'id': id1, 'workerName': workerName, 'sex': sex, 'phone': phone, 'ID':ID, 'birthday':birthday, 'hire_date': hire_date, 'resign_date': resign_date, 'des':des, 'createTime':createTime, 'createName':createName,"image":img,})
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
    data = request.form
    db = DBController()
    vName = data.get('volunteerName')
    sex = data.get('sex')
    phone = data.get('phone')
    ID = data.get('ID')
    birth = data.get('birthday')
    workTime = data.get('workTime')
    hire_date = data.get('hire_date')
    file_obj = request.files.get('file')
    file_name = request.form.get('fileName')
    save_path = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\img' + '\\' + str(file_name)
    file_obj.save(save_path)
    print(123)
    path = "http://127.0.0.1:5000/static/img/" + file_name
    status = db.add_volunteer(vName, sex, phone, ID, birth, workTime,hire_date, file_name, path)
    print(234)
    return jsonify(status)

#修改义工信息
@app.route("/changeVolunteer", methods = ['POST'])
def change_volunteer():
    data = request.form
    db = DBController()
    id = data.get('id')
    vName = data.get('volunteerName')
    sex = data.get('sex')
    phone = data.get('phone')
    ID = data.get('ID')
    birth = data.get('birthday')
    workTime = data.get('workTime')
    file_obj = request.files.get('file')
    file_name = request.form.get('fileName')
    path=' '
    print(file_name)
    if file_name!=None:
        save_path = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\img' + '\\' + str(file_name)
        file_obj.save(save_path)
        path = "http://127.0.0.1:5000/static/img/" + file_name
    else:file_name=' '
    status = db.change_volunteer(id, vName, sex, phone, ID, birth, workTime,file_name,path)
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
    print(data)
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
@app.route("/readRecord", methods = ['GET'])
def read_record():
    db = DBController()
    status = db.read_record()
    print(status)
    result = []
    for item in status:
        id = item[0]
        type = item[1]
        time = item[2].__str__()
        dest = item[3]
        des = item[4]
        old_id = item[5]
        url = item[6]
        result.append({'id':id, 'type':type, 'time':time, 'destination':dest, 'des':des, 'old_id':old_id,'image':url})
    print(result)
    return jsonify(result)

#录入老人信息
@app.route("/addOld", methods=['POST'])
def add_Old():
    data = request.form
    # json_data = json.loads(data)
    db = DBController()
    file_obj = request.files.get('file')
    file_name = request.form.get('fileName')
    oldName = data.get('oldName')
    print(oldName)
    sex = data.get('sex')
    phone = data.get('phone')
    ID = data.get('ID')
    birthday = data.get('birthday')
    date_in = data.get('date_in')
    date_out = data.get('date_out')
    roomNumber = data.get('roomNumber')
    guardian1_name = data.get('guardian1_name')
    guardian1_phone = data.get('guardian1_phone')
    guardian1_wechat = data.get('guardian1_wechat')
    guardian2_name = data.get('guardian2_name')
    guardian2_phone = data.get('guardian2_phone')
    guardian2_wechat = data.get('guardian2_wechat')
    situation = data.get('situation')
    des = data.get('des')
    createTime = data.get('createTime')
    createName = data.get('createName')
    updateTime = data.get('updateTime')
    updateName = data.get('updateName')

    save_path = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\img' + '\\' + str(file_name)
    file_obj.save(save_path)
    path = "http://127.0.0.1:5000/static/img/" + file_name
    s = db.addOld(oldName,sex,phone,ID,birthday,date_in,date_out,roomNumber,guardian1_name,guardian1_phone,guardian1_wechat,guardian2_name,guardian2_phone,guardian2_wechat,situation,des,createTime,createName,updateTime,updateName,file_name,path)
    print(s)
    return s

#修改老人信息
@app.route("/changeOld", methods=['POST'])
def chanegOld():
    db = DBController()
    data = request.get_data()
    json_data = json.loads(data)
    id=json_data['id']
    oldName = json_data['oldName']
    sex = json_data['sex']
    phone =json_data['phone']
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
    file_obj = request.files.get('file')
    file_name = request.form.get('fileName')
    save_path1 = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\img' + '\\' + str(file_name)
    file_obj.save(save_path1)
    path = "http://127.0.0.1:5000/static/img/" + file_name
    s = db.changeOld(id,oldName,sex,phone,ID,birthday,date_in,date_out,roomNumber,guardian1_name,guardian1_phone,guardian1_wechat,guardian2_name,guardian2_phone,guardian2_wechat,situation,des,createTime,createName,updateTime,updateName,file_name, path)
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
    print(data)
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
    # print(request)
    file_obj = request.files.get('file')
    # print(type(file_obj))
    # print(file_obj)
    file_name = request.form
    file1 = file_name.get('fileName')
    data = file_name.get('userid')
    print(data)
    save_path = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\img' + '\\' + str(file1)
    # 保存
    file_obj.save(save_path)
    print(save_path)
    return '图片保存成功'


#上传图片
def get_picture(src):
    picture_data = {
        "file_name": src,
        "url": "http://127.0.0.1:5000/" + src

    }
    return jsonify(picture_data)

@app.route("/analysisImage_old",methods=['GET'])
def analysis_old():
    db = DBController()
    db.analysisImage_old()
    return get_picture("/static/image/oldAna.png")

@app.route("/workerImage",methods=['GET'])
def workerImage():
    db = DBController()
    db.workerImage()
    return get_picture("/static/image/worker.png")

@app.route("/volunteerImage",methods=['GET'])
def volunteerImage():
    db = DBController()
    db.volunteerImage()
    return get_picture("/static/image/volunteer.png")

if __name__ == '__main__':
    app.run()
