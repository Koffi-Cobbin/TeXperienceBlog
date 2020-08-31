__author__ = "Cobbin"
import uuid
from src.common.database import Database
import src.models.blogs.constants as BlogConstants
import src.models.blogs.errors as blogErrors
from datetime import datetime   

class BlogPost(object):
    def __init__(self, title, content, author, author_id, category, date_posted = None, likes=None, post_images=None, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.author = author
        self.author_id = author_id
        self.title = title
        self.content = content
        self.category = category
        self.date_posted = datetime.utcnow() if date_posted is None else date_posted
        self.likes = [0] if likes is None else likes
        self.post_images = [] if post_images is None else post_images
        #self.comments = comments
        

    def __repr__(self):
        return "<Post for {}>".format(self.author)

    def json(self):
        return {
            "_id": self._id,
            "author": self.author,
            "author_id": self.author_id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "date_posted": self.date_posted,
            "likes": self.likes,
            "post_images": self.post_images
            #"comments": self.comments
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(BlogConstants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        Database.update(BlogConstants.COLLECTION, {"_id": self._id} ,self.json())
        return self._id

    @classmethod
    def get_by_name(cls, blog_title):
        return cls(**Database.find_one(BlogConstants.COLLECTION, {"title": blog_title}))

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(BlogConstants.COLLECTION, {})]

    @classmethod
    def get_author_posts(cls, author_id):
        return [cls(**elem) for elem in Database.find(BlogConstants.COLLECTION, {'author_id': author_id})] 

    def delete(self):
        Database.remove(BlogConstants.COLLECTION, {'_id': self._id}) 

    @classmethod
    def delete_author_posts(cls, author_id):
        posts = BlogPost.get_author_posts(author_id)
        for post in posts:
            post.delete()
#---------------------------------------------------------------------------------------------------------------



