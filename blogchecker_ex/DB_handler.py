import datetime
from flask import redirect, url_for
import pyrebase
import json
from werkzeug.security import generate_password_hash, check_password_hash

class DBModule:

    def __init__(self):
        with open("./auth/firebaseAuth.json") as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()

    def login(self, id, pwd):
        users = self.db.child("users").get().val()
        try:
            userinfo = users[id]
            # pwd = userinfo["pwd"]
            pwdcheck = check_password_hash(userinfo["pwd"], pwd)
            if pwdcheck == True:
                return True
            else:
                return False
        except:
            return False

    def signup_verification(self, id):
        users = self.db.child("users").get().val()
        for i in users:
            if id == i:
                return False
        return True

    def signup(self, id, pwd_hash, name, blogid, tel, startdate, useday, token):
        information = {
            "pwd": pwd_hash,
            "name":name,
            "blogid":blogid,
            "tel":tel,
            "startdate":startdate,
            "useday":useday,
            "token":token
        }

        if self.signup_verification(id):
            self.db.child("users").child(id).set(information)
            return True
        else:
            return False

    def index(self, id):
        users = self.db.child("users").get().val()
        try:
            userinfo = users[id]
            # useday와 startdate, DB에서 불러오기
            useday = userinfo["useday"]
            startdate = userinfo["startdate"]
            # print(useday)
            # print(startdate)
            # 현재 시간 불러오기
            now_date = datetime.datetime.now()

            # DB, str 시간 date로 바꾸기
            startdate_date = datetime.datetime.strptime(startdate, '%y%m%d')
            # print(startdate_date)
            # date에 로그인 한 날짜에서 빼기
            day = now_date - startdate_date
            # 날짜를 일 단위로 변경
            passday = day.days
            # print(passday)
            if passday < useday:
                return True
            else:
                return False
        except:
            return False

    def pay(self, startdate, useday, id):
        self.db.child("users").child(id).update({"startdate": startdate, "useday": useday})

    def token(self, token, id):
        self.db.child("users").child(id).update({"token": token})

    def tokencheck(self, token, id):
        users = self.db.child("users").get().val()
        userinfo = users[id]
        usertoken = userinfo["token"]
        if token==usertoken:
            return True
        else:
            return False