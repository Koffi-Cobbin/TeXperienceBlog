__author__ = "Cobbin"
from passlib.hash import pbkdf2_sha512
import re

class Utils(object):
    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches that of the database
        The Database password is encrypted more than the user's password at this satge.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return" True if passwordsss mathch else False.
        """
        try:
            return pbkdf2_sha512.verify(password, hashed_password)
        except:
            return False
        