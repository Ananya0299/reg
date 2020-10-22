from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash
from flask_migrate import Migrate
from flask_cors import CORS
import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')



CORS(app, resources={r'/*': {'origins': '*'}})
db=SQLAlchemy(app)
migrate=Migrate(app,db)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True, unique=True)
    last_name = db.Column(db.String(64), index=True, unique=True)
    company_name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password= db.Column(db.String(128))

    def __init__(self, first_name, last_name, company_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.company_name = company_name
        self.email = self.email
        self.password=self.password


    def __repr__(self):
        return '<user {}>'.format(self.first_name)


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_user = User(first_name=data['first_name'], last_name=data['last_name'],company_name=data['company_name'],email=data['email'],password=data['password'])
            db.session.add(new_user)
            db.session.commit()
            return jsonify("user  has been created successfully.")
        else:
            return jsonify("The request payload is not in JSON format")

    else:
        return jsonify("error : Not POST method")




@app.route('/ping',methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__=='__main__':
    app.run()