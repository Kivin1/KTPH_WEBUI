# from werkzeug.security import generate_password_hash
# from werkzeug.security import check_password_hash
from flask_login import UserMixin
# from flaskext.mysql import MySQL
# import uuid
# import flask
#
# app = flask.Flask(__name__)
# # define profile.json constant, the file is used to
# # save user name and password_hash
# # PROFILE_FILE = "profiles.json"
# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'ktph'
# app.config['MYSQL_DATABASE_DB'] = 'inpatient'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)
#
# conn = mysql.connect()
# cursor = conn.cursor()
#
# class User(UserMixin):
#     def __init__(self, username,password):
#         self.username = username
#         self.set_password(username,password)
#
#
#     def set_password(self,username,password):
#         self.pw_hash =generate_password_hash(password)
#         self.na_hash =generate_password_hash(username)
#
#     def check_name_password(self,username,password):
#
#         result =  check_password_hash(self.pw_hash,password) and check_password_hash(self.na_hash,username)
#
#         return result
#
#     # def get_id(self):
#     #     """get user id from profile file, if not exist, it will
#     #             generate a uuid for the user.
#     #             """
#     #     if self.username is not None:
#     #         try:
#     #             sql = "SELECT User.user FROM inpatient.User;"
#     #             cursor.execute(sql)
#     #             for i in cursor:
#     #                 if self.username in i:
#     #                     return
#     #         except IOError:
#     #             pass
#     #
#     #     return uuid.uuid4()
#
#
#
#
#
#
#
#
#
#     # @property
#     # def password(self):
#     #     raise AttributeError('password is not a readable attribute')
#     #
#     # @password.setter
#     # def password(self, password):
#     #     """save user name, id and password hash to json file"""
#     #     self.password_hash = generate_password_hash(password)
#     #     with open(PROFILE_FILE, 'w+') as f:
#     #         try:
#     #             profiles = json.load(f)
#     #         except ValueError:
#     #             profiles = {}
#     #         profiles[self.username] = [self.password_hash,
#     #                                    self.id]
#     #         f.write(json.dumps(profiles))
#     #
#     # def verify_password(self, password):
#     #     if self.password_hash is None:
#     #         return False
#     #     return check_password_hash(self.password_hash, password)
#     #
#     # def get_password_hash(self):
#     #     """try to get password hash from file.
#     #
#     #     :return password_hash: if the there is corresponding user in
#     #             the file, return password hash.
#     #             None: if there is no corresponding user, return None.
#     #     """
#     #     try:
#     #         with open(PROFILE_FILE) as f:
#     #             user_profiles = json.load(f)
#     #             user_info = user_profiles.get(self.username, None)
#     #             if user_info is not None:
#     #                 return user_info[0]
#     #     except IOError:
#     #         return None
#     #     except ValueError:
#     #         return None
#     #     return None
#     #
#     # def get_id(self):
#     #     """get user id from profile file, if not exist, it will
#     #     generate a uuid for the user.
#     #     """
#     #     if self.username is not None:
#     #         try:
#     #             with open(PROFILE_FILE) as f:
#     #                 user_profiles = json.load(f)
#     #                 if self.username in user_profiles:
#     #                     return user_profiles[self.username][1]
#     #         except IOError:
#     #             pass
#     #         except ValueError:
#     #             pass
#     #     return uuid.uuid4()
#     #
#     # @staticmethod
#     # def get(user_id):
#     #     """try to return user_id corresponding User object.
#     #     This method is used by load_user callback function
#     #     """
#     #     if not user_id:
#     #         return None
#     #     try:
#     #         with open(PROFILE_FILE) as f:
#     #             user_profiles = json.load(f)
#     #             for user_name, profile in user_profiles.iteritems():
#     #                 if profile[1] == user_id:
#     #                     return User(user_name)
#     #     except:
#     #         return None
#     #     return None
#     @staticmethod
#     def get(self,username):
#         """try to return user_id corresponding User object.
#         This method is used by load_user callback function
#         """
#         if self.username is None:
#             return None
#         try:
#             sql = "SELECT User.user FROM inpatient.User;"
#             cursor.execute(sql)
#             for i in cursor:
#                 if self.username in i:
#                     return username
#         except:
#             return None
#         return None
#
class User(UserMixin):
    pass