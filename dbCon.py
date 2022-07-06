import pymysql #导入模块

class DBController:
    def __init__(self):
        self.connect = pymysql.connect(host='localhost',  # 本地数据库
                                  user='root',
                                  password='yourpassword',
                                  db='old_care',
                                  charset='utf8')  # 服务器名,账户,密码，数据库名称
        self.cursor = self.connect.cursor()
    def register(self,name,pasw,rname,sex,email,phone,des):

        try:
            sql = """INSERT INTO sys_user (UserName,Password,REAL_NAME,SEX,EMAIL,PHONE,DESCRIPTION) values(%s,%s,%s,%s,%s,%s,%s)"""
            print(sql)
            values=(name,pasw,rname,sex,email,phone,des)
            self.cursor.execute(sql,values)  # 执行sql语句
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库
            str="1"
        except:
            self.connect.rollback()
            str="0"
        self.cursor.close()  # 关闭游标
        return str
    def pass_confirm(self,name,pasw):
        try:
            sql = """SELECT Password FROM `sys_user` WHERE `UserName`= %s"""
            self.cursor.execute(sql, name)  # 执行sql语句
            res=self.cursor.fetchone()
            print(res,pasw)
            if(res[0]==pasw):
                str="1"
            else:str="0"
            self.connect.commit()  # COMMIT命令用于把事务所做的修改保存到数据库

        except:
            self.connect.rollback()
            str = "0"
        return str
    def close(self):
        self.connect.close()  # 关闭数据库连接