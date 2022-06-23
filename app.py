
from flask import Flask,request,jsonify,send_file,render_template
from flask_cors import CORS
import matplotlib
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from users import users
from flask_mysqldb import MySQL

matplotlib.use('Agg')

app = Flask(__name__)
df = pd.read_csv('CSMCQ_Interacting_with_others_Dummy.csv')

app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'juncture_test'

app.secret_key="secret"
CORS(app, support_credentials=True)
mysql = MySQL(app)
#Line, bar, scatter, histogram, boxplot, Wordcloud, spider/radar, Bubble Map

#functions to display plots
#---------boxplot--------------
def get_boxplot(data_list):
    img = BytesIO()
    plt.boxplot(data_list)
    plt.savefig(img,format='png')
    plt.close()
    img.seek(0)
    return img

#------------scatter plot -----------
def get_scatter():
    return ''

#main route
@app.route('/')
def home():
    return jsonify({'message':'Welcome'})

#plot
@app.route('/plot')
def plot():
    df_id = df.ID
    
    df_totalScore = df['Total Score by Applicant ']
    plt.plot(df_id[0:10], df_totalScore[0:10], color='orange', alpha=0.99)
    plt.xticks(rotation='vertical')
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return send_file(img, mimetype='image/png')

@app.route('/boxplot')
def boxplot():
    data = list([df['Building Inclusivity '], df['Collaboration '], df['Communication '], df['Customer Orientation'], df['Developing People'], df['Influence']])
    image = get_boxplot(data)
    #plot_url = base64.b64encode(image.getvalue()).decode('utf8')
    return send_file(image, mimetype='image/png')



#login
@app.route('/login',methods=['GET','POST'])
def login():
    
    if request.method == 'POST' and 'username' in request.json and 'password' in request.json:
        print(request.json)
        username = request.json['username']
        password_input = request.json['password']
        # if username == users['User_Name'] and password_input == users['User_Password']:
        #     return jsonify({'success':username}),201
        # else:
        #     return jsonify({'error':'Incorrect credentials'})
        cursor = mysql.connection.cursor()
        print('connected')
        query = "Select *from user_login WHERE User_Name=%s "
        cursor.execute(query,(username,))
        user = cursor.fetchone()
        print('user in db: ',user)
        if user and user[1] == password_input:

            return jsonify({'success':username})
        else:
            return jsonify({'error':'password incorrect'})
    else:
        return jsonify({'error':'Send both username and password'})


@app.route('/reset',methods=['GET','POST'])
def reset():
    if request.method == 'POST' and 'username' in request.json and 'password' in request.json:
        username = request.json['username']
        password = request.json['password']
        new_password = request.json['new_password']
        if users['User_name'] == username and users['User_Password']==password:           
            return jsonify({'password reset success':username}),201
        else:
            return jsonify({'error':'Username or Password incorrect incorrect'})


@app.route('/<string:username>/jobtitles')
def jobtitles(username):
    #select from jobs_table with matching username
    print(username)
    return jsonify({'jobs':['React','UI/UX Designer','Frontend Developer']})

    
if __name__ == "__main__":
    app.run(debug=True)