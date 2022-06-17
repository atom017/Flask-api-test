
from flask import Flask, render_template,request,jsonify
from flask_cors import CORS

app = Flask(__name__)


app.secret_key="secret"
CORS(app, support_credentials=True)


@app.route('/')
def home():
    return jsonify({'message':'Welcome'})



if __name__ == "__main__":
    app.run(debug=True)