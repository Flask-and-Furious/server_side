from flask import Flask, request, jsonify, make_response, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

from dotenv import load_dotenv 
from os import environ 

# Load environment variables

load_dotenv()
database_uri = environ.get('DATABASE_URL') 
if 'postgres' in database_uri:
    database_uri = database_uri.replace('postgres:', 'postgresql:')
secret_key = environ.get('SECRET_KEY')

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLACHEMY_TRACK_MODIFICATIONS=environ.get('SQL_ALCHEMY_TRACK_MODIFICATIONS'),
    SECRET_KEY=secret_key
)

CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create database

@app.before_first_request
def create_tables():
    db.create_all()

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # Check hash with password 

    @property
    def password_hash(self):
	    raise AttributeError('password is not a readable attribute!')

    @password_hash.setter
    def password_hash(self, password):
	    self.password_hash = generate_password_hash(password)

    def verify_password_hash(self, password):
	    return check_password_hash(self.password_hash, password)


@app.route('/')
def home():
    return "<h1>Hello!</h1>"


@app.route('/login', methods=['POST'])
def login():
    data =  request.get_json()
    username = data['parameters']['username']
    password = data['parameters']['password']
    db_user = Users.query.filter_by(username=username).first()
    if db_user and check_password_hash(db_user.password, password):
                login_user(db_user)
                return make_response('success', 200)
    print(data)
    print(data['parameters'])
    return make_response('failed', 401)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print("Data test:", data)
    username = data['username']
    email = data['email']
    db_user = Users.query.filter_by(username=username).first()
    db_email = Users.query.filter_by(email=email).first()
    if db_user is not None:
        return make_response(f"{username} already exists", 403)
    elif db_email is not None:
        return make_response(f"{email} already exists", 403)
    else:
        new_user = Users(
            username = data['username'], 
            email=data['email'], 
            password=generate_password_hash(data['password']))
        db.session.add(new_user)
        db.session.commit()
        return make_response("user created", 201)

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
