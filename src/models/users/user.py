__author__ = "Cobbin"
import uuid
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants
from passlib.hash import pbkdf2_sha512

class User(object):
    def __init__(self,name, email, password, author_id, profile_image=None, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.name = name
        self.email = email
        self.password = password
        self.author_id = author_id
        self.profile_image = None if profile_image is None else profile_image
#!--------------------------------------------
        #self.comments = comments
        

    def __repr__(self):
        return "<User {}>".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an e-mail/password combo (As sent by the site forms) is valid or not.
        Checks that the e-mail exists and that the password associated to the email is correct.
        :param email: The user's e-mail
        :param password: A sha512 hashed password
        :return: True if valid, False if otherwise.
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            # Tell the user their e-mail does'nt exist
            raise UserErrors.UserDontExistError("This e-mail does'nt exist ):")
        if not Utils.check_hashed_password(password, user_data['password']):
            # Tell the user that their password is wrong
            raise UserErrors.IncorrectPasswordError("Invalid Password ):")
        return True

    @staticmethod
    def register_user(name, email, password):
        """
        This registers a user using e-mail and password.
        The password already comes hashed as sha-512.
        :param email:   user's e-mail (might be invalid)
        :param password:    sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is not None:
            # Tell user they already exist
            raise UserErrors.UserAlreadyRegisteredError("The email already exists.")
        if not Utils.email_is_valid(email):
            # Tell user that their e-mail is not constructed properly.
            raise UserErrors.InvalidEmailError("The email does not have the right format.")
        author_id = uuid.uuid4().hex 
        User(name, email, Utils.hash_password(password), author_id).save_to_db()
        return True

    def save_to_db(self):
        Database.update(UserConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "name": self.name, 
            "email": self.email,
            "password": self.password,
            "author_id": self.author_id,
            "profile_image": self.profile_image
        }

    @classmethod
    def find_by_id(cls, id):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'_id': id}))

    @classmethod
    def find_by_email(cls, email):
        return cls(**Database.find_one(UserConstants.COLLECTION, {'email': email}))

    def delete(self):
        Database.remove(UserConstants.COLLECTION, {'author_id': self.author_id})

    def get_alerts(self):
        return Alert.find_by_user_email(self.email)
    
    @classmethod
    def all(cls):
        users = [cls(**elem) for elem in Database.find(UserConstants.COLLECTION, {})]
        users_details = [user.json() for user in users]
        for mem in user_details:
            mem['password'] = pbkdf2_sha512.decrypt(mem['password'])
        return users_details
