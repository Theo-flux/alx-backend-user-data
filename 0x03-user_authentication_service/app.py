#!/usr/bin/env python3
"""basic flask app module"""
from flask import (
    Flask,
    jsonify,
    request,
    abort,
    redirect
)
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
      - 401 if can't create the new User
    """
    mail = request.form.get('email')
    pwd = request.form.get('password')

    flag = AUTH.valid_login(email=mail, password=pwd)
    if flag:
        session_id = AUTH.create_session(mail)
        res = jsonify({"email": f"{mail}", "message": "logged in"})
        res.set_cookie("session_id", session_id)
        return res
    return abort(401, description="unauthorized")


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ DELETE /api/v1/users/:id
    Return:
      - redirects to home route
      - 403 if the User ID doesn't exist
    """
    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id)

    if session_id is None or user is None:
        return abort(403, description='Forbidden')

    AUTH.destroy_session(getattr(user, 'id'))
    return redirect('/')


@app.route('/profile', strict_slashes=False)
def profile():
    """ DELETE /api/v1/users/:id
    Return:
      - redirects to home route
      - 403 if the User ID doesn't exist
    """
    session_id = request.cookies.get('session_id', None)
    user = AUTH.get_user_from_session_id(session_id)

    if session_id is None or user is None:
        return abort(403, description='Forbidden')

    return jsonify({"email": f"{getattr(user, 'email')}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
