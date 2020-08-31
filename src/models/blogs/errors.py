__author__ = "Cobbin"

class BlogException(Exception):
    def __init__(self, message):
        self.message = message

class BlogNotFoundException(BlogException):
    pass
