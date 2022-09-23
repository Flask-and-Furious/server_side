import os
from flask import Flask, render_template, request
from flask_cors import CORS
from werkzeug import exceptions
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ

# Load environment variables

load_dotenv()
database_uri = environ.get('DATABASE_URL')

# Set up the app 

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLACHEMY_TRACK_MODIFICATIONS=environ.get('SQL_ALCHEMY_TRACK_MODIFICATIONS')
)

CORS(app)

db = SQLAlchemy(app)

# Database

@app.before_first_request
def create_tables():
    # Clear it all out
    db.drop_all()

    # Set it back 
    db.create_all()

# Models 



# Routes 

@app.route('/')
def home():
    return "Hello!"

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/code', methods=['POST'])
def incoming_code():
    snippet = open('snippet.py', 'w')
    snippet.write(request.get_json()['code'] + '\n\nif __name__ == "__main__":\n\tadd(2,3)')
    snippet.close()
    print('request: ', request.get_json()['code'])
    result = os.system('python snippet.py')
    print('result variable in fn: ', result)
    # subprocess.call('snippet.py', shell=True)
    # f = open("demofile3.txt", "w")
    # f.write("Woops! I have deleted the content!")
    # f.close()
    return 'Data from frontend'


if __name__ == "__main__":
    app.run(debug=True)
