from flask import Flask, request, jsonify, make_response, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

from flask_jwt_extended import JWTManager, create_access_token

from dotenv import load_dotenv 
from os import environ
import random
import string
import importlib
import ast
import copy


# Load environment variables

load_dotenv()
database_uri = environ.get('DATABASE_URL') 
if 'postgres' in database_uri:
    database_uri = database_uri.replace('postgres:', 'postgresql:')
secret_key = environ.get('SECRET_KEY')

# Set up app

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLACHEMY_TRACK_MODIFICATIONS=environ.get('SQL_ALCHEMY_TRACK_MODIFICATIONS'),
    SECRET_KEY=secret_key,
    JWT_SECRET_KEY=environ.get('JWT_SECRET_KEY')
)

CORS(app)
jwt = JWTManager(app)
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
    password = db.Column(db.String(255), nullable=False)

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
    return "<h1>Welcome to debug server!</h1>"


@app.route('/login', methods=['POST'])
def login():
    try:
        data =  request.get_json()
        username = data['username']
        password = data['password']
        db_user = Users.query.filter_by(username=username).first()
        if db_user and check_password_hash(db_user.password, password):
                    access_token = create_access_token(identity=db_user.id)
                    login_user(db_user)
                    return jsonify({ "token": access_token, "user_id": db_user.id }, 200)
        return jsonify('failed', 401)
    except Exception as err:
        print(err)
        return jsonify("something went wrong!", 500)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@ app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print("Data test:", data)
        username = data['username']
        email = data['email']
        db_user = Users.query.filter_by(username=username).first()
        db_email = Users.query.filter_by(email=email).first()
        if db_user is not None:
            return jsonify(f"{username} already exists", 403)
        elif db_email is not None:
            return jsonify(f"{email} already exists", 403)
        else:
            new_user = Users(
                username = data['username'], 
                email=data['email'], 
                password=generate_password_hash(data['password']))
            db.session.add(new_user)
            db.session.commit()
            return jsonify("user created", 201)
    except Exception as err:
        print(err)
        return jsonify("something went wrong!", 500)

@app.route('/code', methods=['POST']) # route for accepting codes from frontend
def incoming_code():
    
    def convertExpr2Expression(Expr):
        Expr.lineno = 0
        Expr.col_offset = 0
        result = ast.Expression(Expr.value, lineno=0, col_offset = 0)
        return result

    def exec_with_return(code):
        code_ast = ast.parse(code)

        init_ast = copy.deepcopy(code_ast)
        init_ast.body = code_ast.body[:-1]

        last_ast = copy.deepcopy(code_ast)
        last_ast.body = code_ast.body[-1:]

        exec(compile(init_ast, "<ast>", "exec"), globals())
        if type(last_ast.body[0]) == ast.Expr:
            return eval(compile(convertExpr2Expression(last_ast.body[0]), "<ast>", "eval"),globals())
        else:
            exec(compile(last_ast, "<ast>", "exec"),globals())

    code_body = request.get_json()['code-package']['snippet']['body']
    test_function_1 = request.get_json()['code-package']['snippet']['to-execute-1']
    test_function_2 = request.get_json()['code-package']['snippet']['to-execute-2']
    result_1 = exec_with_return(f"{request.get_json()['code-package']['snippet']['body']}\n{request.get_json()['code-package']['snippet']['to-execute-1']}")
    # result_1 = eval(f'snippet.{function_1}')
    try:
        result_1 = exec_with_return(f"{code_body}\n{test_function_1}")
        result_2 = exec_with_return(f"{code_body}\n{test_function_2}")
    except SyntaxError:
        return 'Syntax Error' # Buggy
    except:
        return 'Unsuccessful attempt'      # This can be anything but the correct return value
    print('result after eval: ', result_1, result_2)
   
    return [result_1, result_2] # send back the returned value to frontend
    # integer cannot be returned for some reason. Hmmm... silly Python!

if __name__ == "__main__":
    app.run(debug=True)
