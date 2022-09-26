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

@app.route('/code', methods=['POST']) # route for accepting codes from frontend
def incoming_code():
    snip = open('snippet.py', 'w') # create (or overwrite) a snippet.py file with the code content from the frontend
    snip.write(request.get_json()['code-package']['snippet']['body'])
    snip.close()
    import snippet # import the snippet.py here instead of the top because the content is updated at this stage only
    function_1 = request.get_json()['code-package']['snippet']['to-execute-1']
    function_2 = request.get_json()['code-package']['snippet']['to-execute-2']
    try:
        result_1 = eval(f'snippet.{function_1}')
        result_2 = eval(f'snippet.{function_2}')
    except SyntaxError:
        return 'Syntax Error' # Buggy
    except:
        return 'Unsuccessful attempt'      # This can be anything but the correct return value
    print('result after eval: ', result_1, result_2)
   
    return [result_1, result_2] # send back the returned value to frontend
    # integer cannot be returned for some reason. Hmmm... silly Python!


if __name__ == "__main__":
    app.run(debug=True)
