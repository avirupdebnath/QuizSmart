import aiT
import matplotlib.pyplot as plt
import re
from flask import Flask,request,render_template,flash,redirect,url_for
import sqlite3 as lite
import sys
import io
import base64
import pypyodbc

app = Flask(__name__)
app.secret_key="random string"
ability_lis=[]
qcount=0
qlimit=5
server = 'quicksmartsv.database.windows.net'
driver= '{ODBC Driver 17 for SQL Server}'
usernameSV = 'avirup'
passwordSV = 'Singapore404'
stuName=""

def generateQuestion(ability, subjectCode):
    conn = lite.connect('question.db')
    c = conn.cursor()
    # Contents of all columns for row that match a certain value in 1 column and then randomly selecting one out of them
    c.execute('SELECT * FROM QuestionBank WHERE ( AggregateParameter >= {n1} AND AggregateParameter <= {n2} AND SubjectCode == "{n3}" AND Answered == 0) ORDER BY RANDOM() LIMIT 1'.\
        format( n1 = ability-1, n2 = ability+1, n3=subjectCode ))
    fetchQuestion = c.fetchall()
    print (ability)
    print (ability_lis)
    print(fetchQuestion[0][11])
    with conn:
        c.execute('''UPDATE QuestionBank SET Answered = ? WHERE id = ?''', (int(1), int(fetchQuestion[0][0])))
    # Closing the connection to the database file
    conn.close()
    return fetchQuestion

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/login",methods=['POST'])
def checkNLogUser():
    global stuName
    stuName=""
    database = 'user'
    cnxn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+usernameSV+';PWD='+ passwordSV)
    c = cnxn.cursor()
    username = request.form['username']
    password = request.form['password']
    print(username , password)
    SQLcommand="SELECT * FROM UserDetails WHERE username = ? AND password = ? "
    row_count=c.execute(SQLcommand,[username,password])
    if(row_count!=0):
        fetchUser = c.fetchall()
        stuName=fetchUser[0][1]
        cnxn.close()
        return redirect(url_for('student_landing'))
    else:
        cnxn.close()
        return redirect(url_for('login'))

@app.route("/admin",methods=['POST'])
def checkNLogAdmin():
    admin = lite.connect('user.db')
    c = admin.cursor()
    username = request.form['username']
    password = request.form['password']
    print(username , password)
    c.execute('SELECT * FROM AdminDetail WHERE ( Username == "{n1}") '.\
        format( n1 = username ))
    fetchUser = c.fetchall()
    if(password==fetchUser[0][5]):
        admin.close()
        return redirect(url_for('entry'))
    else:
        admin.close()
        return redirect(url_for('admin'))

@app.route("/sign_up")
def sign_up():
    return render_template('sign_up.html')

@app.route("/admin_sign_up")
def admin_sign_up():
    return render_template('admin_sign_up.html')

@app.route("/sign_up", methods=['POST'])
def signUserUp():
    database = 'user'
    cnxn = pypyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+usernameSV+';PWD='+ passwordSV)
    name = str(request.form['name'])
    gender = str(request.form['sex'])
    email = str(request.form['email'])
    username = str(request.form['username'])
    password = str(request.form['password1'])
    password0 = str(request.form['password2'])
    print (name,gender,email,username,password,password0)
    if(password==password0):
        c1 = cnxn.cursor()
        c1.execute("if not exists (select * from sysobjects where name='UserDetails' and xtype='U')create table UserDetails (Id INT IDENTITY(1,1) PRIMARY KEY, Name TEXT, Gender TEXT, Email TEXT, Username TEXT, Password TEXT)")
        
        #c1.execute("CREATE TABLE IF NOT EXISTS UserDetail(Id INTEGER PRIMARY KEY AUTOINCREMENT,Name TEXT, Gender TEXT, Email TEXT, Username TEXT, Password TEXT )")
        c1.execute("INSERT INTO UserDetails(Name, Gender, Email, Username, Password) VALUES(?,?,?,?,?)",(name,gender,email,username,password))
        cnxn.commit()
        cnxn.close()
        return redirect(url_for('login'))
    else:
        flash("Passwords did not match!") 
        cnxn.close()
        return redirect(url_for('sign_up'))
   
@app.route("/admin_sign_up", methods=['POST'])
def signAdminUp():
    admin = lite.connect('user.db')
    name = str(request.form['name'])
    dept = str(request.form['dept'])
    reg = str(request.form['reg'])
    username = str(request.form['username'])
    password = str(request.form['password1'])
    password0 = str(request.form['password2'])
    print (name,dept,reg,username,password,password0)
    if(password==password0):
        with admin:
            c1 = admin.cursor()
            c1.execute("CREATE TABLE IF NOT EXISTS AdminDetail(Id INTEGER PRIMARY KEY AUTOINCREMENT,Name TEXT, Department TEXT, Registration TEXT, Username TEXT, Password TEXT )")
            c1.execute("INSERT INTO AdminDetail(Name, Department, Registration, Username, Password) VALUES(?,?,?,?,?)",(name,dept,reg,username,password))
        admin.close()
        return redirect(url_for('admin'))
    else:
        flash("Passwords did not match!")
        admin.close() 
        return redirect(url_for('admin_sign_up'))

@app.route("/student_landing")
def student_landing():
    conn = lite.connect('question.db')
    c = conn.cursor()
    global ability_lis
    ability_lis=[]
    global qcount
    qcount=0
    global stuName
    with conn:
        c.execute('''UPDATE QuestionBank SET Answered = 0''')
    conn.close()
    return render_template('student_landing.html',username=stuName)


@app.route("/entry")
def entry():
    return render_template('entry.html')

@app.route("/entry",methods=['POST'])
def addQuestionToBank():
    
    db = lite.connect('question.db')
    subjectCode = request.form['subjectCode']
    question = request.form['question']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    correctOption = request.form['correctOption']
    diff = request.form['difficulty']
    discrim = request.form['discrimination']
    guess = request.form['guess']
    x=aiT.fuzzyBox(diff,discrim,guess)

    with db:
        cur = db.cursor()    
        cur.execute("CREATE TABLE IF NOT EXISTS QuestionBank(Id INTEGER PRIMARY KEY AUTOINCREMENT, SubjectCode TEXT, Question TEXT, OptionA TEXT, OptionB TEXT, OptionC TEXT, OptionD TEXT, CorrectOption INT, Difficulty INT, Discrimination INT, Guess INT, AggregateParameter FLOAT, Answered INT)")
        cur.execute("INSERT INTO QuestionBank(SubjectCode, Question, OptionA, OptionB, OptionC, OptionD, CorrectOption, Difficulty, Discrimination, Guess, AggregateParameter) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(subjectCode,question,option1,option2,option3,option4,correctOption,diff,discrim,guess,x))
    print(x)    
    db.close()
    return render_template('transition.html')

@app.route("/quiz_ui/<subjectCode>")
def quiz_ui_get(subjectCode):
    ability=5
    global ability_lis
    global qcount
    global qlimit
    ability_lis.append(ability)
    subjectCode=str(subjectCode)
    fetchQuestion=generateQuestion(ability,subjectCode)
    questionId = fetchQuestion[0][0]    
    questionText = fetchQuestion[0][2]
    option1= fetchQuestion[0][3]
    option2= fetchQuestion[0][4]
    option3= fetchQuestion[0][5]
    option4= fetchQuestion[0][6]
    correct= fetchQuestion[0][7]
    correctOption=fetchQuestion[0][correct+2]
    print (questionId,questionText,option1,option2,option3,option4,correct)
    qcount+=1
    return render_template('quiz_ui.html',x=qcount, y=qlimit,question=questionText,option1=option1,option2=option2,option3=option3,option4=option4,ability=ability,correctOption=correctOption,subjectCode=subjectCode)
   
@app.route("/quiz_ui/<subjectCode>", methods= ['POST','GET'] )
def quiz_ui_post(subjectCode):
    ability=int(request.form['ability'])
    global ability_lis
    global qcount
    global stuName
    global qlimit
    subjectCode=str(subjectCode)
    if qcount==qlimit:
        kI=knowledge_index(ability)
        return render_template('result.html', graph1=build_graph(range(1,qlimit+1),ability_lis),stuName=stuName,kI=kI,subjectCode=subjectCode)
    if request.form['options']==request.form['correctOption']:
        if ability < 8:
            ability+=1
    else:
        if ability > 2:
            ability-=1
    ability_lis.append(ability)
    fetchQuestion=generateQuestion(ability,subjectCode)
    questionText = fetchQuestion[0][2]
    option1= fetchQuestion[0][3]
    option2= fetchQuestion[0][4]
    option3= fetchQuestion[0][5]
    option4= fetchQuestion[0][6]
    correct= fetchQuestion[0][7]
    correctOption=fetchQuestion[0][correct+2]
    qcount+=1
    return render_template('quiz_ui.html',x=qcount, y=qlimit, question=questionText,option1=option1,option2=option2,option3=option3,option4=option4,ability=ability,correctOption=correctOption,subjectCode=subjectCode)

def build_graph(x_coordinates, y_coordinates):
    img = io.BytesIO()
    plt.plot(x_coordinates, y_coordinates)
    plt.xlabel('Question No.') 
    # naming the y axis 
    plt.ylabel('Ability') 
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)

def knowledge_index(ability):
    if ability>=7:
        return "Advanced"
    elif ability<7 and ability>=5:
        return "Mediocre"
    else:
         return "Poor"
def graph():
    x=[1,2,3,4,5]
    plt.plot(x,ability_lis)
    # naming the x axis 
    plt.xlabel('Question No.') 
    # naming the y axis 
    plt.ylabel('Ability') 
    plt.xlim(1,5,1) 
    
    # giving a title to my graph 
    plt.title('Ability Flow') 
    
    # function to show the plot 
    plt.show() 
if __name__ == "__main__":
    app.run()