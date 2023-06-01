# import jwt
# from flask import Blueprint, request, jsonify
#
# auth_route = Blueprint('route', __name__)
#
#
# @auth_route.route('/login', methods=['POST'])
# def login():
#     # get username and password from request
#     username = request.json.get('username', None)
#     password = request.json.get('password', None)
#
#     # check if username exists and password are valid
#     user = get_user_by_username(username)
#     if user:
#         if is_valid_password(password, user.password):
#             token = jwt.encode({'user_id': user.id, 'role': user.role}, JWT_SECRET_KEY, algorithm='HS256')
#             return jsonify({'token': token}), 200
#         else:
#             return jsonify({'message': 'Incorrect Credentials'}), 401
#     else:
#         return jsonify({'message': 'User does not exist'}), 401
#
#
# @auth_route.route('/register', methods=['POST'])
# def register():
#     # get username and password from request
#     username = request.json.get('username', None)
#     password = request.json.get('password', None)
#
#     user = get_user_by_username(username)
#
#     if user:
#         return jsonify({'message': 'Such username already exists'}), 404
#
#     hashed_password = get_hash(password)
#
#     add_user(username=username, password=hashed_password)
#     user = get_user_by_username(username)
#
#     token = jwt.encode({'user_id': user.id, 'role': user.role}, JWT_SECRET_KEY, algorithm='HS256')
#     return jsonify({'token': token}), 200
