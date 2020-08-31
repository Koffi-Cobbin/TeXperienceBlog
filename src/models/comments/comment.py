__author__ = "Cobbin"

import uuid
from src.common.database import Database
from src.common.utils import Utils
from datetime import datetime
import src.models.comments.constants as  CommentConstants

class Comment(object):
    def __init__(self, content, user_id, blog_id, author_id, date_posted=None, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.content = content
        self.user_id = user_id
        self.blog_id = blog_id
        self.author_id = author_id
        self.date_posted = datetime.utcnow() if date_posted is None else date_posted

    def __repr__(self):
            return '<Comment %r>' % self._id

    def json(self):
        return {
            "_id" : self._id ,
            "content": self.content,
            "user_id": self.user_id,
            "blog_id": self.blog_id,
            "author_id": self.author_id,
            "date_posted": self.date_posted
        }

    @classmethod
    def get_by_id(cls, id):
        return cls(**Database.find_one(CommentConstants.COLLECTION, {"_id": id}))

    def save_to_mongo(self):
        Database.update(CommentConstants.COLLECTION, {"_id": self._id} ,self.json())
        return self._id

    @classmethod
    def get_by_blog_id(cls, blog_id):
        return [cls(**elem) for elem in Database.find(CommentConstants.COLLECTION, {"blog_id": blog_id})] 

    @classmethod
    def all(cls):
        return [cls(**elem) for elem in Database.find(CommentConstants.COLLECTION, {})]

    def delete(self):
        Database.remove(CommentConstants.COLLECTION, {'_id': self._id}) 

    @classmethod
    def get_post_comments(cls, query_name, other_id):
        return [cls(**elem) for elem in Database.find(CommentConstants.COLLECTION, {f"{query_name}": other_id})] 

    @classmethod
    def delete_post_comments(cls, query_name, other_id):
        cmt_lst = Comment.get_post_comments(query_name, other_id)
        for cmt in cmt_lst:
            cmt.delete()
