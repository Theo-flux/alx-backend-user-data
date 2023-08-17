#!/usr/bin/env python3
"""basic flask app module"""
from flask import Flask, jsonify, request, abort
from sqlalchemy.orm.exc import NoResultFound

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def index():
    """return joson payload"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ POST /users
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    mail = request.form['email']
    pwd = request.form['password']

    try:
        AUTH.register_user(mail, pwd)
    except ValueError:
        return jsonify({"message": "email already registered"})
    else:
        return jsonify({"email": f"{mail}", "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ POST /users
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    mail = request.form['email']
    pwd = request.form['password']

    flag = AUTH.valid_login(email=mail, password=pwd)
    if flag:
        session_id = AUTH.create_session(mail)
        res = jsonify({"email": f"{mail}", "message": "user created"})
        res.set_cookie("session_id", session_id)
        return res
    return abort(401, description="unautheorized user")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
