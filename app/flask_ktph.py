# -*- coding: utf-8 -*-
# @Author: Kivin1
# @Date:   2018-02-13 16:48:34
# @Last Modified by:   Kivin1
# @Last Modified time: 2018-03-29 10:20:24
import flask
import time
from flask import render_template,request,redirect,url_for,flash
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flaskext.mysql import MySQL


import os
from flask_wtf.csrf import CsrfProtect
from models import User
import forms as forms
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
import numpy as np

app = flask.Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager(app)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'ktph_admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ktph_admin'
app.config['MYSQL_DATABASE_DB'] = 'KTPH' 
app.config['MYSQL_DATABASE_HOST'] = 'ktphdatabase.ct4c3hj4sn6o.ap-southeast-1.rds.amazonaws.com'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)

# csrf protection
csrf = CsrfProtect()
csrf.init_app(app)

month = time.strftime("%b")
# li_select1 = [month]
# li_select2 = [month]
# li_select3 = [month]


ip_tables = ["KTPHIP_1117DATA","KTPHIP_1217DATA","KTPHIP_0118DATA",]
op_tables = ["KTPHOP_1117DATA","KTPHOP_1217DATA","KTPHOP_0118DATA",]
legend1 = 'Top-box'
legend2 = 'Middle-box'
legend3 = 'Bottom-box'



def query_user(username):
    sql = "SELECT * FROM KTPH.User;"
    cursor.execute(sql)
    for i in cursor:
        print("i",i)
        if i[0] == username:
            # print("i[0]",i[0])
            return i

# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_user(username):
    if query_user(username) is not None:
        curr_user = User()
        curr_user.id = username
        return curr_user


# test method
@app.route('/',methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():

        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        sql = "SELECT * FROM KTPH.User;"
        cursor.execute(sql)
        for i in cursor:
            # user = User(i[0],i[1])
            # hash_na = generate_password_hash(i[0])
            # print("i[1]",i[1])
            hash_pa = generate_password_hash(password)
            if check_password_hash(hash_pa,i[1]):
                curr_user = User()
                curr_user.id = user_name
                login_user(curr_user, remember=remember_me)
                return redirect(url_for('render_index'))

            flash('Wrong username or password!')
    return render_template("signin.html", title="Sign In", form=form)


def getLabelsDepartments():
    labels = []
    in_departments = []
    out_departments = []
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for i in ip_tables:
        labels.append(month[int(i[-8:-6])-1]+" "+i[-6:-4])

        department = getDepartments("select distinct Ward from KTPH."+i)
        in_departments.append(set(department))

    for i in op_tables:
        department = getDepartments("select distinct Clinic from KTPH."+i)
        out_departments.append(set(department))

    in_s = in_departments[0]
    for i in in_departments:
        in_s = in_s.intersection(i)

    out_s = out_departments[0]
    for i in out_departments:
        out_s = out_s.intersection(i)


    return labels, in_s,out_s

@app.route('/home',methods=['GET', 'POST'])
def render_index():
    hour = time.strftime("%H")
    month = time.strftime("%b")
    day = time.strftime("%e")
    ti = time.strftime("%H:%M")

    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    intop_boxs = []
    inmiddle_boxs = []
    inbottom_boxs = []
    outtop_boxs = []
    outmiddle_boxs = []
    outbottom_boxs = []

    for i in ip_tables:
        
        OverallExperience = getRatings("select A1 from KTPH."+i)
        
        top_box,middle_box,bottom_box = trans_scale(OverallExperience)
        intop_boxs.append(top_box)
        inmiddle_boxs.append(middle_box)
        inbottom_boxs.append(bottom_box)

    for i in op_tables:
        OverallExperience = getRatings("select A1 from KTPH."+i)    
       
        
        top_box,middle_box,bottom_box = trans_scale(OverallExperience)
        outtop_boxs.append(top_box)
        outmiddle_boxs.append(middle_box)
        outbottom_boxs.append(bottom_box)

    labels, in_s,out_s = getLabelsDepartments()

    feedback,feedback_ratio = getCollectedFeedback()
    data = {
        "feedback":feedback,
        "feedback_ratio":feedback_ratio,
        "hour":hour,
        "day":day,
        "ti":ti,
        "indepartments":in_s,
        "outdepartments":out_s,
        "intop": [intop_boxs[-1],1-intop_boxs[-1]],
        "instr_top":convertfloat_str(intop_boxs[-1]),
        "inmiddle": [inmiddle_boxs[-1],1-inmiddle_boxs[-1]],
        "instr_middle": convertfloat_str(inmiddle_boxs[-1]),
        "inbottom": [inbottom_boxs[-1],1-inbottom_boxs[-1]],
        "instr_bottom": convertfloat_str(inbottom_boxs[-1]),
        "intops":intop_boxs,
        "inmiddles":inmiddle_boxs,
        "inbottoms":inbottom_boxs,

        "outtop": [outtop_boxs[-1],1-outtop_boxs[-1]],
        "outstr_top":convertfloat_str(outtop_boxs[-1]),
        "outmiddle": [outmiddle_boxs[-1],1-outmiddle_boxs[-1]],
        "outstr_middle": convertfloat_str(outmiddle_boxs[-1]),
        "outbottom": [outbottom_boxs[-1],1-outbottom_boxs[-1]],
        "outstr_bottom": convertfloat_str(outbottom_boxs[-1]),
        "outtops":outtop_boxs,
        "outmiddles":outmiddle_boxs,
        "outbottoms":outbottom_boxs,
        "mons":labels,
        "legend1":"Top-box",
        "legend2":"Middle-box",
        "legend3": "Bottom-box",
    }

    if request.method == "POST":
        select1 = request.form.get("select_index1", None)
        print("select1",select1)
        if select1!=None:
            select = "%02d" % (month.index(select1.split(" ")[0])+1)
            print("select",select)
            for i in ip_tables:
                if select == i[-8:-6]:
                    ip_OverallExperience = getRatings("select A1 from KTPH."+i)
                    ip_top_box,ip_middle_box,ip_bottom_box = trans_scale(ip_OverallExperience)
                    return_select = select1+" "+i[-6:-4]
                    

            for i in op_tables:
                if select == i[-8:-6]:
                    op_OverallExperience = getRatings("select A1 from KTPH."+i)
                    op_top_box,op_middle_box,op_bottom_box = trans_scale(op_OverallExperience)
            
            data = {
            "feedback":feedback,
            "hour":hour,
            "day":day,
            "ti":ti,
            "indepartments":in_s,
            "outdepartments":out_s,
            "intop": [ip_top_box,1-ip_top_box],
            "instr_top":convertfloat_str(ip_top_box),
            "inmiddle": [ip_middle_box,1-ip_middle_box],
            "instr_middle": convertfloat_str(ip_middle_box),
            "inbottom": [ip_bottom_box,1-ip_bottom_box],
            "instr_bottom": convertfloat_str(ip_bottom_box),
            "intops":intop_boxs,
            "inmiddles":inmiddle_boxs,
            "inbottoms":inbottom_boxs,

            "outtop": [op_top_box,1-op_top_box],
            "outstr_top":convertfloat_str(op_top_box),
            "outmiddle": [op_middle_box,1-op_middle_box],
            "outstr_middle": convertfloat_str(op_middle_box),
            "outbottom": [op_bottom_box,1-op_bottom_box],
            "outstr_bottom": convertfloat_str(op_bottom_box),
            "outtops":outtop_boxs,
            "outmiddles":outmiddle_boxs,
            "outbottoms":outbottom_boxs,
            "mons":labels,
            "legend1":"Top-box",
            "legend2":"Middle-box",
            "legend3": "Bottom-box",
    }


            return render_template("index.html", select1= return_select,result = data,username=current_user.get_id())
      

    # if request.method == "POST":
    #     select1 = request.form.get("select_index1", None)
    #     select2 = request.form.get("select_index2", None)
    #     select3 = request.form.get("select_index3", None)
    #     print("select1",select1)
    #     print("select2",select2)
    #     print("select3",select3)
    #     if select1!=None:
    #         li_select1.append(select1)
    #         return render_template("index.html", select1= li_select1[-1],select2 = li_select2[-1], select3 = li_select3[-1],result = data,username=current_user.get_id())
    #     if select2!=None:
    #         li_select2.append(select2)
    #         return render_template("index.html", select1= li_select1[-1],select2 = li_select2[-1], select3 = li_select3[-1],result = data,username=current_user.get_id())
    #     if select3!=None:
    #         li_select3.append(select3)
    #         return render_template("index.html", select1= li_select1[-1],select2 = li_select2[-1], select3 = li_select3[-1],result = data,username=current_user.get_id())
    
    return render_template('index.html',result = data,select1= labels[-1],select2=month,select3=month,username=current_user.get_id())


    

def getRatings(sql):  
    cursor.execute(sql)
    ratings = [] 
    for i in cursor:

        ratings.extend(i)
    print("ratings",ratings)
    return ratings

def getDepartments(sql):
    cursor.execute(sql)
    departments = []
    for i in cursor:
        departments.append(i[0])
    return departments





    # mons,departments = render_month_department()
    # legend1 = 'Top-box'
    # legend2 = 'Middle-box'
    # legend3 = 'Bottom-box'

    # in_top, str_top, in_middle, str_middle, in_bottom, str_bottom = render_home_inpatient(month)
    # tops, middles, bottoms = home_inpatient_chart(mons)
    # feedback = feedback_collected(month)
    # # print(tops)
    # # print(middles)
    # # print(bottoms)
    # data = {
    #     "feedback":feedback,
    #     "hour":hour,
    #     "day":day,
    #     "ti":ti,
    #     "departments":departments,
    #     "intop": in_top,
    #     "str_top":str_top,
    #     "inmiddle": in_middle,
    #     "str_middle": str_middle,
    #     "inbottom": in_bottom,
    #     "str_bottom": str_bottom,
    #     "tops":tops,
    #     "middles":middles,
    #     "bottoms":bottoms,
    #     "mons":mons,
    #     "legend1":legend1,
    #     "legend2":legend2,
    #     "legend3": legend3,
    # }
    # if request.method == "POST":
    #     select1 = request.form.get("select_index1", None)
    #     select2 = request.form.get("select_index2", None)
    #     select3 = request.form.get("select_index3", None)
    #     print("select1",select1)
    #     print("select2",select2)
    #     print("select3",select3)
    #     if select1!=None:
    #         li_select1.append(select1)
    #         return render_template("index.html", select1= li_select1[-1],select2 = li_select2[-1], select3 = li_select3[-1],result = data,username=current_user.get_id())
    #     if select2!=None:
    #         li_select2.append(select2)
    #         return render_template("index.html", select1= li_select1[-1],select2 = li_select2[-1], select3 = li_select3[-1],result = data,username=current_user.get_id())
    #     if select3!=None:
    #         li_select3.append(select3)
    #         return render_template("index.html", select1= li_select1[-1],select2 = li_select2[-1], select3 = li_select3[-1],result = data,username=current_user.get_id())

    # return render_template('index.html',result = data,select1= month,select2=month,select3=month,username=current_user.get_id())


# @app.route('/home',methods=['POST'])
# def render_index1():
#     hour = time.strftime("%H")
#     month = time.strftime("%b")
#     day = time.strftime("%e")
#     ti = time.strftime("%H:%M")

#     mons,departments = render_month_department()
#     legend1 = 'Top-box'
#     legend2 = 'Middle-box'
#     legend3 = 'Bottom-box'

#     in_top, str_top, in_middle, str_middle, in_bottom, str_bottom = render_home_inpatient(month)
#     tops, middles, bottoms = home_inpatient_chart(mons)
#     feedback = feedback_collected(month)
#     # print(tops)
#     # print(middles)
#     # print(bottoms)
#     data = {
#         "feedback":feedback,
#         "hour":hour,
#         "day":day,
#         "ti":ti,
#         "departments":departments,
#         "intop": in_top,
#         "str_top":str_top,
#         "inmiddle": in_middle,
#         "str_middle": str_middle,
#         "inbottom": in_bottom,
#         "str_bottom": str_bottom,
#         "tops":tops,
#         "middles":middles,
#         "bottoms":bottoms,
#         "mons":mons,
#         "legend1":legend1,
#         "legend2":legend2,
#         "legend3": legend3,

#     }
#     select1 = request.form.get("select_index1", None)
#     select2 = request.form.get("select_index2", None)
#     select3 = request.form.get("select_index3", None)
   
#     print("select1",select1)
#     print("select2",select2)
#     print("select3",select3)
#     if select1!=None:
#         li_select1.append(select1)
#         return render_template("index.html", select1= li_select1[-1],select2 = li_select2[-1], select3 = li_select3[-1],result = data,username=current_user.get_id())
#     if select2!=None:
#         li_select2.append(select2)
#         return render_template("index.html", select1= li_select1[-1],select2 = li_select2[-1], select3 = li_select3[-1],result = data,username=current_user.get_id())
#     if select3!=None:
#         li_select3.append(select3)
#         return render_template("index.html", select1= li_select1[-1],select2 = li_select2[-1], select3 = li_select3[-1],result = data,username=current_user.get_id())



# def render_month_department():
#     # month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#     sql = "SELECT DISTINCT month_id,department_month_ratings.﻿Month FROM inpatient.department_month_ratings order by month_id"
#     cursor.execute(sql)
#     mons = []
#     for i in cursor:
#         mons.append(i[1])
#     departments = []
#     sql = "SELECT DISTINCT Department FROM inpatient.department_month_ratings;"
#     cursor.execute(sql)
#     for i in cursor:
#         departments.append(i[0])
#     return mons,departments


def convertstr_float(str):
    fl = (float(str.strip('%'))/100)
    return fl

def convertfloat_str(float):
    str = "%.2f%%" % (100*float)
    return str


def getCollectedFeedback():
    feedback = []
    feedback_ratio = []
    sum = 0
    for index in range(0,len(ip_tables)):
        ipsql = "SELECT count(*) FROM KTPH."+ip_tables[index]
        opsql = "SELECT count(*) FROM KTPH."+op_tables[index]
      
        cursor.execute(ipsql)
        ipresults = cursor.fetchall()

        cursor.execute(opsql)
        opresults = cursor.fetchall()
      
        feedback.append([ipresults[0][0],opresults[0][0]])
        sum+=ipresults[0][0]+opresults[0][0]
    for i in feedback:
        feedback_ratio.append([convertfloat_str(i[0]/sum),convertfloat_str(i[1]/sum)])
    print("feedback........",feedback)
    return feedback,feedback_ratio



# @app.route('/A&E_inpatient')
# @login_required
# def renderInpatientAE():
#     mons, departments = render_month_department()
#     report = render_report('A&E')
#     legend1 = 'Top-box'
#     legend2 = 'Middle-box'
#     legend3 = 'Bottom-box'
#     data = {
#         "legend1":legend1,
#         "legend2": legend2,
#         "legend3": legend3,
#         "mons":mons,
#         "departments":departments,
#     }
#     return render_template('A&E_inpatient.html',result = data,report =report,username=current_user.get_id())


def trans_scale(list):
    list_new = []
    print("list",list)
    for i in list:
        if type(i) == str:
            i = i.strip()
        if i != "n" and i != '':
            list_new.append(int(i))
    print("list_new",list_new)
    if max(list_new) == 5:
        print("max is 5")
        top_box = list_new.count(5)/len(list_new)
        middle_box = (list_new.count(3)+list_new.count(4))/len(list_new)
        bottom_box = 1-middle_box-top_box
        return top_box,middle_box,bottom_box
    else:
        print("max is 4")
        top_box = list_new.count(4)/len(list_new)
        middle_box = list_new.count(3)/len(list_new)
        bottom_box = 1-middle_box-top_box     
        return top_box,middle_box,bottom_box 

def render_IPreport(department,fields):
    top_boxs = []
    middle_boxs = []
    bottom_boxs = []
    for i in ip_tables:
        results = []
        sql = "SELECT "+fields +" FROM KTPH."+i +" where Ward='"+department+"'"
        print(sql)   
        cursor.execute(sql)
        for i in cursor:
            results.extend(i) 
        top_box,middle_box,bottom_box  = trans_scale(results)
        middle_boxs.append(middle_box)
        top_boxs.append(top_box)
        bottom_boxs.append(bottom_box)
    return top_boxs,middle_boxs,bottom_boxs


@app.route('/Inpatient/<department>')
@login_required
def renderDepartment_report(department):
    report = {}
    labels, in_s,out_s = getLabelsDepartments()
    OverallExperience = render_IPreport(department,'A1')
    doctors = render_IPreport(department,"D1,D2,D3,D4")
    nurses = render_IPreport(department,"C1,C2,C3")
    AHPS = render_IPreport(department,"E1,E2,E3")
    meals = render_IPreport(department,"B1,B2")
    Empowerment = render_IPreport(department,"G1,G2,G3,G4")
  
    report['OverallExperience'] = OverallExperience
    report["doctors"]=doctors
    report['nurses']=nurses
    report['AHPS'] = AHPS
    report['meals'] = meals
    report['Empowerment'] = Empowerment

    data = {
        "legend1":legend1,
        "legend2": legend2,
        "legend3": legend3,
        "mons":labels,
        "indepartments":in_s,
    }
   
    return render_template(department+'.html',result = data,report =report,department = department,username=current_user.get_id())


# @app.route('/AMU_inpatient')
# @login_required
# def renderInpatientAMU():
#     mons, departments = render_month_department()
#     report = render_report('AMU')
#     legend1 = 'Top-box'
#     legend2 = 'Middle-box'
#     legend3 = 'Bottom-box'
#     data = {
#         "legend1": legend1,
#         "legend2": legend2,
#         "legend3": legend3,
#         "mons": mons,
#         "departments": departments,
#     }
#     return render_template('AMU_inpatient.html', result=data, report=report,username=current_user.get_id())
#
# @app.route('/HFU_inpatient')
# @login_required
# def renderInpatientHFU():
#     mons, departments = render_month_department()
#     report = render_report('HFU')
#     legend1 = 'Top-box'
#     legend2 = 'Middle-box'
#     legend3 = 'Bottom-box'
#     data = {
#         "legend1": legend1,
#         "legend2": legend2,
#         "legend3": legend3,
#         "mons": mons,
#         "departments": departments,
#     }
#     return render_template('HFU_inpatient.html', result=data, report=report,username=current_user.get_id())
#
# @app.route('/HFU_outpatient')
# @login_required
# def renderOutpatientHFU():
#     mons, departments = render_month_department()
#     return render_template('HFU_outpatient.html',departments = departments,username=current_user.get_id())


# @app.route('/AMU_outpatient')
# @login_required
# def renderOutpatientAMU():
#     mons, departments = render_month_department()
#     return render_template('AMU_outpatient.html',departments = departments,username=current_user.get_id())
#
#
# @app.route('/A&E_outpatient')
# @login_required
# def renderOutpatienAEt():
#     mons, departments = render_month_department()
#     return render_template('A&E_outpatient.html',departments = departments,username=current_user.get_id())
#
#
@app.route('/tables')
def renderTable():
    labels, in_s,out_s = getLabelsDepartments()
    sql1 = "SELECT * FROM KTPH.ip_0118improve;"
    cursor.execute(sql1)
    results = cursor.fetchall()
    
    sql2 = "SELECT COLUMN_NAME FROM information_schema.columns where table_name = 'ip_0118improve'";
    cursor.execute(sql2)
    columns = cursor.fetchall()

    return render_template('tables.html',columns = columns,results = results, in_s = in_s,out_s = out_s,username=current_user.get_id())



 



if __name__ == "__main__":
    app.run(debug=True)

