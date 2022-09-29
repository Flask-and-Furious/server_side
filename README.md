# Bug Basher Server

Python Server for [Bug Basher](https://bug-basher.netlify.app/)

Deployed Server URL [https://python-debug.herokuapp.com](https://python-debug.herokuapp.com)


## Installation & Usage 

- Clone/download the repo or try the deployed version
- `pipenv shell` : to start virtual environment
- `pipenv install` --dev : install all required packages.
- Set up environment variables in a `.env` file.

```bash
FLASK_ENV=XXXX
DATABASE_URL=XXXX
SQL_ALCHEMY_TRACK_MODIFICATIONS=XXXX
SECRET_KEY=XXXX
JWT_SECRET_KEY=XXXX
```
- `pipenv run dev` : run the development server

## Routes 

### GET requests

`/` : Welcome message 

### POST request 

- `/register` : To register a new user 

```bash
"username": "test",
"email": "test@gmail.com",
"password": "12345678"
```
- `/login`  : To login an existing user 

```bash
"username": "test",
"password": "12345678"
```
- `/code` : To store/run the snippet codes from the frontend

```bash
'id': 0,                       // sample buggy functions
     'snippet': {
        'description': 'Debug the multiplication',
        'import': 'multiply',
        'body' : 'function multiply(a, b) {\n\treturn a * a\n}',
        'to-execute-1': 'multiply(3,2)',
        'return-1' : 6,
        'to-execute-2': 'multiply(6,4)',
        'return-2' : 24
```













