
from flask import Flask,request,jsonify,send_file,render_template
from flask_cors import CORS
import matplotlib
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
from users import users

matplotlib.use('Agg')

app = Flask(__name__)
df = pd.read_csv('CSMCQ_Interacting_with_others_Dummy.csv')

app.secret_key="secret"
CORS(app, support_credentials=True)

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
    
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        password_input = request.form['password']
        if username == users['User_Name'] and password_input == users['User_Password']:
            return jsonify({'success':username}),201
        return jsonify({'error':'Incorrect credentials'})
    else:
        return jsonify({'error':'Send both username and password'})


@app.route('/reset',methods=['GET','POST'])
def reset():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        new_password = request.form['new_password']
        if users['User_name'] == username and users['User_Password']==password:
            
            return jsonify({'password reset success':username}),201
        else:
            return jsonify({'error':'Username or Password incorrect incorrect'})


@app.route('/<string:username>/jobtitles')
def jobtitles(username):

    return jsonify({'jobs':['React','UI/UX Designer','Frontend Developer']})
if __name__ == "__main__":
    app.run(debug=True)