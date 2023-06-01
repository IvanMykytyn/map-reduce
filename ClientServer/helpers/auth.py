# import hashlib
#
# import jwt
#
# from ClientServer.constants import JWT_SECRET_KEY
# # from ClientServer.models.User import get_user_by_id, get_username_by_id
#
#
# def get_username(request):
#     token = request.headers.get('Authorization')
#     decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
#     user_id = decoded_token['user_id']
#     username = get_username_by_id(user_id)
#     return username
#
#
# def get_user(request):
#     token = request.headers.get('Authorization')
#     decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
#     user_id = decoded_token['user_id']
#     user = get_user_by_id(user_id)
#     return user
#
#
# def get_auth_header(request):
#     token = request.headers.get('Authorization')
#     return {'Authorization': token}
#
#
# def get_hash(password):
#     hash_object = hashlib.sha256(password.encode())
#     return hash_object.hexdigest()
#
#
# def is_valid_password(password, hashed_password):
#     hash_object = hashlib.sha256(password.encode())
#     return hash_object.hexdigest() == hashed_password
