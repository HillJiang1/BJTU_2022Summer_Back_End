import pymysql #导入模块
from flask import Flask,jsonify,request
import matplotlib.pyplot as plt
import os

class DBController:
    def __init__(self):
        self.connect = pymysql.connect(host='localhost',  # 本地数据库
                                  user='root',
                                  password='yourpassword',
                                  db='old_care',
                                  charset='utf8')  # 服务器名,账户,密码，数据库名称
        self.cursor = self.connect.cursor()

    #注册
    def register(self,name,pasw,rname,sex,email,phone,des, code, file_name, url):
        find = "SELECT * FROM invite_code WHERE code = '{}'".format(code)
        self.cursor.execute(find)
        result = self.cursor.fetchall()
        if result:
            time = result[0][1] - 1
            if(time > 0):
                insert = "UPDATE invite_code SET degree = '{}' WHERE code = '{}'".format(time, code)
                self.cursor.execute(insert)
                self.connect.commit()
            else:
                delete = "DELETE FROM invite_code WHERE code = '{}'".format(code)
                self.cursor.execute(delete)
                self.connect.commit()
            sql = """INSERT INTO sys_user (UserName,Password,REAL_NAME,SEX,EMAIL,PHONE,DESCRIPTION, imageName, url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            print(sql)
            values = (name, pasw, rname, sex, email, phone, des, file_name, url)
            self.cursor.execute(sql, values)  # 执行sql语句
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
            str = "1"
        else:
            str = "2"
        self.cursor.close()  # 关闭游标
        return str

    # 登录
    def login(self,userid, password):
        print(type(password))
        s = "SELECT *FROM sys_user WHERE UserName = '{}' AND Password = '{}'".format(userid, password)
        self.cursor.execute(s)
        result = self.cursor.fetchall()
        print(result)
        status = []
        if result:
            status.append({'userName':userid, 'realName':result[0][3]})
        else:
            status = "0"
        return status

    #确认密码
    def pass_confirm(self,name,pasw):
        sql = """SELECT Password FROM `sys_user` WHERE `UserName`= %s"""
        self.cursor.execute(sql, name)  # 执行sql语句
        res = self.cursor.fetchone()
        print(res, pasw)
        if (res[0] == pasw):
            str = "1"
        else:
            str = "0"
        self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
        return str


    #修改密码
    def change_password(self, userid, password):
        update = "UPDATE sys_user SET Password= '{}' WHERE UserName = '{}' ".format(password, userid)
        self.cursor.execute(update)
        self.connect.commit()
        # count = cursor.rowcount
        s = "SELECT * FROM sys_user WHERE UserName='{}' ".format(userid)
        self.cursor.execute(s)
        result = self.cursor.fetchall()
        print(result)
        pwd = result[0][2]
        print(pwd)
        if pwd == password:
            status = "1"
        else:
            status = "0"
        return status

    #查询管理员个人信息
    def queryManager(self, userName):
        jdata = []
        try:
            sql = """SELECT REAL_NAME,SEX,EMAIL,PHONE,DESCRIPTION,UserName, url FROM `sys_user` WHERE UserName= %s """
            self.cursor.execute(sql, userName)  # 执行sql语句
            res = self.cursor.fetchall()
            print(res)

            for row in res:
                result = {}
                realname = row[0].replace(" ", "")
                sex = row[1].replace(" ", "")
                email = row[2].replace(" ", "")
                phone = row[3].replace(" ", "")
                description = row[4].replace(" ", "")
                userName = row[5].replace(" ", "")
                url = row[6]
                print(userName)
                result['realName'] = realname
                result['sex'] = sex
                result['mail'] = email
                result['phone'] = phone
                result['des'] = description
                result['userName'] = userName

                result['image'] = url

                jdata.append(result)
            print(jdata)
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
            str = "1"
        except:
            self.connect.rollback()
            str = "0"
        return jsonify(jdata[0])

    #修改管理员个人信息
    def change(self, userid, realname, sex, email, phone, description,imageName,url):
        try:
            str = '0'
            sql = """UPDATE sys_user SET REAL_NAME=%s,SEX=%s,EMAIL=%s,PHONE=%s,DESCRIPTION=%s,imageName=%s,url=%s WHERE UserName=%s"""
            print(sql)
            values = (realname, sex, email, phone, description,imageName, url ,userid )
            print(values)
            self.cursor.execute(sql, values)  # 执行sql语句
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
            str = "1"
        except:
            self.connect.rollback()
            str = "0"
        # self.cursor.close()  # 关闭游标
        # self.connect.close()  # 关闭数据库连接
        return str

    #录入工作人员信息
    def add_worker(self, wName, sex,phone, ID, birth, hire_date, des, createTime,file_name, url):
        select = "SELECT * FROM employee_info WHERE id_card = '{}'".format(ID)
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        if result:
            status = "0"
        else:
            sql = "INSERT INTO employee_info (username, gender, phone, id_card, birthday, hire_date, DESCRIPTION, CREATED,imgset_dir, profile_photo) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}','{}','{}')".format(
            wName, sex, phone, ID, birth, hire_date, des, createTime,file_name, url)
            self.cursor.execute(sql)
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
            status = "1"
        return status

    #修改工作人员信息
    def change_worker(self, id, wName, sex,phone, ID, birth, hire_date,resign_date, des, createTime, createName, file_name, url):
        update = "UPDATE employee_info SET gender = '{}' , username = '{}' , phone = '{}' , id_card = '{}' , birthday = '{}' , hire_date = '{}' , resign_date = '{}' , DESCRIPTION = '{}' , CREATED = '{}' , CREATEBY = '{}',  imgset_dir = '{}', profile_photo = '{}' WHERE id = '{}'".format(sex, wName, phone, ID, birth, hire_date, resign_date, des, createTime, createName, file_name, url, id)
        self.cursor.execute(update)
        self.connect.commit()
        status = "1"
        return status

    #查询工作人员
    def query_workers(self):
        select = "SELECT id, username, gender, phone, hire_date FROM employee_info"
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        return result

    #查询具体工作人员
    def query_worker(self, id):
        select = "SELECT id, username, gender, phone, id_card, birthday, hire_date, resign_date, DESCRIPTION, CREATED, CREATEBY, profile_photo FROM employee_info WHERE id = '{}'".format(id)
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        return result

    #删除工作人员
    def delete_worker(self, id):
        delete = "DELETE FROM employee_info WHERE id = '{}'".format(id)
        self.cursor.execute(delete)
        self.connect.commit()
        status = "1"
        return status

    #录入义工信息
    def add_volunteer(self, vName, sex, phone, ID, birth, workTime,hire_date, file_name, url):
        select = "SELECT * FROM volunteer_info WHERE id_card = '{}'".format(ID)
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        if result:
            status = "0"
        else:
            add = "INSERT INTO volunteer_info (name, gender, phone, id_card, birthday, workTime,checkin_date, imgset_dir, profile_photo) values('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(vName, sex, phone, ID, birth, workTime,hire_date, file_name, url)
            self.cursor.execute(add)
            self.connect.commit()
            status = "1"
        return status

    #修改义工信息
    def change_volunteer(self, id, vName, sex, phone, ID, birth, workTime,file_name, url):
        update = "UPDATE volunteer_info SET name = '{}' , gender = '{}' , phone = '{}'  , birthday = '{}' , workTime = '{}'  , imgset_dir = '{}', profile_photo = '{}' WHERE id = '{}'".format(vName, sex, phone,  birth, workTime, file_name, url, id)
        self.cursor.execute(update)
        self.connect.commit()
        status = "1"
        return status

    #查询义工
    def query_volunteers(self):
        select = "SELECT id, name, gender, phone, workTime FROM volunteer_info"
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        return result

    # 查询义工具体信息
    def queryVolunteer(self, id):
        json_data = []
        try:
            sql = """SELECT id,name,gender,phone,id_card,birthday,workTime,checkin_date,checkout_date,profile_photo FROM `volunteer_info` WHERE id=%s """
            self.cursor.execute(sql, id)  # 执行sql语句
            res = self.cursor.fetchall()
            print(res)

            for row in res:
                result = {}
                id = row[0]
                username = row[1]
                gender = row[2]
                phone = row[3]
                id_card = row[4]
                birthday = row[5].__str__()
                worktime = row[6]
                hire_date = row[7].__str__()
                resign_date = row[8].__str__()
                profile_photo = row[9]
                print(1)
                result['id'] = id
                result['volunteerName'] = username
                result['sex'] = gender
                result['phone'] = phone
                result['ID'] = id_card
                result['birthday'] = birthday
                result['workTime'] = worktime
                result['hire_date'] = hire_date
                result['resign_date'] = resign_date
                result['image'] = profile_photo

                json_data.append(result)
            print(json_data)
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
            str = "1"
        except:
            self.connect.rollback()
            str = "0"
        return jsonify(json_data[0])

    #删除义工信息
    def deleteVolunteer(self, id):
        try:
            str = '0'
            sql = """DELETE FROM volunteer_info WHERE id=%s"""
            print(sql)
            values = (id)
            self.cursor.execute(sql, values)  # 执行sql语句
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
            str = "1"
        except:
            self.connect.rollback()
            str = "0"
        return str

    #读取突发情况记录
    def read_record(self):
        select = "SELECT id, event_type, event_date, event_location, event_desc, oldperson_id,url  FROM event_info"
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        print(result)
        return result

    #录入老人信息
    def addOld(self, oldName, sex, phone, ID, birthday, date_in, date_out, roomNumber, guardian1_name,
                   guardian1_phone, guardian1_wechat, guardian2_name, guardian2_phone, guardian2_wechat, situation, des,
                   createTime, createName, updateTime, updateName,file_name, url):
        try:
            sql = """INSERT into oldperson_info(username,gender,phone,id_card,birthday,checkin_date,room_number,firstguardian_name,firstguardian_phone,firstguardian_wechat,secondguardian_name,secondguardian_phone,secondguardian_wechat,health_state,DESCRIPTION,CREATED,CREATEBY,UPDATED,UPDATEBY,imgset_dir, profile_photo)
    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            print(sql)
            values = (
                    oldName, sex, phone, ID, birthday, date_in, roomNumber, guardian1_name, guardian1_phone,
                    guardian1_wechat, guardian2_name, guardian2_phone, guardian2_wechat, situation, des, createTime,
                    createName, updateTime, updateName,file_name, url)
            # values = (
            #     'zhang','male','234212321','1231313213211221','2002-02-10','2002-02-20','2002-03-30','202','chua','1232123131','312313131','eqwq','23131313132','31312132','health','dasadasda','2002-01-20','111','2005-04-23','111')

            self.cursor.execute(sql, values)  # 执行sql语句
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
            str = "1"
        except:
            self.connect.rollback()
            str = "0"
            # self.cursor.close()  # 关闭游标
            # self.connect.close()  # 关闭数据库连接
        return str

    #修改老人信息
    def changeOld(self, id, oldName, sex, phone, ID, birthday, date_in, date_out, roomNumber, guardian1_name,
                      guardian1_phone, guardian1_wechat, guardian2_name, guardian2_phone, guardian2_wechat, situation,
                      des, createTime, createName, updateTime, updateName,file_name, url):
        try:
            str = '0'
            sql = """UPDATE oldperson_info SET username=%s,gender=%s,phone=%s,id_card=%s,birthday=%s,checkin_date=%s,checkout_date=%s,room_number=%s,firstguardian_name=%s,firstguardian_phone=%s,firstguardian_wechat=%s,secondguardian_name=%s,secondguardian_phone=%s,secondguardian_wechat=%s,health_state=%s,DESCRIPTION=%s,CREATED=%s,CREATEBY=%s,UPDATED=%s,UPDATEBY=%s,imgset_dir=%s, profile_photo=%s WHERE id=%s"""
            print(sql)
            values = (
                oldName, sex, phone, ID, birthday, date_in, date_out, roomNumber, guardian1_name, guardian1_phone,
                guardian1_wechat, guardian2_name, guardian2_phone, guardian2_wechat, situation, des, createTime,
                createName, updateTime, updateName,file_name,url, id)
            self.cursor.execute(sql, values)  # 执行sql语句
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
            str = "1"
        except:
            self.connect.rollback()
            str = "0"
            # self.cursor.close()  # 关闭游标
            # self.connect.close()  # 关闭数据库连接
        print(str)
        return str

    #查询老人信息
    def queryOlds(self):
        print("res")
        try:
            sql = """SELECT id,username,gender,phone,room_number,firstguardian_phone FROM `oldperson_info` """
            self.cursor.execute(sql)  # 执行sql语句
            res=self.cursor.fetchall()
            json_data=[]
            for row in res:
                print(row)
                result={}
                id=row[0]
                username=row[1].replace(" ", "")
                gender = row[2].replace(" ", "")
                phone = row[3].replace(" ", "")
                room_number = row[4].replace(" ", "")
                firstguardian_phone = row[5].replace(" ", "")
                result['id']=id
                result['oldName']=username
                result['sex']=gender
                result['phone']=phone
                result['roomNumber']=room_number
                result['guardian1_phone']=firstguardian_phone
                print(result)
                json_data.append(result)
            print(json_data)
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
        except:
            self.connect.rollback()

        return jsonify(json_data)

    # 查询老人具体信息
    def queryOld(self, id):
        print("res")
        try:
            sql = """SELECT * FROM `oldperson_info` WHERE id=%s """
            self.cursor.execute(sql, id)  # 执行sql语句
            res = self.cursor.fetchall()
            print(res)
            json_data = []
            for row in res:
                result = {}
                id = row[0]
                username = row[1].replace(" ", "")
                gender = row[2].replace(" ", "")
                phone = row[3].replace(" ", "")
                id_card = row[4].replace(" ", "")
                birthday = row[5].__str__()
                checkin_date = row[6].__str__()
                checkout_date = row[7].__str__()
                img = row[9]
                room_number = row[10].replace(" ", "")
                firstguardian_name = row[11].replace(" ", "")
                firstguardian_phone = row[13].replace(" ", "")
                firstguardian_wechat = row[14].replace(" ", "")
                secondguardian_name = row[15].replace(" ", "")
                secondguardian_phone = row[17].replace(" ", "")
                secondguardian_wechat = row[18].replace(" ", "")
                health_state = row[19].replace(" ", "")
                description = row[20].replace(" ", "")
                created = row[22].__str__()
                createby = row[23].replace(" ", "")
                updated = row[24].__str__()
                updateby = row[25].replace(" ", "")

                result['id'] = id
                result['oldName'] = username
                result['sex'] = gender
                result['phone'] = phone
                result['ID'] = id_card
                result['birthday'] = birthday
                result['date_in'] = checkin_date
                result['date_out'] = checkout_date
                result['image'] = img
                result['roomNumber'] = room_number
                result['guardian1_name'] = firstguardian_name
                result['guardian1_phone'] = firstguardian_phone
                result['guardian1_wechat'] = firstguardian_wechat
                result['guardian2_name'] = secondguardian_name
                result['guardian2_phone'] = secondguardian_phone
                result['guardian2_wechat'] = secondguardian_wechat
                result['situation'] = health_state
                result['des'] = description
                result['createTime'] = created
                result['createName'] = createby
                result['updateTime'] = updated
                result['updateName'] = updateby
                json_data.append(result)
            print(json_data)
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
            str = "1"
        except:
            self.connect.rollback()
            str = "0"
        return jsonify(json_data[0])

    #删除老人信息
    def deleteOld(self,id):
        try:
            str = '0'
            sql = """DELETE FROM oldperson_info WHERE id=%s"""
            print(sql)
            values = (id)
            self.cursor.execute(sql, values)  # 执行sql语句
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
            str = "1"
        except:
            self.connect.rollback()
            str = "0"
        # self.cursor.close()  # 关闭游标
        # self.connect.close()  # 关闭数据库连接
        return str

    def analysisImage_old(self):
        sql = """select
    Sum(Case When 年龄 <=60 Then 1 Else 0 End) As '1',
    Sum(Case When 年龄 Between 60 And 65 Then 1 Else 0 End) As '2',
    Sum(Case When 年龄 Between 65 And 70 Then 1 Else 0 End) As '3',
    Sum(Case When 年龄 Between 70 And 75 Then 1 Else 0 End) As '4',
    Sum(Case When 年龄 Between 75 And 80 Then 1 Else 0 End) As '5',
    Sum(Case When 年龄 >=80 Then 1 Else 0 End) As '6'
    From
    (
    SELECT *, ROUND(DATEDIFF(CURDATE(), birthday)/365.2422)  AS '年龄' FROM oldperson_info
    ) s ;"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        # y1 = self.cursor.fetchone()  # 获取sql数据

        x = ("60岁以下", "60-65岁", "65-70岁", "70-75岁", "75-80岁", "80岁以上")
        plt.bar(x, rows[0])
        plt.title("年龄分析")
        plt.xlabel("年龄段")
        plt.ylabel("人数")
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=5, labels=['年龄段'])
        plt.rcParams['font.sans-serif'] = ['SimHei']
        save_path = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\image' + '\\oldAna.png'
        plt.savefig(save_path)
        plt.show()

    def workerImage(self):
        sql = """select COUNT(id),MONTH(hire_date) as month from employee_info where hire_date>'2020-01-01' AND hire_date<'2020-12-31'group by month order by month ASC"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        print(rows)
        y1 = []
        j = 0
        for x in range(1, 13):
            if ((j < len(rows) and (rows[j][1] == x))):
                print(j)
                y1.append(rows[j][0])
                j = j + 1
            else:
                y1.append(0)
        sql = """select COUNT(id),MONTH(resign_date) as month from employee_info where resign_date>'2020-01-01' AND resign_date<'2020-12-31'group by month order by month ASC"""
        self.cursor.execute(sql)
        rows1 = self.cursor.fetchall()
        y2 = []
        j = 0
        for x in range(1, 13):
            if ((j < len(rows1) and (rows1[j][1] == x))):
                print(j)
                y2.append(rows1[j][0])
                j = j + 1
            else:
                y2.append(0)
        print(y1)
        x = ("一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月")
        plt.plot(x, y1, label="入职人数")
        plt.plot(x, y2, label="离职人数")
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=5, labels=['入职人数', '离职人数'])
        plt.rcParams['font.sans-serif'] = ['SimHei']
        save_path = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\image' + '\\worker.png'
        plt.savefig(save_path)
        plt.show()

    def volunteerImage(self):
        sql = """select COUNT(id),MONTH(checkin_date) as month from volunteer_info where checkin_date>'2020-01-01' AND checkin_date<'2020-12-31'group by month order by month ASC"""
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        print(rows)
        y1 = []
        j = 0
        for x in range(1, 13):
            if ((j < len(rows) and (rows[j][1] == x))):
                print(j)
                y1.append(rows[j][0])
                j = j + 1
            else:
                y1.append(0)
        sql = """select COUNT(id),MONTH(checkout_date) as month from volunteer_info where checkout_date>'2020-01-01' AND checkout_date<'2020-12-31'group by month order by month ASC"""
        self.cursor.execute(sql)
        rows1 = self.cursor.fetchall()
        y2 = []
        j = 0
        for x in range(1, 13):
            if ((j < len(rows1) and (rows1[j][1] == x))):
                print(j)
                y2.append(rows1[j][0])
                j = j + 1
            else:
                y2.append(0)
        print(y1)
        x = ("一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月")
        plt.plot(x, y1, label="入职人数")
        plt.plot(x, y2, label="离职人数")
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.03), fancybox=True, ncol=5, labels=['入职人数', '离职人数'])
        plt.rcParams['font.sans-serif'] = ['SimHei']
        save_path = os.path.abspath(os.path.dirname(__file__) + '\\static') + '\\image' + '\\volunteer.png'
        plt.savefig(save_path)
        plt.show()

    def roomRecord(self):
        select = "select * from room_info"
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        return result

    def corridorRecord(self):
        select = "select * from corridor_info"
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        return result

    def deskRecord(self):
        select = "select * from desk_info"
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        return result

    def yardRecord(self):
        select = "select * from yard_info"
        self.cursor.execute(select)
        result = self.cursor.fetchall()
        return result

    def queryHolidays(self):
        try:
            sql = """SELECT day(date),title FROM `calendar` """
            self.cursor.execute(sql)  # 执行sql语句
            res = self.cursor.fetchall()
            json_data = []
            for row in res:
                print(row)
                result = {}
                id = row[0].__str__()
                title = row[1].replace(" ", "")
                result['date'] = id
                result['name'] = title
                print(result)
                json_data.append(result)
            print(json_data)
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
        except:
            self.connect.rollback()
        print(json_data)
        return jsonify(json_data)

    def addHoliday(self, id, title):
        sql = """INSERT into calendar(date,title)
        values (%s,%s)"""
        print(sql)
        values = (id, title)
        self.cursor.execute(sql, values)  # 执行sql语句
        self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
        str = "1"

        return str

    def close(self):
        self.connect.close()  # 关闭数据库连接