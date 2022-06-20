
from flask import Flask,request,jsonify,send_file
from flask_cors import CORS
import matplotlib
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from users import users

matplotlib.use('Agg')

app = Flask(__name__)
df = pd.read_csv('CSMCQ_Interacting_with_others_Dummy.csv')

app.secret_key="secret"
CORS(app, support_credentials=True)


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


#login
@app.route('/login',methods=['GET','POST'])
def login():
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password_input = request.form['password']
        if username == users['User_Name'] and password_input == users['User_Password']:
            return jsonify({'success':username})
        return jsonify({'unsuccessful login with username: ':username})
    else:
        return jsonify({'error':'Send both username and password'})
    


if __name__ == "__main__":
    app.run(debug=True)