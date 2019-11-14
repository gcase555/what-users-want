# from flask import g
# from flask_httpauth import HTTPBasicAuth

# import models

# basic_auth = HTTPBasicAuth()
# auth = basic_auth


# # TODO: Switch to token based
# @basic_auth.verify_password
# def verify_password(username, password):
#     from IPython import embed; embed()
#     try:
#         user = models.User.get(
#             (models.User.username == username)
#         )
#         if not user.verify_password(password):
#             return False
#     except models.User.DoesNotExist:
#         return False
#     else:
#         g.user = user
#         return True
