#!/usr/bin/env python3
"""Module for session auth views"""
from flask import request, jsonify, abort
from api.v1.views import app_views
from models.user import User


from os import getenv


# @app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
# def session_login():
#     """session login authentication route"""
#     email = request.form.get('email')
#     password = request.form.get('password')

#     if email is None or len(email) == 0:
#         return jsonify({'error': "email missing"}), 400

#     if password is None or len(password) == 0:
#         return jsonify({'error': "password missing"}), 400

#     session_user_instance = User.search({'email': email})

#     if not session_user_instance:
#         return jsonify({"error": "no user found for this email"}), 404
#     else:
#         for session_user in session_user_instance:
#             is_valid = session_user.is_valid_password(password)

#             if not is_valid:
#                 return jsonify({"error": "wrong password"}), 401
#             else:
#                 from api.v1.app import auth

#                 user_id = getattr(session_user, 'id')
#                 session_id = auth.create_session(user_id)

#                 response = jsonify(session_user.to_json())
#                 response.set_cookie(getenv("SESSION_NAME"), session_id)

#                 return response

#     return jsonify({'email': email, 'password': password})


@app_views.route(
    '/auth_session/logout',
    methods=['DELETE'],
    strict_slashes=False
)
def session_logout():
    """session logout route"""
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
